"""Tests for Phase 25.0 Goal Understanding Engine.

Covers:
- GoalSpecification creation, defaults, ambiguity checks, success criteria evaluation
- IntentClassifier pattern matching, confidence scoring, hints, and secondary intents
- ConstraintExtractor SLA, accuracy, cost, compliance frameworks, format, and PII parsing
- GoalParser end-to-end translation
- GoalManager registration, query, and lifecycle status tracking
"""

from __future__ import annotations

import pytest

from app.agents.intelligence.goal import (
    ConstraintExtractor,
    ExtractedConstraints,
    GoalManager,
    GoalParser,
    GoalPriority,
    GoalSpecification,
    GoalStatus,
    IntentClassifier,
    IntentResult,
    IntentType,
    RiskLevel,
    SuccessCriteria,
)


class TestSuccessCriteria:
    def test_gte_operator_success(self):
        sc = SuccessCriteria(metric_name="accuracy", target_value=0.90, comparison_operator=">=")
        assert sc.evaluate(0.95) is True
        assert sc.evaluate(0.90) is True

    def test_gte_operator_failure(self):
        sc = SuccessCriteria(metric_name="accuracy", target_value=0.90, comparison_operator=">=")
        assert sc.evaluate(0.85) is False

    def test_lte_operator(self):
        sc = SuccessCriteria(metric_name="latency", target_value=5.0, comparison_operator="<=")
        assert sc.evaluate(4.2) is True
        assert sc.evaluate(5.0) is True
        assert sc.evaluate(5.1) is False

    def test_eq_operator(self):
        sc = SuccessCriteria(metric_name="schema_valid", target_value=1.0, comparison_operator="==")
        assert sc.evaluate(1.0) is True
        assert sc.evaluate(0.0) is False

    def test_neq_operator(self):
        sc = SuccessCriteria(metric_name="error_count", target_value=0.0, comparison_operator="!=")
        assert sc.evaluate(1.0) is True
        assert sc.evaluate(0.0) is False


class TestGoalSpecification:
    def test_goal_specification_defaults(self):
        goal = GoalSpecification(objective="Extract invoice")
        assert goal.goal_id.startswith("goal_")
        assert goal.status == GoalStatus.PENDING
        assert goal.priority == GoalPriority.MEDIUM
        assert goal.risk_level == RiskLevel.LOW
        assert goal.is_ambiguous() is False

    def test_ambiguous_short_objective(self):
        goal = GoalSpecification(objective="abc")
        assert goal.is_ambiguous() is True

    def test_ambiguous_low_confidence(self):
        goal = GoalSpecification(objective="Process document", confidence_score=0.45)
        assert goal.is_ambiguous() is True

    def test_add_criterion(self):
        goal = GoalSpecification(objective="Process invoice document")
        goal.add_criterion("accuracy", 0.95, weight=2.0)
        assert len(goal.success_criteria) == 1
        assert goal.success_criteria[0].metric_name == "accuracy"
        assert goal.success_criteria[0].target_value == 0.95
        assert goal.success_criteria[0].weight == 2.0

    def test_evaluate_success_all_passed(self):
        goal = GoalSpecification(objective="Process invoice document")
        goal.add_criterion("accuracy", 0.90, weight=1.0, mandatory=True)
        goal.add_criterion("latency", 5.0, op="<=", weight=1.0, mandatory=False)
        passed, score = goal.evaluate_success({"accuracy": 0.95, "latency": 3.0})
        assert passed is True
        assert score == 1.0

    def test_evaluate_success_mandatory_failed(self):
        goal = GoalSpecification(objective="Process invoice document")
        goal.add_criterion("accuracy", 0.95, weight=1.0, mandatory=True)
        goal.add_criterion("latency", 5.0, op="<=", weight=1.0, mandatory=False)
        passed, score = goal.evaluate_success({"accuracy": 0.85, "latency": 2.0})
        assert passed is False
        assert score == 0.5

    def test_evaluate_success_no_criteria(self):
        goal = GoalSpecification(objective="Do something")
        passed, score = goal.evaluate_success({})
        assert passed is True
        assert score == 1.0


class TestIntentClassifier:
    @pytest.fixture
    def classifier(self):
        return IntentClassifier()

    def test_classify_empty_string(self, classifier):
        res = classifier.classify("")
        assert res.primary_intent == IntentType.GENERIC_TASK
        assert res.confidence == 0.1

    def test_classify_invoice(self, classifier):
        res = classifier.classify("Process accounts payable vendor invoice INV-100")
        assert res.primary_intent == IntentType.INVOICE_PROCESSING
        assert res.confidence >= 0.70
        assert res.domain == "FINANCIAL_DOCUMENTS"

    def test_classify_receipt(self, classifier):
        res = classifier.classify("Extract merchant receipt for meal reimbursement")
        assert res.primary_intent == IntentType.RECEIPT_ANALYSIS
        assert res.confidence >= 0.70

    def test_classify_contract(self, classifier):
        res = classifier.classify("Review legal terms, conditions, and nda agreement")
        assert res.primary_intent == IntentType.CONTRACT_REVIEW
        assert res.confidence >= 0.70

    def test_classify_compliance(self, classifier):
        res = classifier.classify("Audit regulatory compliance against gdpr and sox")
        assert res.primary_intent == IntentType.COMPLIANCE_AUDIT
        assert res.confidence >= 0.70

    def test_classify_fraud(self, classifier):
        res = classifier.classify("Check for fraud, altered amounts, and suspicious tampering")
        assert res.primary_intent == IntentType.FRAUD_DETECTION
        assert res.confidence >= 0.70

    def test_classify_batch_ingestion(self, classifier):
        res = classifier.classify("Bulk ingest all documents from inbound directory")
        assert res.primary_intent == IntentType.BATCH_INGESTION
        assert res.confidence >= 0.70

    def test_classify_reconciliation(self, classifier):
        res = classifier.classify("3-way match reconciliation between invoice and purchase order")
        assert res.primary_intent == IntentType.RECONCILIATION
        assert res.confidence >= 0.70

    def test_classify_data_transformation(self, classifier):
        res = classifier.classify("Transform and convert parquet dataset into CSV format")
        assert res.primary_intent == IntentType.DATA_TRANSFORMATION

    def test_classify_with_intent_hint_override(self, classifier):
        res = classifier.classify("Random text", context={"intent_hint": "FRAUD_DETECTION"})
        assert res.primary_intent == IntentType.FRAUD_DETECTION
        assert res.confidence >= 0.95

    def test_classify_secondary_intents(self, classifier):
        res = classifier.classify("Audit invoice compliance under regulatory SOX rules")
        assert len(res.secondary_intents) >= 1 or res.primary_intent in (
            IntentType.INVOICE_PROCESSING,
            IntentType.COMPLIANCE_AUDIT,
        )


class TestConstraintExtractor:
    @pytest.fixture
    def extractor(self):
        return ConstraintExtractor()

    def test_extract_accuracy_percentage(self, extractor):
        res = extractor.extract("Extract document with accuracy >= 98%")
        assert res.min_accuracy == 0.98

    def test_extract_accuracy_ratio(self, extractor):
        res = extractor.extract("Target precision of 0.92")
        assert res.min_accuracy == 0.92

    def test_extract_accuracy_word_percent(self, extractor):
        res = extractor.extract("Requires confidence at least 95 percent")
        assert res.min_accuracy == 0.95

    def test_extract_sla_seconds(self, extractor):
        res = extractor.extract("Process within 15 seconds")
        assert res.max_latency_seconds == 15.0

    def test_extract_sla_minutes(self, extractor):
        res = extractor.extract("Complete under 2 minutes")
        assert res.max_latency_seconds == 120.0

    def test_extract_sla_milliseconds(self, extractor):
        res = extractor.extract("Latency under 500 ms")
        assert res.max_latency_seconds == 0.5

    def test_extract_cost_budget(self, extractor):
        res = extractor.extract("Budget cap of $10")
        assert res.cost_budget_usd == 10.0

    def test_extract_output_format(self, extractor):
        res = extractor.extract("Export extracted data to parquet")
        assert res.output_format == "PARQUET"

    def test_extract_compliance_frameworks(self, extractor):
        res = extractor.extract("Ensure SOX and HIPAA compliance standards")
        assert "SOX" in res.compliance_frameworks
        assert "HIPAA" in res.compliance_frameworks

    def test_extract_human_review_flag(self, extractor):
        res = extractor.extract("Requires human in the loop approval before release")
        assert res.require_human_review is True

    def test_extract_pii_flag(self, extractor):
        res = extractor.extract("Please redact sensitive PII information")
        assert res.pii_redaction is True

    def test_extract_with_context_overrides(self, extractor):
        res = extractor.extract(
            "Default text",
            context={
                "min_accuracy": 0.99,
                "max_latency_seconds": 1.5,
                "cost_budget_usd": 0.05,
                "output_format": "XML",
                "require_human_review": True,
            },
        )
        assert res.min_accuracy == 0.99
        assert res.max_latency_seconds == 1.5
        assert res.cost_budget_usd == 0.05
        assert res.output_format == "XML"
        assert res.require_human_review is True


class TestGoalParserAndManager:
    @pytest.fixture
    def parser(self):
        return GoalParser()

    @pytest.fixture
    def manager(self):
        return GoalManager()

    def test_parse_priority_critical(self, parser):
        spec = parser.parse("URGENT: Process invoice immediately")
        assert spec.priority == GoalPriority.CRITICAL

    def test_parse_priority_high(self, parser):
        spec = parser.parse("Expedite extraction of receipt ASAP")
        assert spec.priority == GoalPriority.HIGH

    def test_parse_priority_low(self, parser):
        spec = parser.parse("Background batch scan of documents")
        assert spec.priority == GoalPriority.LOW

    def test_parse_risk_level_critical(self, parser):
        spec = parser.parse("Audit contract under SOX compliance")
        assert spec.risk_level == RiskLevel.CRITICAL

    def test_parse_success_criteria_attached(self, parser):
        spec = parser.parse("Extract invoice with accuracy >= 95% under 10 seconds")
        metric_names = [sc.metric_name for sc in spec.success_criteria]
        assert "accuracy" in metric_names
        assert "schema_validation" in metric_names
        assert "execution_latency_seconds" in metric_names

    def test_manager_submit_and_get_goal(self, manager):
        spec = manager.submit_goal("Process invoice INV-1")
        assert manager.get_goal(spec.goal_id) is not None
        assert manager.get_goal(spec.goal_id).objective == "Process invoice INV-1"

    def test_manager_list_goals_by_status(self, manager):
        spec1 = manager.submit_goal("Goal 1")
        spec2 = manager.submit_goal("Goal 2")
        manager.update_status(spec1.goal_id, GoalStatus.IN_PROGRESS)
        manager.update_status(spec2.goal_id, GoalStatus.READY)

        in_prog = manager.list_goals(GoalStatus.IN_PROGRESS)
        assert len(in_prog) == 1
        assert in_prog[0].goal_id == spec1.goal_id

    def test_manager_evaluate_goal(self, manager):
        spec = manager.submit_goal("Extract invoice with accuracy >= 90%")
        passed, score = manager.evaluate_goal(spec.goal_id, {"accuracy": 0.95, "schema_validation": 1.0})
        assert passed is True
        assert spec.status == GoalStatus.COMPLETED

    def test_manager_evaluate_goal_failure(self, manager):
        spec = manager.submit_goal("Extract invoice with accuracy >= 95%")
        passed, score = manager.evaluate_goal(spec.goal_id, {"accuracy": 0.80, "schema_validation": 1.0})
        assert passed is False
        assert spec.status == GoalStatus.FAILED
