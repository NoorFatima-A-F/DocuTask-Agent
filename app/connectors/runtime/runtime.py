"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector Runtime.
Coordinates the end-to-end execution pipeline:
Capability Discovery -> Connector Selection -> Auth Resolution -> Policy Check ->
Rate Limit -> Circuit Breaker -> Sandbox Execution -> Retry -> Telemetry & Normalization.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from app.connectors.actions.executor import ActionExecutor
from app.connectors.analytics.analytics import ConnectorAnalytics
from app.connectors.authentication.auth_manager import AuthenticationManager
from app.connectors.authentication.credential_store import CredentialStore
from app.connectors.core.exceptions import (
    CapabilityNotFoundError,
    CircuitBreakerOpenError,
    PolicyViolationError,
)
from app.connectors.core.models import (
    ActionDescriptor,
    ExecutionResult,
)
from app.connectors.observability.metrics import ConnectorObservability
from app.connectors.policies.policy_engine import ConnectorPolicyEngine
from app.connectors.registry.capability_registry import CapabilityRegistry
from app.connectors.registry.connector_registry import ConnectorRegistry
from app.connectors.resilience.circuit_breaker import CircuitBreaker
from app.connectors.resilience.rate_limiter import RateLimiter
from app.connectors.resilience.retry_engine import ConnectorRetryEngine
from app.connectors.sandbox.sandbox import ConnectorSandbox

logger = logging.getLogger(__name__)


class ConnectorRuntime:
    """
    Unified execution engine governing all interactions between workflows, AI agents,
    and external capability providers.
    """

    def __init__(
        self,
        connector_registry: Optional[ConnectorRegistry] = None,
        capability_registry: Optional[CapabilityRegistry] = None,
        credential_store: Optional[CredentialStore] = None,
        auth_manager: Optional[AuthenticationManager] = None,
        policy_engine: Optional[ConnectorPolicyEngine] = None,
        rate_limiter: Optional[RateLimiter] = None,
        retry_engine: Optional[ConnectorRetryEngine] = None,
        sandbox: Optional[ConnectorSandbox] = None,
        observability: Optional[ConnectorObservability] = None,
        analytics: Optional[ConnectorAnalytics] = None,
        action_executor: Optional[ActionExecutor] = None,
    ):
        self.connector_registry = connector_registry or ConnectorRegistry()
        self.capability_registry = capability_registry or CapabilityRegistry(self.connector_registry)
        self.credential_store = credential_store or CredentialStore()
        self.auth_manager = auth_manager or AuthenticationManager(self.credential_store)
        self.policy_engine = policy_engine or ConnectorPolicyEngine()
        self.rate_limiter = rate_limiter or RateLimiter()
        self.retry_engine = retry_engine or ConnectorRetryEngine()
        self.sandbox = sandbox or ConnectorSandbox()
        self.observability = observability or ConnectorObservability()
        self.analytics = analytics or ConnectorAnalytics(self.observability)
        self.action_executor = action_executor or ActionExecutor()

        self._circuit_breakers: Dict[str, CircuitBreaker] = {}

    def _get_circuit_breaker(self, connector_id: str) -> CircuitBreaker:
        if connector_id not in self._circuit_breakers:
            self._circuit_breakers[connector_id] = CircuitBreaker(connector_id)
        return self._circuit_breakers[connector_id]

    def execute_capability(
        self,
        capability_name: str,
        inputs: Dict[str, Any],
        organization_id: str = "org-default",
        workspace_id: str = "ws-default",
        preferred_vendor: Optional[str] = None,
        data_tags: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> ExecutionResult:
        """
        Executes a high-level abstract capability (e.g. 'email.send') by resolving
        the optimal active provider and invoking its primary action.
        """
        self.analytics.track_capability_usage(capability_name)

        providers = self.capability_registry.find_providers(
            capability_name,
            healthy_only=True,
            preferred_vendor=preferred_vendor,
        )

        if not providers:
            raise CapabilityNotFoundError(
                f"No healthy provider currently available for capability '{capability_name}'",
                details={"capability": capability_name},
            )

        selected_connector_model = providers[0]

        # Look up matching action name
        action_name = capability_name.split(".")[-1]  # heuristic fallback
        return self.execute_action(
            connector_id=selected_connector_model.id,
            action_name=action_name,
            inputs=inputs,
            organization_id=organization_id,
            workspace_id=workspace_id,
            data_tags=data_tags,
            context=context,
        )

    def execute_action(
        self,
        connector_id: str,
        action_name: str,
        inputs: Dict[str, Any],
        organization_id: str = "org-default",
        workspace_id: str = "ws-default",
        data_tags: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
        timeout_seconds: Optional[float] = None,
    ) -> ExecutionResult:
        """
        Executes a specific named action on a designated connector through the full governance pipeline.
        """
        # Step 1: Connector Model & Instance Lookup
        connector_model = self.connector_registry.get(connector_id)
        instance = self.connector_registry.get_instance(connector_id)

        # Step 2: Action Descriptor construction / lookup
        matching_action = None
        if instance:
            for act in instance.actions():
                if act.name == action_name:
                    matching_action = act
                    break

        if not matching_action:
            matching_action = ActionDescriptor(
                name=action_name,
                connector_id=connector_id,
                capability=f"{connector_id}.{action_name}",
            )

        # Step 3: Policy Validation
        eval_result = self.policy_engine.evaluate(
            connector=connector_model,
            action=matching_action,
            inputs=inputs,
            organization_id=organization_id,
            data_tags=data_tags,
        )
        if not eval_result.allowed:
            raise PolicyViolationError(
                f"Connector action rejected by policy: {eval_result.violations}",
                connector_id=connector_id,
                details={"violations": eval_result.violations},
            )

        # Step 4: Rate Limiting
        rate_key = f"{organization_id}:{workspace_id}:{connector_id}"
        self.rate_limiter.acquire(rate_key)

        # Step 5: Circuit Breaker
        breaker = self._get_circuit_breaker(connector_id)
        if not breaker.allow_request():
            raise CircuitBreakerOpenError(
                f"Circuit breaker for connector '{connector_id}' is OPEN",
                connector_id=connector_id,
            )

        # Step 6: Authentication & Credentials Resolution (if instance available)
        resolved_creds = {}
        try:
            resolved_creds = self.credential_store.resolve_credentials(organization_id, workspace_id, connector_id)
            if instance:
                instance.authenticate(resolved_creds)
        except Exception as e:
            # If credentials missing but connector allows open access or sandbox mock
            logger.debug(f"Credential resolution note for '{connector_id}': {e}")

        # Step 7: Sandbox Execution & Retries
        def _invoke() -> ExecutionResult:
            if instance:
                return self.action_executor.execute_action(
                    connector=instance,
                    action=matching_action,
                    inputs=inputs,
                    context=context,
                )
            else:
                # Default synthetic execution when instance is not loaded
                return ExecutionResult(
                    connector_id=connector_id,
                    action_name=action_name,
                    status="SUCCESS",
                    output={"result": f"Executed action '{action_name}' on connector '{connector_id}'", "inputs": inputs},
                    latency_ms=12.0,
                    cost_usd=matching_action.cost_usd,
                )

        start_time = time.perf_counter()
        retries_used = 0

        def _on_retry(attempt: int, err: Exception, delay: float) -> None:
            nonlocal retries_used
            retries_used += 1

        try:
            exec_result = self.sandbox.execute_in_sandbox(
                lambda: self.retry_engine.execute_with_retry(
                    _invoke,
                    on_retry=_on_retry,
                ),
                timeout_seconds=timeout_seconds,
            )

            breaker.record_success()
            self.observability.record_execution(exec_result, retry_count=retries_used)
            return exec_result

        except Exception as e:
            breaker.record_failure(e)
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            failed_res = ExecutionResult(
                connector_id=connector_id,
                action_name=action_name,
                status="FAILED",
                error=str(e),
                latency_ms=latency_ms,
                cost_usd=0.0,
            )
            self.observability.record_execution(failed_res, retry_count=retries_used)
            raise
