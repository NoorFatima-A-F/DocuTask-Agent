"""
Unit Tests for Enterprise Audit Engine and Cryptographic Signatures.
"""

from app.runtime.observability.schemas import RuntimeEvent, EventCategory, EventType, EventSeverity
from app.runtime.audit.audit_engine import MasterAuditEngine


def test_audit_engine_signature_and_verification():
    engine = MasterAuditEngine()

    events = [
        RuntimeEvent(
            event_id="ev_aud_01",
            mission_id="m_aud_01",
            sequence_number=1,
            category=EventCategory.PLANNER,
            event_type=EventType.PLANNER_STRATEGY_SELECTED,
            severity=EventSeverity.INFO,
            stage="PLANNING",
            payload={"selected_strategy": "Pareto Extraction", "rationale": "Optimized latency"},
        ),
        RuntimeEvent(
            event_id="ev_aud_02",
            mission_id="m_aud_01",
            sequence_number=2,
            category=EventCategory.GOVERNANCE,
            event_type=EventType.GOVERNANCE_RULE_EVALUATED,
            severity=EventSeverity.INFO,
            stage="VALIDATION",
            payload={"rule": "Arithmetic Invariant", "passed": True},
        ),
    ]

    records = engine.build_from_events("m_aud_01", events)

    assert len(records) == 2
    assert records[0].sha256 is not None
    assert records[0].signature is not None
    assert records[1].previous_sha256 == records[0].sha256

    report = engine.verify_audit_trail("m_aud_01")
    assert report.is_valid is True
    assert report.total_records == 2
    assert report.audit_coverage_ratio == 1.0


def test_audit_engine_tamper_detection():
    engine = MasterAuditEngine()

    events = [
        RuntimeEvent(
            event_id="ev_1",
            mission_id="m_tamper_01",
            sequence_number=1,
            category=EventCategory.PLANNER,
            event_type=EventType.PLANNER_STRATEGY_SELECTED,
            severity=EventSeverity.INFO,
            stage="PLANNING",
            payload={},
        ),
        RuntimeEvent(
            event_id="ev_2",
            mission_id="m_tamper_01",
            sequence_number=2,
            category=EventCategory.EXECUTION,
            event_type=EventType.EXECUTION_TASK_COMPLETED,
            severity=EventSeverity.INFO,
            stage="EXECUTION",
            payload={},
        ),
    ]

    records = engine.build_from_events("m_tamper_01", events)
    # Intentionally corrupt record 0 sha256
    records[0].sha256 = "corrupted_hash_value_12345"

    report = engine.verify_audit_trail("m_tamper_01")
    assert report.is_valid is False
    assert report.first_tampered_index is not None
