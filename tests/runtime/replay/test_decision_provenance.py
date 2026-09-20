"""
Unit Tests for Decision Provenance Engine and 100% Coverage Guarantees.
"""

import pytest
from app.runtime.decision.provenance_engine import DecisionProvenanceEngine
from app.runtime.decision.utility_breakdown import PlanUtilityScore, MultiObjectiveUtilityCalculator
from app.runtime.decision.decision_engine import MasterDecisionEngine


def test_decision_record_creation_and_explainability():
    alts = [
        PlanUtilityScore(
            plan_name="Turbo Cloud OCR",
            total_utility=0.82,
            accuracy_score=0.85,
            latency_score=0.95,
            cost_score=0.70,
            risk_score=0.80,
            rejection_reason="Higher API cost per document ($0.012 > $0.005 budget)",
        ),
        PlanUtilityScore(
            plan_name="Local Tesseract OCR",
            total_utility=0.71,
            accuracy_score=0.70,
            latency_score=0.60,
            cost_score=0.99,
            risk_score=0.55,
            rejection_reason="Unacceptable accuracy drop on distorted tables",
        ),
    ]

    dec = DecisionProvenanceEngine.create_decision(
        decision_id="dec_01",
        mission_id="mission_prov_01",
        goal="Select OCR Extraction Architecture",
        selected_plan="Hybrid Local/Cloud Adaptive OCR",
        why_chosen="Dominates candidate Pareto frontier with optimal accuracy-to-cost ratio",
        alternative_plans=alts,
        utility_scores={"composite": 0.94, "accuracy": 0.96, "latency": 0.90, "cost": 0.95},
        constraints=["Max latency < 1000ms", "Accuracy > 0.95"],
        evidence_ids=["evi_raster_scan_01", "evi_confidence_metric"],
    )

    assert dec.decision_id == "dec_01"
    assert dec.decision_hash is not None
    assert len(dec.decision_hash) == 64
    assert "Turbo Cloud OCR" in dec.why_not_others
    assert "evi_raster_scan_01" in dec.based_on


def test_decision_provenance_coverage_metric():
    engine = MasterDecisionEngine()

    dec1 = DecisionProvenanceEngine.create_decision(
        decision_id="d1",
        mission_id="mission_cov_01",
        goal="Goal 1",
        selected_plan="Plan A",
        why_chosen="Optimal Pareto",
    )
    engine.record_decision(dec1)

    cov = engine.evaluate_coverage("mission_cov_01")
    assert cov.total_decisions == 1
    assert cov.provenance_coverage_ratio == 1.0
    assert cov.is_fully_explainable is True
