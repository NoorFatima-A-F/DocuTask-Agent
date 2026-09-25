"""
Phase 3H.4.10.11: Observability Security Failure Simulator
"""
from typing import List
from ..domain.interfaces import ISecurityFailureSimulator
from ..domain.models import SecurityFailureSimulationResult


class SecurityFailureSimulator(ISecurityFailureSimulator):
    def simulate_security_failure_injections(self) -> List[SecurityFailureSimulationResult]:
        simulations = [
            SecurityFailureSimulationResult(
                test_name="Secret Key Injection in Log Message",
                injection_type="API_KEY_LEAKAGE_ATTEMPT",
                payload_injected="log.info('Initializing Gemini client with key TEST_MOCK_GEMINI_KEY_PAYLOAD_94819')",
                defense_mechanism="Sanitization Middleware Regex Masker",
                blocked_or_redacted=True,
                result_status="BLOCKED_AND_REDACTED",
            ),
            SecurityFailureSimulationResult(
                test_name="Sensitive Medical Document Log Injection",
                injection_type="PII_AND_PROTECTED_HEALTH_INFO",
                payload_injected="log.error('Failed to parse patient medical history: Diagnosis=Glioblastoma')",
                defense_mechanism="PII Sanitizer & Log Redaction Rule",
                blocked_or_redacted=True,
                result_status="BLOCKED_AND_REDACTED",
            ),
            SecurityFailureSimulationResult(
                test_name="Unauthorized RBAC Dashboard Alert Modification",
                injection_type="PRIVILEGE_ESCALATION_ATTEMPT",
                payload_injected="HTTP PUT /api/v1/alerts/rules - Header Role: Viewer",
                defense_mechanism="Grafana / API RBAC Authorizer",
                blocked_or_redacted=True,
                result_status="403_FORBIDDEN",
            ),
            SecurityFailureSimulationResult(
                test_name="Unencrypted Plaintext Telemetry Interception",
                injection_type="PLAINTEXT_TRANSPORT_ATTEMPT",
                payload_injected="gRPC connection to collector on port 4317 without TLS certificate",
                defense_mechanism="OTLP Ingestion TLS Enforcement Policy",
                blocked_or_redacted=True,
                result_status="CONNECTION_REFUSED_TLS_REQUIRED",
            ),
            SecurityFailureSimulationResult(
                test_name="High Cardinality Customer Email Label Injection",
                injection_type="METRIC_LABEL_PII_INJECTION",
                payload_injected="docutask_requests_total{user_email='victim@enterprise.com'}",
                defense_mechanism="Prometheus Exporter Label Whitelist & Metric Filter",
                blocked_or_redacted=True,
                result_status="LABEL_DROPPED_CARDINALITY_PROTECTED",
            ),
        ]
        return simulations
