"""
Tests for Runtime Truth Ledger (Pillar 1).
"""

from app.runtime.truth.ledger import TruthLedger


def test_truth_ledger_append_and_hash_chain():
    ledger = TruthLedger()
    
    e1 = ledger.append_event(
        mission_id="msn_1001",
        event_type="PLANNER_DECISION",
        planner_version="v2.1.0",
    )
    assert e1.entry_hash != ""
    assert e1.parent_event_hash == "0" * 64

    e2 = ledger.append_event(
        mission_id="msn_1001",
        event_type="TOOL_EXECUTION",
        tool_name="tesseract_ocr",
    )
    assert e2.parent_event_hash == e1.entry_hash
    assert ledger.count() == 2

    # Integrity verification
    verification = ledger.verify_chain_integrity()
    assert verification["valid"] is True
    assert verification["total_entries"] == 2


def test_truth_ledger_tamper_detection():
    ledger = TruthLedger()
    e1 = ledger.append_event(mission_id="msn_1", event_type="PLANNER_DECISION")
    ledger.append_event(mission_id="msn_1", event_type="TOOL_EXECUTION")

    # Simulate retroactive tamper
    e1.planner_version = "v9.9.9_tampered"
    verification = ledger.verify_chain_integrity()
    assert verification["valid"] is False
    assert verification["tampered_event_id"] == e1.event_id
