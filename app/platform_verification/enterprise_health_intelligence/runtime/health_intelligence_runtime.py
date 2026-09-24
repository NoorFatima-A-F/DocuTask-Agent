"""
Phase 3H.5: Enterprise Health Intelligence Runtime
"""
from typing import Dict, Any
from ..verifiers import (
    HealthEventArchitectureVerifier,
    FailureClassificationEngine,
    HealthSignalCorrelationEngine,
    RootCauseAnalysisVerifier,
    RemediationDecisionEngine,
    RecoveryExecutionVerifier,
    SelfHealingValidator,
    RemediationSafetyVerifier,
    HealthObservabilityVerifier,
    ChaosIntelligenceValidator,
)
from ..scoring.health_intelligence_scorer import HealthIntelligenceScorer
from ..exporter.health_intelligence_exporter import HealthIntelligenceExporter


class HealthIntelligenceRuntime:
    def __init__(self):
        self.event_verifier = HealthEventArchitectureVerifier()
        self.classification_engine = FailureClassificationEngine()
        self.correlation_engine = HealthSignalCorrelationEngine()
        self.rca_verifier = RootCauseAnalysisVerifier()
        self.remediation_engine = RemediationDecisionEngine()
        self.recovery_verifier = RecoveryExecutionVerifier()
        self.self_healing_validator = SelfHealingValidator()
        self.safety_verifier = RemediationSafetyVerifier()
        self.observability_verifier = HealthObservabilityVerifier()
        self.chaos_validator = ChaosIntelligenceValidator()
        self.scorer = HealthIntelligenceScorer()
        self.exporter = HealthIntelligenceExporter()

    def run_full_verification(
        self, output_dir: str = "health_intelligence_verification"
    ) -> Dict[str, Any]:
        event_report = self.event_verifier.verify_event_architecture()
        class_report = self.classification_engine.classify_failures()
        corr_report = self.correlation_engine.correlate_signals()
        rca_report = self.rca_verifier.verify_rca()
        remed_report = self.remediation_engine.generate_remediation_decisions()
        recov_report = self.recovery_verifier.verify_recovery_execution()
        self_heal_report = self.self_healing_validator.validate_self_healing_lifecycle()
        safety_report = self.safety_verifier.verify_remediation_safety()
        obs_report = self.observability_verifier.verify_observability_dashboards()
        chaos_report = self.chaos_validator.run_chaos_validation()

        scorecard = self.scorer.calculate_scorecard(
            event_report=event_report,
            class_report=class_report,
            corr_report=corr_report,
            rca_report=rca_report,
            remed_report=remed_report,
            recov_report=recov_report,
            self_heal_report=self_heal_report,
            safety_report=safety_report,
            obs_report=obs_report,
            chaos_report=chaos_report,
        )

        exported_files = self.exporter.export_evidence_manifests(
            output_dir=output_dir,
            event_report=event_report,
            class_report=class_report,
            corr_report=corr_report,
            rca_report=rca_report,
            remed_report=remed_report,
            recov_report=recov_report,
            self_heal_report=self_heal_report,
            chaos_report=chaos_report,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "event_report": event_report,
            "class_report": class_report,
            "corr_report": corr_report,
            "rca_report": rca_report,
            "remed_report": remed_report,
            "recov_report": recov_report,
            "self_heal_report": self_heal_report,
            "safety_report": safety_report,
            "obs_report": obs_report,
            "chaos_report": chaos_report,
            "exported_files": exported_files,
            "composite_score": scorecard.composite_score,
            "tier": scorecard.tier.value,
            "certified": scorecard.certified_enterprise_ready,
        }
