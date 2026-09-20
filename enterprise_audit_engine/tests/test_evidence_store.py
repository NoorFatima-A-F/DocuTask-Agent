"""Unit tests for Evidence Store & Persistence."""

import shutil
from pathlib import Path
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
    AuditReportManifest,
)
from enterprise_audit_engine.storage.evidence_store import EvidenceStore


def test_evidence_store_lifecycle(tmp_path):
    store = EvidenceStore(tmp_path)

    record = EvidenceRecord.create(
        category="StorageTest",
        collector="UnitTestCollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        summary="Testing store persistence",
        confidence=EvidenceConfidence.MEDIUM,
        classification=EvidenceClassification.VERIFIED,
    )

    saved_path = store.save_evidence(record)
    assert saved_path.exists()

    loaded = store.load_all_evidence()
    assert len(loaded) == 1
    assert loaded[0].id == record.id
    assert loaded[0].content_hash == record.content_hash

    manifest = AuditReportManifest(
        run_id="RUN-TEST-001",
        total_evidence_collected=1,
        findings_count=1,
        maturity_scorecard={"StorageTest": "VERIFIED"},
        evidence_hashes=[record.content_hash],
    )
    manifest_path = store.save_manifest(manifest)
    assert manifest_path.exists()
