"""Unified Mesh Client and End-to-End Service Communication Pipeline."""

from __future__ import annotations

import time
import uuid
from typing import Any, Callable, Dict, Optional

from ..mesh.control_plane import ServiceMeshController
from ..mesh.data_plane import MeshRequest, MeshResponse
from ..identity.service_identity import ServiceIdentityManager
from ..identity.certificates import CertificateManager
from ..identity.workload import WorkloadAttestationManager, SVIDType
from ..security.mtls import MTLSManager, MTLSMode
from ..security.policies import NetworkPolicyEngine, PolicyAction
from ..security.authorization import ZeroTrustEvaluator, ZeroTrustSubject, ZeroTrustResource
from ..discovery.registry import ServiceRegistry, ServiceEndpoint
from ..discovery.resolver import ServiceResolver
from ..routing.router import TrafficRouter
from ..routing.policies import RoutingPolicyEngine, LoadBalancingAlgorithm
from ..routing.traffic_split import TrafficSplitter
from ..resilience.retry import RetryPolicyEngine, RetryPolicy
from ..resilience.circuit_breaker import CircuitBreaker
from ..resilience.fault_injection import FaultInjectionEngine
from ..load_balancing.algorithms import LoadBalancerEngine
from ..load_balancing.health import HealthCheckEngine
from ..telemetry.metrics import MeshMetricsCollector
from ..telemetry.traces import TraceContextPropagator, MeshSpan, SpanKind
from ..telemetry.logs import MeshAccessLogger, MeshAccessLogRecord


class MeshClient:
    """Enterprise Service Mesh Client orchestrating secure, resilient, observable service-to-service communication."""

    def __init__(
        self,
        service_name: str = "docutask-app",
        namespace: str = "default",
        node_id: Optional[str] = None,
        region: str = "us-central1",
        zone: str = "us-central1-a",
    ):
        self.service_name = service_name
        self.namespace = namespace
        self.node_id = node_id or f"node-{service_name}-{uuid.uuid4().hex[:6]}"
        self.region = region
        self.zone = zone

        # Core Subsystems
        self.controller = ServiceMeshController()
        self.cert_manager = CertificateManager()
        self.identity_manager = ServiceIdentityManager()
        self.attestation_manager = WorkloadAttestationManager(cert_manager=self.cert_manager)
        self.mtls_manager = MTLSManager(cert_manager=self.cert_manager)
        self.policy_engine = NetworkPolicyEngine(default_action=PolicyAction.ALLOW)
        self.zero_trust_evaluator = ZeroTrustEvaluator(policy_engine=self.policy_engine)
        self.registry = ServiceRegistry()
        self.resolver = ServiceResolver(registry=self.registry)
        self.router = TrafficRouter()
        self.routing_policy_engine = RoutingPolicyEngine()
        self.traffic_splitter = TrafficSplitter()
        self.retry_engine = RetryPolicyEngine()
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.fault_injector = FaultInjectionEngine()
        self.load_balancer = LoadBalancerEngine()
        self.health_engine = HealthCheckEngine(registry=self.registry)
        self.metrics = MeshMetricsCollector()
        self.logger = MeshAccessLogger()

        # Local handler registry for mock/in-process endpoints
        # key: f"{namespace}/{service_name}/{action}"
        self._local_handlers: Dict[str, Callable[[MeshRequest], MeshResponse]] = {}

        # Issue self identity & certificate
        self.identity = self.identity_manager.mint_identity(
            service_name=self.service_name,
            namespace=self.namespace,
        )
        self.svid = self.attestation_manager.attest_workload(
            service_name=self.service_name,
            namespace=self.namespace,
            svid_type=SVIDType.X509,
        )

    def register_handler(
        self,
        service_name: str,
        action: str,
        handler_fn: Callable[[MeshRequest], MeshResponse],
        namespace: str = "default",
    ) -> None:
        """Register a handler for a service endpoint."""
        key = f"{namespace}/{service_name}/{action}"
        self._local_handlers[key] = handler_fn

        # Ensure service is registered in discovery
        ep_id = f"ep-{service_name}-{uuid.uuid4().hex[:6]}"
        self.registry.register_endpoint(
            ServiceEndpoint(
                endpoint_id=ep_id,
                service_name=service_name,
                namespace=namespace,
                host=f"{service_name}.{namespace}.internal",
                port=8080,
                region=self.region,
                zone=self.zone,
            )
        )

    def get_circuit_breaker(self, target_service: str) -> CircuitBreaker:
        if target_service not in self.circuit_breakers:
            self.circuit_breakers[target_service] = CircuitBreaker(service_name=target_service)
        return self.circuit_breakers[target_service]

    def call(
        self,
        target_service: str,
        action: str,
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        target_namespace: str = "default",
        timeout_ms: float = 5000.0,
        retry_policy: Optional[RetryPolicy] = None,
        custom_headers: Optional[Dict[str, str]] = None,
    ) -> MeshResponse:
        """Execute complete service-to-service communication call through the mesh fabric."""
        start_time = time.time()
        req_headers = dict(headers or {})
        if custom_headers:
            req_headers.update(custom_headers)

        # 1. Distributed Tracing - Inject context
        trace_id = req_headers.get("x-b3-traceid") or TraceContextPropagator.generate_trace_id()
        span_id = TraceContextPropagator.generate_span_id()
        req_headers = TraceContextPropagator.inject_w3c_headers(trace_id, span_id, req_headers)

        span = MeshSpan(
            span_id=span_id,
            trace_id=trace_id,
            name=f"{self.service_name}->{target_service}:{action}",
            kind=SpanKind.CLIENT,
            start_time=start_time,
            attributes={"target.service": target_service, "action": action},
        )

        request = MeshRequest(
            source_service=self.service_name,
            source_namespace=self.namespace,
            target_service=target_service,
            target_namespace=target_namespace,
            action=action,
            path=f"/{action}",
            payload=payload or {},
            headers=req_headers,
            trace_id=trace_id,
            span_id=span_id,
            timeout_ms=timeout_ms,
        )

        # 2. Resilience: Circuit Breaker wrapping
        cb = self.get_circuit_breaker(target_service)

        def _execute_pipeline(req: MeshRequest) -> MeshResponse:
            # 3. Fault Injection Simulation
            fault_res = self.fault_injector.evaluate_and_inject(req)
            if fault_res is not None:
                return fault_res

            # 4. Identity & Zero-Trust Authorization Evaluation
            subject = ZeroTrustSubject(
                spiffe_uri=self.identity.spiffe_id.uri,
                tenant_id=self.identity.tenant_id,
                roles=self.identity.roles,
            )
            resource = ZeroTrustResource(
                service_name=target_service,
                namespace=target_namespace,
                path=req.path,
                action=req.action,
            )
            zt_decision = self.zero_trust_evaluator.evaluate(subject, resource)
            if not zt_decision.allowed:
                return MeshResponse(
                    status_code=403,
                    error_message=f"Zero-Trust Authorization Denied: {zt_decision.reason}",
                    request_id=req.request_id,
                    applied_policy=zt_decision.policy_action.value,
                )

            # 5. Service Discovery & Resolution
            resolved = self.resolver.resolve(
                target_name_or_host=target_service,
                caller_region=self.region,
                caller_zone=self.zone,
            )
            if not resolved.endpoints:
                return MeshResponse(
                    status_code=503,
                    error_message=f"No healthy endpoints found for service '{target_service}' in namespace '{target_namespace}'",
                    request_id=req.request_id,
                )

            # 6. Routing & Traffic Splitting
            selected_version = self.traffic_splitter.select_version(target_service, target_namespace)
            endpoint = self.load_balancer.select_endpoint(
                resolved.endpoints,
                algorithm=LoadBalancingAlgorithm.ROUND_ROBIN,
            )
            if not endpoint:
                return MeshResponse(
                    status_code=503,
                    error_message=f"Load balancer failed to select endpoint for '{target_service}'",
                    request_id=req.request_id,
                )

            # 7. mTLS Handshake & Encryption Session
            server_svid = self.attestation_manager.attest_workload(
                service_name=target_service,
                namespace=target_namespace,
                svid_type=SVIDType.X509,
            )
            handshake = self.mtls_manager.perform_handshake(
                client_cert_serial=self.svid.token_or_serial,
                server_cert_serial=server_svid.token_or_serial,
                mode=MTLSMode.STRICT,
            )
            if not handshake.success:
                return MeshResponse(
                    status_code=502,
                    error_message=f"mTLS handshake failure: {handshake.error_reason}",
                    request_id=req.request_id,
                )

            # 8. Dispatch to Target Service Handler
            handler_key = f"{target_namespace}/{target_service}/{action}"
            handler = self._local_handlers.get(handler_key)

            self.load_balancer.record_connection_start(endpoint.endpoint_id)
            try:
                if handler:
                    res = handler(req)
                else:
                    # Default mock response when no explicit handler is bound
                    res = MeshResponse(
                        status_code=200,
                        payload={
                            "result": "success",
                            "service": target_service,
                            "action": action,
                            "version": selected_version,
                            "processed_by": endpoint.endpoint_id,
                            "received_payload": req.payload,
                        },
                    )

                res.routed_node_id = endpoint.endpoint_id
                # Record health outcome
                is_err = res.status_code >= 500
                self.health_engine.record_call_result(endpoint.endpoint_id, is_error=is_err)

                # Check Shadow Traffic Mirroring
                should_mirror, shadow_ver = self.traffic_splitter.should_mirror_shadow(target_service, target_namespace)
                if should_mirror and shadow_ver:
                    shadow_res = MeshResponse(
                        status_code=res.status_code,
                        payload={"shadow": True, "version": shadow_ver},
                        duration_ms=res.duration_ms,
                    )
                    self.traffic_splitter.record_shadow_execution(req, shadow_ver, shadow_res)

                return res
            finally:
                self.load_balancer.record_connection_end(endpoint.endpoint_id)

        # Execute with retry engine and circuit breaker
        response = cb.execute(
            request,
            lambda r: self.retry_engine.execute_with_retry(r, _execute_pipeline, policy=retry_policy),
        )

        # 9. Telemetry Recording
        duration_ms = (time.time() - start_time) * 1000.0
        response.duration_ms = duration_ms
        response.request_id = request.request_id

        span.finish(status_code=response.status_code)
        self.metrics.record_call(
            source_service=self.service_name,
            target_service=target_service,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        self.logger.log_access(
            MeshAccessLogRecord(
                timestamp=time.time(),
                request_id=request.request_id,
                trace_id=trace_id,
                source_service=self.service_name,
                target_service=target_service,
                method=request.method,
                path=request.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
                mtls_authenticated=True,
                security_decision="ALLOW" if response.status_code < 400 else "REJECT_OR_ERROR",
                error_message=response.error_message,
            )
        )

        return response
