"""
Unit and Integration Tests for Scientific Certification Packages & Autonomous Research (ASVSP Pillar 10).
"""

from app.runtime.certification import (
    CertificationPackageBuilder,
)
from app.runtime.research import (
    AutonomousResearchEngine,
)


def test_certification_package_builder():
    builder = CertificationPackageBuilder()
    pkg = builder.build_package(
        package_id="CERT-2026-TEST",
        target_policy_version="v5.0.0",
        empirical_accuracy=0.97,
        empirical_p95_latency_ms=450.0,
        brier_calibration_score=0.015,
        psi_drift_score=0.03,
        total_validated_trials=500,
    )
    assert pkg.is_statistically_sound is True
    assert pkg.package_signature.startswith("ED25519_SIG_")
    assert len(pkg.verification_hash) == 64


def test_autonomous_research_engine():
    engine = AutonomousResearchEngine()
    hypotheses = engine.generate_hypotheses(p95_latency_ms=1200.0, avg_cost_usd=0.01, ocr_confidence=0.75)
    assert len(hypotheses) == 3

    sample = engine.select_exploration_candidate()
    assert "selected_arm" in sample
    assert len(sample["arm_statistics"]) == 4

    val_res = engine.validate_candidate("CAND-01", predicted_accuracy=0.95, predicted_latency_ms=600.0, predicted_cost_usd=0.002)
    assert val_res["is_safe_for_canary"] is True
