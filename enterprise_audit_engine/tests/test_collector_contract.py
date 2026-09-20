"""Formal Contract Tests for All Evidence Collectors."""

import asyncio
import pytest
from pathlib import Path
from enterprise_audit_engine.collectors import ALL_COLLECTORS
from enterprise_audit_engine.collectors.base import BaseCollector
from enterprise_audit_engine.domain.evidence.models import EvidenceRecord, EvidenceSourceType


def test_collector_contract_compliance(tmp_path):
    """Verifies that all registered collectors adhere to the BaseCollector contract."""
    for col_cls in ALL_COLLECTORS:
        assert issubclass(col_cls, BaseCollector), f"{col_cls} must subclass BaseCollector"
        
        collector = col_cls(repo_root=tmp_path)
        assert collector.name, f"{col_cls} missing name property"
        assert collector.category, f"{col_cls} missing category property"

        # Execute collector on empty/minimal repo
        records = asyncio.run(collector.collect())
        assert isinstance(records, list), f"{col_cls}.collect() must return a list"
        
        for r in records:
            assert isinstance(r, EvidenceRecord), f"Items returned by {col_cls} must be EvidenceRecord"
            assert r.id.startswith("EV-"), f"Record ID {r.id} must start with 'EV-'"
            assert r.category, f"Record must have non-empty category"
            assert isinstance(r.source_type, EvidenceSourceType), f"Record source_type must be valid EvidenceSourceType"
            assert r.content_hash == r.calculate_hash(), f"Record content_hash must match computed hash"
