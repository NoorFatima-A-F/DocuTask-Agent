"""Tests for Reflection and Self-Correction Loop (Phase 25.0).

Covers:
- QualityEvaluation (format, arithmetic, completeness, confidence scoring)
- Defect detection (arithmetic mismatches, missing schema fields, low confidence)
- SelfCorrectionTrigger synthesis & action routing
- ReflectionAgent apply_self_correction in-place repair
- Boundary values, thresholds, and multi-defect scenarios
"""

from __future__ import annotations

import pytest

from app.agents.reflection import (
    CorrectionAction,
    QualityEvaluation,
    ReflectionAgent,
    SelfCorrectionTrigger,
)


class TestReflectionScoring:
    @pytest.fixture
    def agent(self):
        return ReflectionAgent(quality_threshold=0.90)

    def test_perfect_invoice_output(self, agent):
        data = {
            "vendor_name": "ACME Corp",
            "invoice_number": "INV-100",
            "subtotal": 100.0,
            "tax_amount": 10.0,
            "total_amount": 110.0,
            "confidence": 0.99,
        }
        res = agent.evaluate_output("validation", data)
        assert res.passed_threshold is True
        assert res.overall_score >= 0.95
        assert len(res.detected_defects) == 0

    def test_arithmetic_mismatch_detected(self, agent):
        data = {
            "vendor_name": "ACME Corp",
            "invoice_number": "INV-100",
            "subtotal": 100.0,
            "tax_amount": 10.0,
            "total_amount": 120.0,  # Defect: 100+10 != 120
            "confidence": 0.95,
        }
        res = agent.evaluate_output("validation", data)
        assert res.passed_threshold is False
        assert res.arithmetic_score == 0.50
        assert any("Arithmetic mismatch" in d for d in res.detected_defects)

    def test_missing_mandatory_field(self, agent):
        data = {
            "invoice_number": "INV-100",
            "total_amount": 100.0,
            "confidence": 0.95,
        }  # Missing vendor_name
        res = agent.evaluate_output("extract", data)
        assert res.passed_threshold is False
        assert res.completeness_score < 1.0
        assert any("Missing mandatory fields" in d for d in res.detected_defects)

    def test_low_confidence_score_defect(self, agent):
        data = {
            "vendor_name": "ACME Corp",
            "invoice_number": "INV-100",
            "subtotal": 50.0,
            "tax_amount": 5.0,
            "total_amount": 55.0,
            "confidence": 0.70,  # Below 0.85
        }
        res = agent.evaluate_output("ocr", data)
        assert any("Low confidence extraction" in d for d in res.detected_defects)

    def test_non_numeric_amount_field(self, agent):
        data = {
            "vendor_name": "ACME Corp",
            "invoice_number": "INV-100",
            "subtotal": "one hundred dollars",
            "tax_amount": 10.0,
            "total_amount": 110.0,
        }
        res = agent.evaluate_output("validation", data)
        assert res.arithmetic_score == 0.30
        assert any("Non-numeric values found" in d for d in res.detected_defects)


class TestSelfCorrectionTriggerFormulation:
    @pytest.fixture
    def agent(self):
        return ReflectionAgent(quality_threshold=0.90)

    def test_no_action_when_passed(self, agent):
        eval_pass = QualityEvaluation(
            overall_score=0.98,
            format_score=1.0,
            arithmetic_score=1.0,
            completeness_score=1.0,
            confidence_score=0.99,
            passed_threshold=True,
        )
        trigger = agent.formulate_correction("t1", eval_pass)
        assert trigger.action == CorrectionAction.NO_ACTION

    def test_inject_repair_node_for_arithmetic_mismatch(self, agent):
        eval_fail = QualityEvaluation(
            overall_score=0.75,
            format_score=1.0,
            arithmetic_score=0.5,
            completeness_score=1.0,
            confidence_score=0.95,
            passed_threshold=False,
            detected_defects=["Arithmetic mismatch: 100+10!=120"],
            recommendations=["Recalculate total"],
        )
        trigger = agent.formulate_correction("t_math", eval_fail)
        assert trigger.action == CorrectionAction.INJECT_REPAIR_NODE
        assert trigger.suggested_alternative_agent == "agent_correction_gemini"
        assert trigger.suggested_alternative_tool == "tool_math_verifier"

    def test_switch_tool_for_low_confidence(self, agent):
        eval_fail = QualityEvaluation(
            overall_score=0.70,
            format_score=1.0,
            arithmetic_score=1.0,
            completeness_score=1.0,
            confidence_score=0.60,
            passed_threshold=False,
            detected_defects=["Low confidence extraction score: 0.60"],
            recommendations=["Switch to vision LLM"],
        )
        trigger = agent.formulate_correction("t_ocr", eval_fail)
        assert trigger.action == CorrectionAction.SWITCH_TOOL
        assert trigger.suggested_alternative_tool == "tool_gemini_vision"

    def test_reexecute_with_feedback_for_missing_fields(self, agent):
        eval_fail = QualityEvaluation(
            overall_score=0.65,
            format_score=1.0,
            arithmetic_score=1.0,
            completeness_score=0.5,
            confidence_score=0.95,
            passed_threshold=False,
            detected_defects=["Missing mandatory fields: vendor_name"],
            recommendations=["Re-extract focusing on vendor_name"],
        )
        trigger = agent.formulate_correction("t_extract", eval_fail, current_agent_id="ag_ext", current_tool_id="tl_regex")
        assert trigger.action == CorrectionAction.REEXECUTE_WITH_FEEDBACK
        assert trigger.suggested_alternative_agent == "ag_ext"
        assert trigger.suggested_alternative_tool == "tl_regex"


class TestApplySelfCorrection:
    @pytest.fixture
    def agent(self):
        return ReflectionAgent()

    def test_apply_arithmetic_correction(self, agent):
        bad_data = {
            "vendor_name": "ACME",
            "subtotal": 200.0,
            "tax_amount": 20.0,
            "total_amount": 999.0,  # wrong
        }
        trigger = SelfCorrectionTrigger(
            action=CorrectionAction.INJECT_REPAIR_NODE,
            diagnosis="Arithmetic mismatch: subtotal + tax != total",
        )
        fixed = agent.apply_self_correction(bad_data, trigger)
        assert fixed["total_amount"] == 220.0
        assert fixed["confidence"] == 0.99
        assert fixed["corrected_by_reflection"] is True

    def test_apply_missing_vendor_correction(self, agent):
        bad_data = {"invoice_number": "INV-1"}
        trigger = SelfCorrectionTrigger(
            action=CorrectionAction.REEXECUTE_WITH_FEEDBACK,
            diagnosis="Missing mandatory fields: vendor_name",
        )
        fixed = agent.apply_self_correction(bad_data, trigger)
        assert "vendor_name" in fixed
        assert "ACME" in fixed["vendor_name"]
        assert fixed["corrected_by_reflection"] is True


class TestExpandedReflectionScenarios:
    @pytest.mark.parametrize("action", [
        CorrectionAction.NO_ACTION,
        CorrectionAction.REEXECUTE_WITH_FEEDBACK,
        CorrectionAction.SWITCH_AGENT,
        CorrectionAction.SWITCH_TOOL,
        CorrectionAction.INJECT_REPAIR_NODE,
        CorrectionAction.ESCALATE_HUMAN,
    ])
    def test_all_correction_actions(self, action):
        trigger = SelfCorrectionTrigger(action=action)
        assert trigger.action == action

    def test_custom_quality_threshold(self):
        agent = ReflectionAgent(quality_threshold=0.99)
        assert agent.quality_threshold == 0.99

    def test_evaluate_empty_output_data(self):
        agent = ReflectionAgent()
        res = agent.evaluate_output("test", {})
        assert res.passed_threshold is False
        assert res.format_score == 0.0

    def test_evaluate_with_custom_schema(self):
        agent = ReflectionAgent()
        data = {"field_a": 1, "field_b": 2}
        res = agent.evaluate_output("custom", data, expected_schema=["field_a", "field_b"])
        assert res.completeness_score == 1.0

    def test_evaluate_custom_schema_missing(self):
        agent = ReflectionAgent()
        data = {"field_a": 1}
        res = agent.evaluate_output("custom", data, expected_schema=["field_a", "field_b", "field_c"])
        assert res.completeness_score == pytest.approx(1 / 3)

    def test_subtotal_zero_does_not_fail_arithmetic(self):
        agent = ReflectionAgent()
        data = {"vendor_name": "ACME", "invoice_number": "INV-1", "total_amount": 0.0, "subtotal": 0.0, "tax_amount": 0.0}
        res = agent.evaluate_output("validation", data)
        assert res.arithmetic_score == 1.0

    def test_trigger_id_unique(self):
        t1 = SelfCorrectionTrigger()
        t2 = SelfCorrectionTrigger()
        assert t1.trigger_id != t2.trigger_id
        assert t1.trigger_id.startswith("corr_")

    def test_apply_self_correction_noop_on_healthy_data(self):
        agent = ReflectionAgent()
        data = {"vendor_name": "ACME", "total_amount": 100.0}
        trigger = SelfCorrectionTrigger(action=CorrectionAction.NO_ACTION, diagnosis="All good")
        out = agent.apply_self_correction(data, trigger)
        assert out == data

    def test_float_precision_arithmetic_tolerance(self):
        agent = ReflectionAgent()
        # 0.1 + 0.2 = 0.30000000000000004 in IEEE 754
        data = {
            "vendor_name": "ACME",
            "invoice_number": "INV-1",
            "subtotal": 0.1,
            "tax_amount": 0.2,
            "total_amount": 0.3,
            "confidence": 0.95,
        }
        res = agent.evaluate_output("validation", data)
        assert res.arithmetic_score == 1.0

    def test_quality_evaluation_detected_defects_empty_on_success(self):
        agent = ReflectionAgent()
        data = {
            "vendor_name": "ACME",
            "invoice_number": "INV-1",
            "subtotal": 10.0,
            "tax_amount": 1.0,
            "total_amount": 11.0,
            "confidence": 0.95,
        }
        res = agent.evaluate_output("validation", data)
        assert res.detected_defects == []
        assert res.recommendations == []

    def test_multiple_defects_combined(self):
        agent = ReflectionAgent()
        # missing vendor AND arithmetic mismatch AND low confidence
        data = {
            "subtotal": 100.0,
            "tax_amount": 10.0,
            "total_amount": 150.0,
            "confidence": 0.50,
        }
        res = agent.evaluate_output("validation", data)
        assert len(res.detected_defects) >= 3

    @pytest.mark.parametrize("conf", [0.95, 0.90, 0.85, 0.80, 0.70])
    def test_confidence_score_scaling(self, conf):
        agent = ReflectionAgent()
        data = {"vendor_name": "ACME", "invoice_number": "INV-1", "total_amount": 10.0, "confidence": conf}
        res = agent.evaluate_output("ocr", data)
        assert res.confidence_score == conf

    def test_formulate_correction_generic_fallback(self):
        agent = ReflectionAgent()
        eval_fail = QualityEvaluation(
            overall_score=0.50,
            format_score=0.50,
            arithmetic_score=1.0,
            completeness_score=1.0,
            confidence_score=1.0,
            passed_threshold=False,
            detected_defects=["Unknown arbitrary defect"],
        )
        trigger = agent.formulate_correction("t_step", eval_fail)
        assert trigger.action == CorrectionAction.SWITCH_AGENT
        assert trigger.suggested_alternative_agent == "agent_correction_gemini"

    def test_self_correction_trigger_timestamp(self):
        t = SelfCorrectionTrigger()
        assert t.timestamp is not None

    def test_arithmetic_score_with_large_numbers(self):
        agent = ReflectionAgent()
        data = {
            "vendor_name": "MegaCorp",
            "invoice_number": "INV-MEGA",
            "subtotal": 1_000_000.00,
            "tax_amount": 100_000.00,
            "total_amount": 1_100_000.00,
            "confidence": 0.98,
        }
        res = agent.evaluate_output("validation", data)
        assert res.arithmetic_score == 1.0
        assert res.passed_threshold is True

    def test_arithmetic_mismatch_recommendation_present(self):
        agent = ReflectionAgent()
        data = {
            "vendor_name": "MegaCorp",
            "invoice_number": "INV-MEGA",
            "subtotal": 100.0,
            "tax_amount": 10.0,
            "total_amount": 200.0,
            "confidence": 0.98,
        }
        res = agent.evaluate_output("validation", data)
        assert any("Re-calculate totals" in r for r in res.recommendations)

    def test_missing_field_recommendation_present(self):
        agent = ReflectionAgent()
        data = {"subtotal": 100.0}
        res = agent.evaluate_output("extract", data, expected_schema=["vendor_name", "tax_amount"])
        assert any("Re-extract document" in r for r in res.recommendations)

    def test_negative_amounts_handled_gracefully(self):
        agent = ReflectionAgent()
        data = {
            "vendor_name": "ACME",
            "invoice_number": "INV-CREDIT",
            "subtotal": -100.0,
            "tax_amount": -10.0,
            "total_amount": -110.0,
            "confidence": 0.95,
        }
        res = agent.evaluate_output("validation", data)
        assert res.arithmetic_score == 1.0

    def test_string_numeric_conversion_valid(self):
        agent = ReflectionAgent()
        data = {
            "vendor_name": "ACME",
            "invoice_number": "INV-1",
            "subtotal": "100.00",
            "tax_amount": "10.00",
            "total_amount": "110.00",
            "confidence": "0.95",
        }
        res = agent.evaluate_output("validation", data)
        assert res.arithmetic_score == 1.0
        assert res.passed_threshold is True

    def test_empty_schema_defaults_to_standard_fields(self):
        agent = ReflectionAgent()
        data = {"total_amount": 100.0}
        res = agent.evaluate_output("extract", data, expected_schema=None)
        assert "vendor_name" in res.detected_defects[0]

    def test_apply_self_correction_retains_existing_fields(self):
        agent = ReflectionAgent()
        data = {
            "vendor_name": "ACME",
            "invoice_number": "INV-99",
            "subtotal": 50.0,
            "tax_amount": 5.0,
            "total_amount": 60.0,
            "extra_custom_field": "custom_data",
        }
        trigger = SelfCorrectionTrigger(action=CorrectionAction.NO_ACTION)
        out = agent.apply_self_correction(data, trigger)
        assert out["extra_custom_field"] == "custom_data"

    def test_confidence_boundary_zero_and_one(self):
        agent = ReflectionAgent()
        d_zero = {"vendor_name": "ACME", "invoice_number": "1", "total_amount": 1, "confidence": 0.0}
        d_one = {"vendor_name": "ACME", "invoice_number": "1", "total_amount": 1, "confidence": 1.0}
        res_zero = agent.evaluate_output("ocr", d_zero)
        res_one = agent.evaluate_output("ocr", d_one)
        assert res_zero.confidence_score == 0.0
        assert res_one.confidence_score == 1.0

    def test_quality_evaluation_repr(self):
        qe = QualityEvaluation(
            overall_score=0.95,
            format_score=1.0,
            arithmetic_score=1.0,
            completeness_score=1.0,
            confidence_score=0.95,
            passed_threshold=True,
        )
        assert qe.overall_score == 0.95
        assert qe.passed_threshold is True

    def test_apply_self_correction_vendor_when_empty_string(self):
        agent = ReflectionAgent()
        data = {"vendor_name": "", "total_amount": 100.0}
        trigger = SelfCorrectionTrigger(
            action=CorrectionAction.REEXECUTE_WITH_FEEDBACK,
            diagnosis="Missing mandatory fields: vendor_name",
        )
        out = agent.apply_self_correction(data, trigger)
        assert "ACME" in out["vendor_name"]

    def test_apply_self_correction_rounds_to_two_decimals(self):
        agent = ReflectionAgent()
        data = {"subtotal": 10.3333, "tax_amount": 1.1111, "total_amount": 99.0}
        trigger = SelfCorrectionTrigger(
            action=CorrectionAction.INJECT_REPAIR_NODE,
            diagnosis="Arithmetic mismatch: subtotal + tax != total",
        )
        out = agent.apply_self_correction(data, trigger)
        assert out["total_amount"] == 11.44

    def test_formulate_correction_preserves_task_id(self):
        agent = ReflectionAgent()
        eval_f = QualityEvaluation(
            overall_score=0.5,
            format_score=1.0,
            arithmetic_score=0.5,
            completeness_score=1.0,
            confidence_score=0.9,
            passed_threshold=False,
            detected_defects=["Arithmetic mismatch"],
        )
        trig = agent.formulate_correction("my_task_999", eval_f)
        assert trig.task_id == "my_task_999"

    def test_reflection_agent_default_threshold_is_ninety_percent(self):
        agent = ReflectionAgent()
        assert agent.quality_threshold == 0.90

