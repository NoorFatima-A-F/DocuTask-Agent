"""
Tests for Ingestion Adapters, DocumentIntelligencePipeline, KnowledgeSDK, and Analytics.
"""

from app.knowledge.core.models import (
    ClassificationLevel,
    KnowledgeDocument,
    KnowledgeObject,
)
from app.knowledge.governance.engine import UserSecurityContext
from app.knowledge.processing.pipeline import DocumentIntelligencePipeline
from app.knowledge.sdk.builder import KnowledgeBuilder


def test_document_intelligence_pipeline_processing():
    pipeline = DocumentIntelligencePipeline()

    raw_text = """# Acme Vendor Agreement
Contact: legal-ops@acme.com
Date: 2026-09-19
Total Fee: $45,000.00 USD

This Master Services Agreement ("Agreement") governs the software automation deployment.

# Payment Terms
Invoices are payable within 30 days of receipt.
"""

    doc = KnowledgeDocument(
        id="kdoc-proc-test",
        knowledge_id="kobj-proc",
        title="Acme MSA",
        file_type="md",
        raw_content=raw_text,
    )

    processed = pipeline.process(doc)

    assert processed.classification_tag == "CONTRACT"
    assert len(processed.sections) >= 2
    assert processed.metadata["word_count"] > 10

    # Entity extraction checks
    entity_types = [e["type"] for e in processed.entities]
    entity_vals = [e["value"] for e in processed.entities]

    assert "EMAIL" in entity_types
    assert "legal-ops@acme.com" in entity_vals
    assert "MONEY" in entity_types
    assert "DATE" in entity_types


def test_knowledge_sdk_end_to_end():
    sdk = KnowledgeBuilder().build()

    # 1. Register Knowledge Object in Registry
    kobj = KnowledgeObject(
        id="kobj-iso-compliance",
        name="ISO-27001 Security Standard",
        department="Security",
        classification=ClassificationLevel.INTERNAL,
    )
    sdk.registry.register(kobj)

    # 2. Ingest Document
    doc = KnowledgeDocument(
        id="kdoc-iso-001",
        knowledge_id="kobj-iso-compliance",
        title="ISO-27001 Controls",
        file_type="md",
        raw_content="""# Access Control Policy
Users must enable multi-factor authentication (MFA) on all production cloud systems.
Session timeouts must occur after 15 minutes of inactivity.
""",
    )

    chunks = sdk.ingest_document(doc, chunking_strategy="heading")
    assert len(chunks) >= 1

    # 3. Query Context with Authorized User Context
    user_context = UserSecurityContext(
        user_id="auditor-1",
        organization_id="org-default",
        clearance=ClassificationLevel.INTERNAL,
    )

    context_pkg = sdk.query_context("What are the MFA and session timeout requirements?", user_context=user_context)

    assert len(context_pkg.chunks) >= 1
    assert "multi-factor authentication" in context_pkg.context_text
    assert len(context_pkg.citations) >= 1
    assert context_pkg.citations[0].source_title == "ISO-27001 Controls"

    # 4. Analytics Telemetry
    report = sdk.analytics.generate_report()
    assert report.total_queries == 1
    assert report.successful_queries == 1
    assert report.total_chunks_indexed >= 1
