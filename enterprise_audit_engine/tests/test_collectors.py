"""Unit tests for Audit Collectors."""

import pytest
from pathlib import Path
from enterprise_audit_engine.collectors.repository.repository_collector import RepositoryCollector
from enterprise_audit_engine.collectors.governance.governance_collector import GovernanceCollector
from enterprise_audit_engine.collectors.dependencies.dependency_collector import DependencyCollector
from enterprise_audit_engine.collectors.security.security_collector import SecurityCollector


@pytest.mark.asyncio
async def test_repository_collector():
    repo_root = Path(__file__).parent.parent.parent
    collector = RepositoryCollector(repo_root)
    records = await collector.collect()

    assert len(records) > 0
    record = records[0]
    assert record.category == "RepositoryStructure"
    assert "total_files" in record.raw_payload


@pytest.mark.asyncio
async def test_governance_collector():
    repo_root = Path(__file__).parent.parent.parent
    collector = GovernanceCollector(repo_root)
    records = await collector.collect()

    assert len(records) > 0
    record = records[0]
    assert record.category == "GovernanceAndCompliance"
    assert record.raw_payload["required_docs"]["README.md"] is True


@pytest.mark.asyncio
async def test_security_collector():
    repo_root = Path(__file__).parent.parent.parent
    collector = SecurityCollector(repo_root)
    records = await collector.collect()

    assert len(records) > 0
    record = records[0]
    assert record.category == "SecurityAndCompliance"
    assert "secrets_detected_count" in record.raw_payload
