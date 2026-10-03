"""
Tests for Reflection Engine, Critic Engine, Evaluation Engine, Confidence Engine, and Human Escalation.
"""

from app.agents.confidence.confidence_engine import ConfidenceEngine
from app.agents.critic.critic_engine import CriticEngine
from app.agents.evaluation.evaluation_engine import EvaluationEngine
from app.agents.human.escalation_engine import (
    EscalationReason,
    EscalationStatus,
    HumanEscalationEngine,
)
from app.agents.reflection.reflection_engine import ReflectionEngine


def test_reflection_engine_summary_generation():
    engine = ReflectionEngine()
    success_outcome = {"status": "SUCCESS", "extracted_fields": 15}

    report = engine.reflect_on_execution(
        agent_id="agent-123",
        task_id="task-456",
        execution_outcome=success_outcome,
    )

    assert report.quality_score >= 0.9
    assert len(report.success_factors) > 0
    assert len(report.memory_update_recommendations) > 0
    assert report.memory_update_recommendations[0]["tier"] == "PROCEDURAL"


def test_critic_engine_independent_evaluation():
    critic = CriticEngine()

    # Incomplete output test
    incomplete_output = {"vendor": "Acme"}
    report_bad = critic.evaluate(
        output=incomplete_output,
        required_fields=["vendor", "total_amount", "tax_id"],
        evidence=[],
    )
    assert not report_bad.is_approved
    assert len(report_bad.issues) >= 2

    # Complete output with evidence
    complete_output = {"vendor": "Acme", "total_amount": 150.0, "tax_id": "TAX-99"}
    evidence = [{"source": "invoice.pdf", "supports": True}]
    report_good = critic.evaluate(
        output=complete_output,
        required_fields=["vendor", "total_amount", "tax_id"],
        evidence=evidence,
    )
    assert report_good.is_approved
    assert report_good.score >= 0.8


def test_confidence_engine_and_human_escalation():
    conf_engine = ConfidenceEngine(confidence_threshold=0.80)
    esc_engine = HumanEscalationEngine()

    # High risk / low confidence scenario
    val_results = {"is_valid": False, "passed_rules_ratio": 0.4}
    conf_report = conf_engine.calculate_confidence(
        validation_results=val_results,
        evidence_items=[],
        financial_impact_usd=15000.0,
    )

    assert conf_report.requires_human_review
    assert conf_report.confidence_score < 0.80

    # Human Escalation Engine
    reason = esc_engine.should_escalate(
        confidence_score=conf_report.confidence_score,
        risk_score=conf_report.risk_score,
        financial_amount=15000.0,
    )
    assert reason in [EscalationReason.HIGH_FINANCIAL_IMPACT, EscalationReason.LOW_CONFIDENCE, EscalationReason.SECURITY_RISK]

    ticket = esc_engine.create_escalation(
        agent_id="agent-finance",
        task_id="task-disbursement",
        reason=reason,
        description="High amount payment requires manager approval",
    )
    assert ticket.status == EscalationStatus.PENDING

    resolved = esc_engine.resolve(ticket.id, approved=True, reviewer_id="mgr-alice", comments="Approved disbursement")
    assert resolved.status == EscalationStatus.APPROVED
    assert resolved.assigned_reviewer == "mgr-alice"


def test_evaluation_engine_metrics_and_grading():
    evaluator = EvaluationEngine()
    metrics = evaluator.evaluate(
        accuracy=0.96,
        latency_ms=85.0,
        cost_usd=0.015,
        confidence=0.94,
        risk=0.1,
        coverage=1.0,
        consistency=0.98,
        tool_calls=5,
        successful_tool_calls=5,
    )
    assert metrics.composite_grade == "A"
    assert metrics.accuracy_score == 0.96
    assert metrics.tool_efficiency_score == 1.0
