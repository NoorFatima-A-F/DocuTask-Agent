"""
Test Suite: Audit Intelligence & End-to-End Cryptographic Provenance
Validates field-level provenance lineage tracing (pixel -> OCR -> LLM -> validation -> DB) and decision audit query engine.
"""
import pytest
from app.runtime.audit_intelligence.provenance_graph import FieldProvenanceTracer
from app.runtime.audit_intelligence.audit_query_engine import AuditQueryEngine


def test_field_provenance_trace():
    trace = FieldProvenanceTracer.trace_field("DOC-INV-2026", "invoice_total_amount")
    
    assert trace["document_id"] == "DOC-INV-2026"
    assert trace["field_key"] == "invoice_total_amount"
    assert len(trace["lineage_steps"]) == 5
    
    # Check that the 5 pipeline stages are connected in sequence
    stages = [node["stage"] for node in trace["lineage_steps"]]
    assert stages == [
        "SOURCE_DOCUMENT",
        "OCR_BOUNDING_BOX",
        "LLM_EXTRACTION",
        "INVARIANT_VALIDATION",
        "STORAGE_COMMIT"
    ]
    assert trace["is_tamper_proof"] is True


def test_audit_query_engine_search_and_filter():
    engine = AuditQueryEngine()
    
    all_records = engine.query_audit_trail()
    assert len(all_records) >= 2

    # Query by decision type
    filtered = engine.query_audit_trail(decision_type="MODEL_ROUTING")
    assert len(filtered) >= 1
    assert all(r["decision_type"] == "MODEL_ROUTING" for r in filtered)

    # Free text query
    searched = engine.query_audit_trail(search_query="Gemini 2.5 Flash")
    assert len(searched) >= 1
    assert "Gemini 2.5 Flash" in searched[0]["decision_summary"]
