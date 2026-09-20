"""
Test Suite: Closed-Loop Human Feedback & Knowledge Evolution
Validates human correction ingestion, self-reflection hypothesis formulation, and rule versioning/commit mechanisms.
"""
import pytest
from app.runtime.feedback_pipeline.feedback_processor import FeedbackProcessor
from app.runtime.feedback_pipeline.reflection_orchestrator import ReflectionOrchestrator
from app.runtime.feedback_pipeline.knowledge_versioner import KnowledgeVersioner


def test_feedback_ingestion_and_status_update():
    processor = FeedbackProcessor()
    
    fb = processor.ingest_correction(
        document_id="DOC-999",
        field_name="subtotal",
        extracted_value="$80.00",
        corrected_value="$100.00",
        confidence_was=0.75,
        submitted_by="user@example.com"
    )

    assert fb.document_id == "DOC-999"
    assert fb.status == "INGESTED"
    
    feedbacks = processor.list_feedbacks()
    assert len(feedbacks) >= 2


def test_reflection_orchestrator_insight_synthesis():
    processor = FeedbackProcessor()
    fb = processor.ingest_correction(
        document_id="DOC-EU-100",
        field_name="tax_rate",
        extracted_value="19%",
        corrected_value="20%",
        confidence_was=0.82,
    )

    insight = ReflectionOrchestrator.reflect_on_correction(fb)
    assert insight.feedback_id == fb.feedback_id
    assert "tax_rate" in insight.root_cause
    assert insight.simulation_accuracy_delta > 0.0
    assert insight.is_safe_to_commit is True


def test_knowledge_versioner_commits_and_rollbacks():
    versioner = KnowledgeVersioner()
    
    rule = versioner.commit_rule(
        rule_statement="Always verify tax_rate against destination country lookup",
        origin_feedback_id="fb_test_123",
        version="v1.4.0"
    )

    assert rule.is_active is True
    assert rule.version == "v1.4.0"
    assert len(rule.provenance_hash) == 16

    rules = versioner.list_rules()
    assert len(rules) >= 2
