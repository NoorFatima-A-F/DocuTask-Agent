"""
Unit Tests for Event-Sourced Timeline Engine.
"""

from app.runtime.observability.schemas import RuntimeEvent, EventCategory, EventType, EventSeverity
from app.runtime.timeline.timeline_engine import MasterTimelineEngine


def test_timeline_engine_reconstruction():
    engine = MasterTimelineEngine()

    events = [
        RuntimeEvent(
            event_id="ev_01",
            mission_id="m_tl_01",
            sequence_number=1,
            category=EventCategory.MISSION,
            event_type=EventType.MISSION_STARTED,
            severity=EventSeverity.INFO,
            stage="INGESTION",
            payload={"summary": "Mission document ingested"},
        ),
        RuntimeEvent(
            event_id="ev_02",
            mission_id="m_tl_01",
            sequence_number=2,
            category=EventCategory.EXECUTION,
            event_type=EventType.EXECUTION_TASK_STARTED,
            severity=EventSeverity.INFO,
            stage="OCR",
            payload={"task_id": "node_ocr", "summary": "OCR processing initiated"},
        ),
    ]

    entries = engine.build_timeline_from_events("m_tl_01", events)

    assert len(entries) == 2
    assert entries[0].stage == "INGESTION"
    assert entries[0].summary == "Mission document ingested"
    assert entries[1].stage == "OCR"

    idx = engine.get_index("m_tl_01")
    assert idx is not None
    assert idx.get_by_event_id("ev_01") is not None
    assert len(idx.get_by_stage("OCR")) == 1
