"""
Unit Tests for Replay Cryptographic Hash-Chain Integrity.
"""

import pytest
from app.runtime.observability.schemas import RuntimeEvent, EventCategory, EventType, EventSeverity
from app.runtime.observability.event_serializer import EventSerializer
from app.runtime.replay.replay_integrity import ReplayIntegrityVerifier


def test_integrity_verifier_clean_stream():
    events = []
    prev_hash = "0" * 64
    for i in range(5):
        ev = RuntimeEvent(
            event_id=f"ev_int_{i+1}",
            mission_id="m_int_01",
            sequence_number=i + 1,
            category=EventCategory.EXECUTION,
            event_type=EventType.EXECUTION_TASK_COMPLETED,
            severity=EventSeverity.INFO,
            stage="TEST",
            payload={"step": i},
            previous_hash=prev_hash,
        )
        ev.hash = EventSerializer.compute_event_hash(ev, prev_hash)
        prev_hash = ev.hash
        events.append(ev)

    res = ReplayIntegrityVerifier.verify_event_stream(events)
    assert res.is_valid is True
    assert res.total_events_verified == 5
    assert res.first_tampered_index is None


def test_integrity_verifier_detects_hash_tamper():
    events = []
    prev_hash = "0" * 64
    for i in range(4):
        ev = RuntimeEvent(
            event_id=f"ev_tamper_{i+1}",
            mission_id="m_tamper_02",
            sequence_number=i + 1,
            category=EventCategory.EXECUTION,
            event_type=EventType.EXECUTION_TASK_COMPLETED,
            severity=EventSeverity.INFO,
            stage="TEST",
            payload={"step": i},
            previous_hash=prev_hash,
        )
        ev.hash = EventSerializer.compute_event_hash(ev, prev_hash)
        prev_hash = ev.hash
        events.append(ev)

    # Tamper with event 2 hash
    events[2].hash = "tampered_hash_value_9999"

    res = ReplayIntegrityVerifier.verify_event_stream(events)
    assert res.is_valid is False
    assert res.first_tampered_index == 2
    assert res.first_tampered_event_id == "ev_tamper_3"
