"""Tests for Explainability Engine (Planner, Tool Call, Decision, Validation, Reflection)."""

from app.runtime.explainability.decision_explainer import DecisionExplainer
from app.runtime.explainability.planner_explainer import PlannerExplainer
from app.runtime.explainability.toolcall_explainer import ToolCallExplainer
from app.runtime.explainability.validation_explainer import (
    ReflectionExplainer,
    ValidationExplainer,
)


def test_planner_explainer():
    candidates = [
        {"candidate_id": "cand-flash", "model_name": "gemini-2.5-flash", "predicted_cost_usd": 0.001, "predicted_latency_ms": 300.0, "predicted_accuracy": 0.98},
        {"candidate_id": "cand-pro", "model_name": "gemini-2.5-pro", "predicted_cost_usd": 0.015, "predicted_latency_ms": 1200.0, "predicted_accuracy": 0.995},
    ]
    exp = PlannerExplainer.explain_plan_selection(
        decision_id="dec-101",
        mission_id="mission-101",
        candidates_data=candidates,
    )
    assert exp.decision_id == "dec-101"
    assert exp.selected_candidate_id == "cand-flash"
    assert len(exp.candidates) == 2
    assert exp.candidates[1].rejection_reason is not None
    assert "U(c)" in exp.mathematical_formula


def test_toolcall_explainer():
    exp = ToolCallExplainer.explain_tool_call(
        call_id="call-55",
        tool_name="specialized_table_extractor",
        intent="Extract table cells with header hierarchy",
        parameters={"table_index": 0, "grid_mode": "strict"},
    )
    assert exp.call_id == "call-55"
    assert exp.tool_name == "specialized_table_extractor"
    assert len(exp.alternatives_considered) >= 1
    assert exp.precondition_checks["input_payload_valid"] is True


def test_decision_explainer():
    exp = DecisionExplainer.explain_general_decision("dec-gen-1", "DYNAMIC_REPLAN", {})
    assert exp.decision_id == "dec-gen-1"
    assert exp.confidence_score > 0.9
    assert "doc_entropy" in exp.feature_attributions
    assert len(exp.counterfactuals) >= 2
    assert len(exp.sensitivity_curve["parameter_steps"]) > 0


def test_validation_and_reflection_explainers():
    val_rules = [
        {"rule_name": "Total Check", "passed": True, "observed_value": 100, "expected_threshold": 100},
        {"rule_name": "Tax Check", "passed": False, "observed_value": 5, "expected_threshold": 8, "deviation_percent": 37.5, "remediation_suggestion": "Re-run tax parsing sub-dag"},
    ]
    val_exp = ValidationExplainer.explain_validation("val-01", "art-hash-123", val_rules)
    assert val_exp.overall_passed is False
    assert len(val_exp.rule_explanations) == 2
    assert val_exp.rule_explanations[1].remediation_suggestion is not None

    ref_exp = ReflectionExplainer.explain_reflection(
        mutation_id="mut-01",
        policy_name="ocr_deskew_threshold",
        triggering_event="Skewed scan warning on doc #401",
        diff={"deskew_angle_tolerance": [0.5, 0.2]},
    )
    assert ref_exp.mutation_id == "mut-01"
    assert ref_exp.governance_verdict == "APPROVED"
