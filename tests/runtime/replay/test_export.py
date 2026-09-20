"""
Unit Tests for Forensic Export Formatting and Signatures.
"""

import pytest
import json
from app.runtime.observability.schemas import RuntimeEvent, EventCategory, EventType, EventSeverity
from app.runtime.observability.event_serializer import EventSerializer
from app.runtime.replay.replay_state_machine import ReplayStateMachine
from app.runtime.replay.replay_exporter import ReplayExporter
from app.runtime.audit.audit_builder import AuditLogBuilder
from app.runtime.audit.audit_export import AuditExporter


def test_replay_exporter_package():
    events = []
    prev_hash = "0" * 64
    for i in range(3):
        ev = RuntimeEvent(
            event_id=f"ev_exp_{i+1}",
            mission_id="m_exp_01",
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

    state = ReplayStateMachine.create_initial_state("m_exp_01")
    for e in events:
        state = ReplayStateMachine.apply_event(state, e)

    pkg = ReplayExporter.export_mission_package("m_exp_01", events, state)

    assert pkg.mission_id == "m_exp_01"
    assert pkg.total_events == 3
    assert pkg.hash_chain_verified is True
    assert pkg.package_signature is not None
    assert len(pkg.package_signature) == 64


def test_audit_exporter_csv_and_json():
    events = [
        RuntimeEvent(
            event_id="ev_exp_aud",
            mission_id="m_exp_02",
            sequence_number=1,
            category=EventCategory.PLANNER,
            event_type=EventType.PLANNER_STRATEGY_SELECTED,
            severity=EventSeverity.INFO,
            stage="PLANNING",
            payload={"rationale": "Forensic test"},
        )
    ]
    records = AuditLogBuilder.build_audit_records_from_events("m_exp_02", events)

    json_str = AuditExporter.export_json(records)
    parsed = json.loads(json_str)
    assert len(parsed) == 1
    assert parsed[0]["mission_id"] == "m_exp_02"

    csv_str = AuditExporter.export_csv(records)
    assert "audit_id,mission_id" in csv_str
    assert "m_exp_02" in csv_str
