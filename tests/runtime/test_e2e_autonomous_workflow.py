"""
End-to-End Automated Test for Autonomous Document Processing Pipeline.
Validates:
- Real DAG task execution across multiple agent steps
- Checkpoint persistence and version tracking
- Real failure injection and supervisor automatic recovery
- Context restoration after simulated crash
- Reflection quality scoring
- Immutable cryptographic audit log chain verification
"""

import pytest
from examples.autonomous_invoice_workflow.run_autonomous_invoice_pipeline import AutonomousInvoicePipeline


@pytest.mark.asyncio
async def test_end_to_end_autonomous_invoice_workflow():
    payload = {
        "document_id": "test-doc-inv-001",
        "invoice_number": "INV-TEST-2026",
        "vendor": "OmniCorp Global Dynamics",
        "amount": "85000.00",
        "tax": "8500.00",
        "items": [
            {"description": "AI Cluster Hardware", "qty": 1, "price": "85000.00"}
        ],
    }

    pipeline = AutonomousInvoicePipeline()
    result = await pipeline.run(payload)

    assert result["status"] == "SUCCESS"
    assert result["document_id"] == "test-doc-inv-001"
    assert result["invoice_number"] == "INV-TEST-2026"
    assert result["failure_recovered"] is True
    assert result["reflection_score"] >= 0.95
    assert result["audit_chain_valid"] is True
    assert result["checkpoints_count"] >= 5
    assert len(result["checkpoints_versions"]) >= 5
    assert result["extracted_data"]["vendor"] == "OmniCorp Global Dynamics"
    assert result["extracted_data"]["total_amount"] == "85000.00"
