"""Comprehensive Unit and Integration Tests for Phase 3H.4.8 — Alert Fatigue Prevention & Signal Optimization."""

import json
import os
import pytest

from app.platform_verification.alert_fatigue_verification.domain.models import (
    AlertIntelligenceTier,
)
from app.platform_verification.alert_fatigue_verification.verifiers.fatigue_architecture_verifier import (
    FatigueArchitectureVerifier,
)
from app.platform_verification.alert_fatigue_verification.verifiers.alert_deduplication_verifier import (
    AlertDeduplicationVerifier,
)
from app.platform_verification.alert_fatigue_verification.verifiers.alert_correlation_verifier import (
    AlertCorrelationVerifier,
)
from app.platform_verification.alert_fatigue_verification.verifiers.severity_optimization_verifier import (
    SeverityOptimizationVerifier,
)
from app.platform_verification.alert_fatigue_verification.verifiers.alert_routing_verifier import (
    AlertRoutingVerifier,
)
from app.platform_verification.alert_fatigue_verification.verifiers.alert_suppression_verifier import (
    AlertSuppressionVerifier,
)
from app.platform_verification.alert_fatigue_verification.verifiers.alert_grouping_verifier import (
    AlertGroupingVerifier,
)
from app.platform_verification.alert_fatigue_verification.verifiers.noise_metrics_verifier import (
    NoiseMetricsVerifier,
)
from app.platform_verification.alert_fatigue_verification.verifiers.alert_storm_simulator import (
    AlertStormSimulator,
)
from app.platform_verification.alert_fatigue_verification.verifiers.machine_prioritization_verifier import (
    MachinePrioritizationVerifier,
)
from app.platform_verification.alert_fatigue_verification.scoring.alert_fatigue_scorer import (
    AlertFatigueScorer,
)
from app.platform_verification.alert_fatigue_verification.runtime.alert_fatigue_verification_runtime import (
    AlertFatigueVerificationRuntime,
)


class TestAlertFatigueVerification:
    """Test suite for validating Enterprise Alert Fatigue Prevention & Signal Optimization components."""

    def test_fatigue_architecture_verification(self):
        """3H.4.8.1: Verify signal processing pipeline architecture and active filtering layers."""
        verifier = FatigueArchitectureVerifier()
        report = verifier.verify_architecture()
        assert report.status == "PASS"
        assert len(report.pipeline_stages) >= 7
        assert report.signal_processing_active is True
        assert report.deduplication_active is True
        assert report.correlation_active is True

    def test_alert_deduplication(self):
        """3H.4.8.2: Verify cross-service deduplication of identical error patterns within sliding time windows."""
        verifier = AlertDeduplicationVerifier()
        report = verifier.verify_deduplication()
        assert report.status == "PASS"
        assert report.total_duplicate_scenarios >= 4
        assert report.deduplication_accuracy_percentage == 100.0
        for s in report.scenarios:
            assert s.deduplicated_to_single_group is True

    def test_alert_correlation_and_root_cause(self):
        """3H.4.8.3: Verify dependency graph traversal and causal root-cause deduction."""
        verifier = AlertCorrelationVerifier()
        report = verifier.verify_correlation()
        assert report.status == "PASS"
        assert report.scenarios_evaluated == 3
        assert report.root_cause_accuracy_percentage == 100.0
        for s in report.scenarios:
            assert s.accuracy_matched is True
            assert len(s.symptom_alerts) > 0

    def test_severity_optimization(self):
        """3H.4.8.4: Verify multi-factor severity assignment (Impact x Criticality x Duration)."""
        verifier = SeverityOptimizationVerifier()
        report = verifier.verify_severity_optimization()
        assert report.status == "PASS"
        assert report.misclassification_count == 0
        assert report.critical_p1_count > 0
        assert report.severity_accuracy_percentage == 100.0

    def test_alert_routing_and_escalation(self):
        """3H.4.8.5: Verify team ownership mapping and escalation timeout SLAs."""
        verifier = AlertRoutingVerifier()
        report = verifier.verify_routing()
        assert report.status == "PASS"
        assert report.total_routing_policies == 4
        assert report.routing_accuracy_percentage == 100.0
        for p in report.policies:
            assert p.verified is True

    def test_alert_suppression_and_safety_bypass(self):
        """3H.4.8.6: Verify planned maintenance window suppression with critical safety bypass."""
        verifier = AlertSuppressionVerifier()
        report = verifier.verify_suppression()
        assert report.status == "PASS"
        assert report.safety_overrides_functional is True
        for r in report.rules:
            assert r.safety_override_verified is True

    def test_alert_grouping_and_compression(self):
        """3H.4.8.7: Verify high-volume alert grouping (500 raw alerts to 5 consolidated incidents)."""
        verifier = AlertGroupingVerifier()
        report = verifier.verify_grouping()
        assert report.status == "PASS"
        assert report.raw_alerts_ingested == 500
        assert report.consolidated_incidents_created == 5
        assert report.compression_ratio >= 0.95

    def test_alert_noise_metrics(self):
        """3H.4.8.8: Verify noise ratio (< 20%), actionable ratio (> 80%), and duplicate reduction (> 50%)."""
        verifier = NoiseMetricsVerifier()
        report = verifier.verify_noise_metrics()
        assert report.status == "PASS"
        assert report.noise_ratio < 0.20
        assert report.actionable_ratio > 0.80
        assert report.duplicate_reduction_ratio > 0.50
        assert report.targets_met is True

    def test_alert_storm_simulation(self):
        """3H.4.8.9: Verify high-throughput stress simulation under 10,000 alert events."""
        simulator = AlertStormSimulator()
        report = simulator.simulate_alert_storm()
        assert report.status == "PASS"
        assert report.events_injected == 10000
        assert report.pipeline_crashed is False
        assert report.critical_signals_preserved is True
        assert report.primary_incidents_created > 0

    def test_machine_assisted_prioritization(self):
        """3H.4.8.10: Verify explainable 0-100 ML-assisted priority scoring with deterministic fallback."""
        verifier = MachinePrioritizationVerifier()
        report = verifier.verify_machine_prioritization()
        assert report.status == "PASS"
        assert report.explainability_verified is True
        assert report.deterministic_fallback_verified is True
        assert report.avg_priority_score > 80.0

    def test_quality_scorecard_calculation(self):
        """3H.4.8.11: Verify 6-category weighted quality scorecard and certification tier."""
        runtime = AlertFatigueVerificationRuntime()
        scorecard, _ = runtime.execute_full_verification()
        assert scorecard.overall_score >= 95.0
        assert scorecard.certification_tier == AlertIntelligenceTier.ENTERPRISE_ALERT_INTELLIGENCE_READY
        assert scorecard.passed is True
        assert scorecard.deduplication_accuracy_score == 100.0
        assert scorecard.correlation_quality_score == 100.0

    def test_evidence_exporter_and_manifests(self, tmp_path):
        """3H.4.8.12: Verify export of all 12 JSON evidence manifests."""
        runtime = AlertFatigueVerificationRuntime(output_dir=str(tmp_path))
        scorecard, manifests = runtime.execute_full_verification()
        assert scorecard.passed is True
        assert len(manifests) == 12

        expected_files = [
            "architecture_report.json",
            "deduplication_report.json",
            "correlation_report.json",
            "severity_report.json",
            "routing_report.json",
            "suppression_report.json",
            "grouping_report.json",
            "noise_metrics_report.json",
            "storm_test_report.json",
            "intelligence_report.json",
            "certification_report.json",
            "metadata.json",
        ]

        for fname in expected_files:
            fpath = tmp_path / fname
            assert fpath.exists(), f"Missing manifest: {fname}"
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)
