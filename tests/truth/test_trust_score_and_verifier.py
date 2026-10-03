"""
Tests for Trust Score, Independent Verifier, Certification, Drift & Reports (Pillars 5-10).
"""

from app.runtime.truth.benchmark_reg import ScientificBenchmarkRegistry
from app.runtime.truth.certification import CertificationTier, MissionCertifier
from app.runtime.truth.drift_detector import RuntimeDriftDetector
from app.runtime.truth.independent_verifier import IndependentVerifier
from app.runtime.truth.report_generator import ScientificReportGenerator
from app.runtime.truth.trust_score import TrustScoreEngine


def test_trust_score_calculation():
    engine = TrustScoreEngine()
    breakdown = engine.compute_trust_score(
        mission_id="msn_1001",
        telemetry={
            "evidence_quality_score": 100.0,
            "planner_stability_score": 100.0,
            "consensus_agreement_pct": 100.0,
            "validation_failures_count": 0,
            "memory_consistency_pct": 100.0,
            "policy_violations_count": 0,
            "human_corrections_count": 0,
            "replay_state_fidelity_pct": 100.0,
            "benchmark_parity_pct": 100.0,
        },
    )
    assert breakdown.composite_trust_score == 100.0
    assert breakdown.trust_grade == "AAA_ENTERPRISE_GRADE"
    assert len(breakdown.dimensions) == 9


def test_independent_verifier():
    verifier = IndependentVerifier()
    bundle = {
        "bundle_id": "b_101",
        "ledger_entries": [{"parent_event_hash": "0" * 64, "entry_hash": "0x1111"}],
        "merkle_root": "0x8f2ac31b4e5d6a7b",
        "decision_proofs": [{"proof_hash": "0xabc"}],
        "replay_state_match_rate": 0.9998,
        "signatures": ["sig_01"],
        "policy_violations_count": 0,
    }

    report = verifier.verify_bundle(bundle)
    assert report.all_passed is True
    assert report.total_checks_passed == 6
    assert report.independent_attestation_status == "CRYPTOGRAPHICALLY_VERIFIED"


def test_mission_certification_and_drift_and_reports():
    certifier = MissionCertifier()
    cert = certifier.issue_certificate("msn_1001", "invoice", trust_score=98.5, replay_fidelity=99.98)
    assert cert.tier == CertificationTier.ENTERPRISE_HIGHEST_ASSURANCE

    drift = RuntimeDriftDetector().evaluate_drift()
    assert drift.overall_system_status == "HEALTHY_STABLE"

    bench = ScientificBenchmarkRegistry().get_benchmark("bench_inv_1000")
    assert bench is not None
    assert bench.observed_accuracy == 0.994

    report_gen = ScientificReportGenerator()
    md_report = report_gen.generate_markdown_report("msn_1001", "invoice", certificate=cert)
    assert "# Scientific Execution & Audit Dossier" in md_report
    assert "ENTERPRISE_HIGHEST_ASSURANCE" in md_report
