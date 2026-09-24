"""Tests for Cryptographic Execution Snapshots and Reproducibility (Phase 8C)."""

from app.model_governance.reproducibility.snapshot import ReproducibilityService


def test_reproducibility_snapshot_integrity_and_verification():
    service = ReproducibilityService()

    snapshot = service.capture_snapshot(
        snapshot_id="snap-20260919-001",
        organization_id="org_enterprise",
        task_name="invoice_parsing",
        model_id="gpt-4o",
        model_version="2024-08-06",
        provider="OPENAI",
        prompt_text="Extract invoice line items from the provided text.",
        system_prompt="You are a strict financial document extractor.",
        input_data={"document_id": "doc_1024", "text": "Invoice total $5,000 USD"},
        hyperparameters={"temperature": 0.0, "seed": 42},
    )

    assert snapshot.snapshot_hash != ""
    assert service.verify_reproducibility("snap-20260919-001") is True

    # Finalize with output
    service.finalize_snapshot("snap-20260919-001", {"total": 5000, "currency": "USD"})
    assert service.verify_reproducibility("snap-20260919-001") is True

    # Tampering with snapshot payload breaks verification
    snapshot.prompt_template_hash = "tampered_hash_value"
    assert service.verify_reproducibility("snap-20260919-001") is False
