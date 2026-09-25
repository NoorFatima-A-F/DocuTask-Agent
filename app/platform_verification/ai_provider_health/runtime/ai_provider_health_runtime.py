"""AI Provider Health Master Runtime.

Coordinates all sub-verifiers across the 15 dimensions of Phase 3H.3.8.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from datetime import datetime, timezone

from app.platform_verification.ai_provider_health.contract.ai_provider_health_contract import AIProviderHealthContractVerifier
from app.platform_verification.ai_provider_health.auth.ai_auth_verifier import AIAuthVerifier
from app.platform_verification.ai_provider_health.connectivity.ai_connectivity_verifier import AIConnectivityVerifier
from app.platform_verification.ai_provider_health.latency.ai_latency_verifier import AILatencyVerifier
from app.platform_verification.ai_provider_health.quota.ai_quota_verifier import AIQuotaVerifier
from app.platform_verification.ai_provider_health.integrity.ai_response_integrity_verifier import AIResponseIntegrityVerifier
from app.platform_verification.ai_provider_health.timeout.ai_timeout_verifier import AITimeoutVerifier
from app.platform_verification.ai_provider_health.taxonomy.ai_failure_classifier import AIFailureClassifier
from app.platform_verification.ai_provider_health.degraded.ai_degraded_mode_verifier import AIDegradedModeVerifier
from app.platform_verification.ai_provider_health.failover.ai_failover_verifier import AIFailoverVerifier
from app.platform_verification.ai_provider_health.monitoring.ai_monitoring_bridge import AIMonitoringBridge
from app.platform_verification.ai_provider_health.security.ai_security_auditor import AISecurityAuditor
from app.platform_verification.ai_provider_health.simulation.ai_failure_simulator import AIFailureSimulator
from app.platform_verification.ai_provider_health.scoring.ai_health_scorer import AIHealthScorer
from app.platform_verification.ai_provider_health.exporter.ai_evidence_exporter import AIEvidenceExporter


class AIProviderHealthRuntime:
    """Master Orchestrator for Phase 3H.3.8 AI Provider Health Verification."""

    def __init__(self, export_dir: Optional[str] = None):
        self.contract_verifier = AIProviderHealthContractVerifier()
        self.auth_verifier = AIAuthVerifier()
        self.connectivity_verifier = AIConnectivityVerifier()
        self.latency_verifier = AILatencyVerifier()
        self.quota_verifier = AIQuotaVerifier()
        self.integrity_verifier = AIResponseIntegrityVerifier()
        self.timeout_verifier = AITimeoutVerifier()
        self.failure_classifier = AIFailureClassifier()
        self.degraded_verifier = AIDegradedModeVerifier()
        self.failover_verifier = AIFailoverVerifier()
        self.monitoring_bridge = AIMonitoringBridge()
        self.security_auditor = AISecurityAuditor()
        self.failure_simulator = AIFailureSimulator()
        self.scorer = AIHealthScorer()
        self.exporter = AIEvidenceExporter(output_dir=export_dir)

    def run_full_verification(self) -> Dict[str, Any]:
        """Executes full AI Provider verification pipeline, generates scorecard, and exports manifests."""
        health_rep = self.contract_verifier.verify_provider_health()
        auth_rep = self.auth_verifier.verify_authentication()
        conn_rep = self.connectivity_verifier.verify_connectivity()
        lat_rep = self.latency_verifier.verify_latency()
        quota_rep = self.quota_verifier.verify_quota()
        integ_rep = self.integrity_verifier.verify_response_integrity()
        timeout_rep = self.timeout_verifier.verify_timeouts()
        fail_rep = self.failure_classifier.classify_failures()
        deg_rep = self.degraded_verifier.verify_degraded_mode()
        failover_rep = self.failover_verifier.verify_failover()
        mon_rep = self.monitoring_bridge.verify_monitoring_integration()
        sec_rep = self.security_auditor.audit_security()
        sim_rep = self.failure_simulator.run_simulations()

        scorecard = self.scorer.compute_scorecard(
            health_report=health_rep,
            auth_report=auth_rep,
            connectivity_report=conn_rep,
            latency_report=lat_rep,
            quota_report=quota_rep,
            integrity_report=integ_rep,
            timeout_report=timeout_rep,
            failure_report=fail_rep,
            degraded_report=deg_rep,
            failover_report=failover_rep,
            monitoring_report=mon_rep,
            security_report=sec_rep,
            simulation_report=sim_rep,
        )

        manifests = self.exporter.export_all(
            health_report=health_rep,
            auth_report=auth_rep,
            latency_report=lat_rep,
            quota_report=quota_rep,
            response_quality_report=integ_rep,
            failure_simulation_report=sim_rep,
            failover_report=failover_rep,
            scorecard=scorecard,
        )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "health_report": health_rep,
            "auth_report": auth_rep,
            "connectivity_report": conn_rep,
            "latency_report": lat_rep,
            "quota_report": quota_rep,
            "integrity_report": integ_rep,
            "timeout_report": timeout_rep,
            "failure_report": fail_rep,
            "degraded_report": deg_rep,
            "failover_report": failover_rep,
            "monitoring_report": mon_rep,
            "security_report": sec_rep,
            "simulation_report": sim_rep,
            "scorecard": scorecard,
            "exported_manifests": manifests,
            "passed": scorecard.passed,
        }
