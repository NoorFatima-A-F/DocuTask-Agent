"""
Tests for Experience Intelligence Engine (Pillar 1).
"""

from app.runtime.intelligence.experience.experience_extractor import ExperienceExtractor
from app.runtime.intelligence.experience.experience_record import (
    ExperienceRecord,
    ExperienceStore,
)


def test_experience_record_creation_and_hashing():
    rec = ExperienceRecord(
        experience_id="exp_test_001",
        mission_id="msn_test_100",
        document_type="invoice",
        task_type="extraction",
        total_latency_ms=1150.0,
        total_cost_usd=0.012,
        final_confidence=0.97,
        evidence_root_hash="0xdeadbeef12345678",
    )
    assert rec.content_hash != ""
    assert len(rec.content_hash) == 64
    assert rec.compute_hash() == rec.content_hash


def test_experience_store_append_and_query():
    store = ExperienceStore()
    extractor = ExperienceExtractor(store)

    rec1 = extractor.extract_from_mission(
        mission_id="msn_1",
        document_type="invoice",
        task_type="extraction",
        telemetry={"total_latency_ms": 950.0, "total_cost_usd": 0.009, "final_confidence": 0.98},
    )
    extractor.extract_from_mission(
        mission_id="msn_2",
        document_type="contract",
        task_type="extraction",
        telemetry={"total_latency_ms": 2100.0, "total_cost_usd": 0.030, "final_confidence": 0.92},
    )

    assert store.count() == 2
    assert store.get(rec1.experience_id) is not None

    inv_records = store.query(document_type="invoice")
    assert len(inv_records) == 1
    assert inv_records[0].document_type == "invoice"

    high_conf = store.query(min_confidence=0.95)
    assert len(high_conf) == 1
    assert high_conf[0].mission_id == "msn_1"
