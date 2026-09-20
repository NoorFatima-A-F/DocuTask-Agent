"""
Comprehensive Unit and Integration Tests for Phase 3H.5: Enterprise Health Intelligence, Diagnosis & Automated Remediation.
"""
import os
import json
import pytest
from app.platform_verification.enterprise_health_intelligence.domain.models import (
    HealthEventType,
    FailureCategory,
    RemediationRiskLevel,
    IntelligenceCertificationTier,
)
from app.platform_verification.enterprise_health_intelligence.verifiers.health_event_architecture_verifier import (
    HealthEventArchitectureVerifier,
)
from app.platform_verification.enterprise_health_intelligence.verifiers.failure_classification_engine import (
    FailureClassificationEngine,
)
from app.platform_verification.enterprise_health_intelligence.verifiers.health_signal_correlation_engine import (
    HealthSignalCorrelationEngine,
)
from app.platform_verification.enterprise_health_intelligence.verifiers.root_cause_analysis_verifier import (
    RootCauseAnalysisVerifier,
)
from app.platform_verification.enterprise_health_intelligence.verifiers.remediation_decision_engine import (
    RemediationDecisionEngine,
)
from app.platform_verification.enterprise_health_intelligence.verifiers.recovery_execution_verifier import (
    RecoveryExecutionVerifier,
)
from app.platform_verification.enterprise_health_intelligence.verifiers.self_healing_validator import (
    SelfHealingValidator,
)
from app.platform_verification.enterprise_health_intelligence.verifiers.remediation_safety_verifier import (
    RemediationSafetyVerifier,
)
from app.platform_verification.enterprise_health_intelligence.verifiers.health_observability_verifier import (
    HealthObservabilityVerifier,
)
from app.platform_verification.enterprise_health_intelligence.verifiers.chaos_intelligence_validator import (
    ChaosIntelligenceValidator,
)
from app.platform_verification.enterprise_health_intelligence.scoring.health_intelligence_scorer import (
    HealthIntelligenceScorer,
)
from app.platform_verification.enterprise_health_intelligence.runtime.health_intelligence_runtime import (
    HealthIntelligenceRuntime,
)


class TestEnterpriseHealthIntelligence:
    """Test suite for validating Enterprise Health Intelligence, Diagnosis & Remediation components."""

    def test_health_event_architecture_verifier(self):
        verifier = HealthEventArchitectureVerifier()
        report = verifier.verify_event_architecture()
        assert report.total_events_captured >= 7
        assert report.architecture_valid is True
        assert len(report.supported_event_types) == 7
        types = [e.type for e in report.events]
        assert HealthEventType.SERVICE_DOWN in types
        assert HealthEventType.DEPENDENCY_FAILURE in types
        assert HealthEventType.HIGH_LATENCY in types
        assert HealthEventType.RESOURCE_EXHAUSTION in types
        assert HealthEventType.QUEUE_OVERFLOW in types
        assert HealthEventType.WORKER_FAILURE in types
        assert HealthEventType.AI_PROVIDER_FAILURE in types

    def test_failure_classification_engine(self):
        engine = FailureClassificationEngine()
        report = engine.classify_failures()
        assert report.total_classified_events >= 7
        assert report.classification_accuracy_pct >= 95.0
        assert report.classification_valid is True
        cats = [c.failure_type for c in report.classifications]
        assert FailureCategory.INFRASTRUCTURE_FAILURE in cats
        assert FailureCategory.DEPENDENCY_FAILURE in cats
        assert FailureCategory.APPLICATION_FAILURE in cats
        assert FailureCategory.AI_SYSTEM_FAILURE in cats

    def test_health_signal_correlation_engine(self):
        engine = HealthSignalCorrelationEngine()
        report = engine.correlate_signals()
        assert report.total_correlated_incidents >= 3
        assert report.noise_reduction_pct >= 50.0
        assert report.correlation_valid is True
        for inc in report.incidents:
            assert len(inc.raw_signals) >= 3
            assert len(inc.dependency_chain) >= 2

    def test_root_cause_analysis_verifier(self):
        verifier = RootCauseAnalysisVerifier()
        report = verifier.verify_rca()
        assert report.total_rcas_performed >= 3
        assert report.mean_confidence_score >= 0.95
        assert report.rca_valid is True
        for r in report.results:
            assert len(r.evidence) >= 3
            assert len(r.affected_services) >= 2

    def test_remediation_decision_engine(self):
        engine = RemediationDecisionEngine()
        report = engine.generate_remediation_decisions()
        assert report.total_decisions >= 8
        assert report.safety_classification_enforced is True
        risks = [d.risk_level for d in report.decisions]
        assert RemediationRiskLevel.SAFE_AUTOMATIC in risks
        assert RemediationRiskLevel.RISKY_APPROVAL_REQUIRED in risks
        assert RemediationRiskLevel.DANGEROUS_FORBIDDEN in risks

    def test_recovery_execution_verifier(self):
        verifier = RecoveryExecutionVerifier()
        report = verifier.verify_recovery_execution()
        assert report.total_recovery_scenarios >= 4
        assert report.all_recoveries_successful is True
        assert report.recovery_success_rate_pct == 100.0
        for s in report.steps:
            assert s.success is True
            assert "HEALTHY" in s.service_state_post_action

    def test_self_healing_validator(self):
        validator = SelfHealingValidator()
        report = validator.validate_self_healing_lifecycle()
        assert len(report.scenarios) == 4
        assert report.self_healing_certified is True
        assert report.automatic_recovery_success_rate == 100.0
        assert report.mean_time_to_detection_seconds <= 5.0
        assert report.mean_time_to_recovery_seconds <= 30.0
        assert report.false_recovery_rate_pct == 0.0

    def test_remediation_safety_verifier(self):
        verifier = RemediationSafetyVerifier()
        report = verifier.verify_remediation_safety()
        assert report.least_privilege_enforced is True
        assert report.audit_trail_immutable is True
        assert report.rollback_supported is True
        assert report.forbidden_actions_blocked is True
        assert report.security_score_pct == 100.0

    def test_health_observability_verifier(self):
        verifier = HealthObservabilityVerifier()
        report = verifier.verify_observability_dashboards()
        assert len(report.dashboards) == 3
        assert report.all_dashboards_active is True

    def test_chaos_intelligence_validator(self):
        validator = ChaosIntelligenceValidator()
        report = validator.run_chaos_validation()
        assert len(report.tests) == 4
        assert report.all_chaos_tests_passed is True
        for t in report.tests:
            assert t.recovery_succeeded is True
            assert t.diagnosis_accuracy_pct >= 95.0

    def test_health_intelligence_scorer(self):
        runtime = HealthIntelligenceRuntime()
        results = runtime.run_full_verification()
        scorecard = results["scorecard"]

        assert scorecard.composite_score >= 95.0
        assert scorecard.tier == IntelligenceCertificationTier.AUTONOMOUS_RELIABILITY_READY
        assert scorecard.certified_enterprise_ready is True

    def test_full_runtime_and_export(self, tmp_path):
        out_dir = str(tmp_path / "health_intelligence_verification")
        runtime = HealthIntelligenceRuntime()
        results = runtime.run_full_verification(output_dir=out_dir)

        assert results["composite_score"] >= 95.0
        assert results["certified"] is True
        assert len(results["exported_files"]) == 10

        for file_path in results["exported_files"]:
            assert os.path.exists(file_path)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)
