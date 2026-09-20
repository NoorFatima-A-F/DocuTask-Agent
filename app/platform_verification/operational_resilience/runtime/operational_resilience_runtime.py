"""
Phase 3H.7: Enterprise Operational Resilience Verification Runtime Orchestrator
"""
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from app.platform_verification.operational_resilience.verifiers.resilience_architecture_verifier import ResilienceArchitectureVerifier
from app.platform_verification.operational_resilience.verifiers.circuit_breaker_verifier import CircuitBreakerVerifier
from app.platform_verification.operational_resilience.verifiers.retry_strategy_verifier import RetryStrategyVerifier
from app.platform_verification.operational_resilience.verifiers.graceful_degradation_verifier import GracefulDegradationVerifier
from app.platform_verification.operational_resilience.verifiers.bulkhead_isolation_verifier import BulkheadIsolationVerifier
from app.platform_verification.operational_resilience.verifiers.load_shedding_verifier import LoadSheddingVerifier
from app.platform_verification.operational_resilience.verifiers.self_healing_verifier import SelfHealingVerifier
from app.platform_verification.operational_resilience.verifiers.chaos_resilience_verifier import ChaosResilienceVerifier
from app.platform_verification.operational_resilience.verifiers.business_continuity_verifier import BusinessContinuityVerifier
from app.platform_verification.operational_resilience.verifiers.resilience_metrics_verifier import ResilienceMetricsVerifier
from app.platform_verification.operational_resilience.scoring.operational_resilience_scorer import OperationalResilienceScorer
from app.platform_verification.operational_resilience.exporter.operational_resilience_exporter import OperationalResilienceExporter

logger = logging.getLogger("operational_resilience.runtime")


class OperationalResilienceRuntime:
    """
    Main runtime orchestrator for Phase 3H.7 Operational Resilience Verification Framework.
    """

    def __init__(self, output_dir: Optional[Path] = None):
        self.arch_verifier = ResilienceArchitectureVerifier()
        self.cb_verifier = CircuitBreakerVerifier()
        self.retry_verifier = RetryStrategyVerifier()
        self.degrade_verifier = GracefulDegradationVerifier()
        self.bulkhead_verifier = BulkheadIsolationVerifier()
        self.load_shedding_verifier = LoadSheddingVerifier()
        self.self_healing_verifier = SelfHealingVerifier()
        self.chaos_verifier = ChaosResilienceVerifier()
        self.continuity_verifier = BusinessContinuityVerifier()
        self.metrics_verifier = ResilienceMetricsVerifier()
        self.scorer = OperationalResilienceScorer()
        self.exporter = OperationalResilienceExporter(output_dir=output_dir)

    def run_full_verification(self, export_evidence: bool = True) -> Dict[str, Any]:
        logger.info("Starting Phase 3H.7 Enterprise Operational Resilience Verification Suite...")

        # 1. Execute all 10 Verifiers
        arch_report = self.arch_verifier.verify_resilience_architecture()
        cb_report = self.cb_verifier.verify_circuit_breakers()
        retry_report = self.retry_verifier.verify_retry_strategies()
        degrade_report = self.degrade_verifier.verify_graceful_degradation()
        bulkhead_report = self.bulkhead_verifier.verify_bulkhead_isolation()
        shed_report = self.load_shedding_verifier.verify_load_shedding()
        self_healing_report = self.self_healing_verifier.verify_self_healing_capabilities()
        chaos_report = self.chaos_verifier.execute_chaos_validation()
        continuity_report = self.continuity_verifier.verify_business_continuity()
        metrics_report = self.metrics_verifier.collect_resilience_metrics()

        # 2. Scorecard Calculation
        scorecard = self.scorer.calculate_scorecard(
            arch_report=arch_report,
            cb_report=cb_report,
            retry_report=retry_report,
            degrade_report=degrade_report,
            bulkhead_report=bulkhead_report,
            shed_report=shed_report,
            self_healing_report=self_healing_report,
            chaos_report=chaos_report,
            continuity_report=continuity_report,
            metrics_report=metrics_report,
        )

        export_metadata = None
        if export_evidence:
            export_metadata = self.exporter.export_all(
                arch_report=arch_report,
                cb_report=cb_report,
                retry_report=retry_report,
                degrade_report=degrade_report,
                bulkhead_report=bulkhead_report,
                shed_report=shed_report,
                self_healing_report=self_healing_report,
                chaos_report=chaos_report,
                continuity_report=continuity_report,
                metrics_report=metrics_report,
                scorecard=scorecard,
            )

        logger.info(
            f"Phase 3H.7 Verification Complete. Score: {scorecard.overall_resilience_score}% "
            f"({scorecard.certification_tier.value}). Passed: {scorecard.passed}"
        )

        return {
            "scorecard": scorecard,
            "architecture_report": arch_report,
            "circuit_breaker_report": cb_report,
            "retry_strategy_report": retry_report,
            "graceful_degradation_report": degrade_report,
            "bulkhead_report": bulkhead_report,
            "load_shedding_report": shed_report,
            "self_healing_report": self_healing_report,
            "chaos_resilience_report": chaos_report,
            "business_continuity_report": continuity_report,
            "resilience_metrics_report": metrics_report,
            "export_metadata": export_metadata,
        }
