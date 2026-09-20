"""Tests for Progressive Traffic Splitting (Canary, Blue-Green, Shadow Mirroring)."""

import pytest
from app.networking.mesh.data_plane import MeshRequest, MeshResponse
from app.networking.routing.traffic_split import (
    SplitType,
    TrafficSplitConfig,
    TrafficSplitter,
    VersionSplit,
)


def test_traffic_splitter_weights():
    splitter = TrafficSplitter()
    config = TrafficSplitConfig(
        split_id="split-canary-01",
        service_name="ai-summarizer",
        split_type=SplitType.CANARY,
        splits=[
            VersionSplit(version="v1", weight=80),
            VersionSplit(version="v2", weight=20),
        ],
    )
    splitter.set_split_config(config)

    # Perform repeated selections to test distribution
    versions = [splitter.select_version("ai-summarizer") for _ in range(100)]
    assert "v1" in versions
    assert "v2" in versions
    # v1 should be majority
    v1_count = sum(1 for v in versions if v == "v1")
    assert v1_count > 50


def test_traffic_splitter_shadow_mirroring():
    splitter = TrafficSplitter()
    config = TrafficSplitConfig(
        split_id="split-shadow-01",
        service_name="ocr-pipeline",
        split_type=SplitType.SHADOW,
        splits=[VersionSplit(version="v1", weight=100)],
        shadow_version="v2-dark",
        shadow_percentage=100.0,  # 100% shadow mirror
    )
    splitter.set_split_config(config)

    should_mirror, shadow_ver = splitter.should_mirror_shadow("ocr-pipeline")
    assert should_mirror is True
    assert shadow_ver == "v2-dark"

    # Record shadow execution
    req = MeshRequest(
        source_service="gateway",
        target_service="ocr-pipeline",
        action="parse",
    )
    res = MeshResponse(status_code=200, duration_ms=45.0)
    splitter.record_shadow_execution(req, shadow_ver, res)

    records = splitter.get_shadow_records()
    assert len(records) == 1
    assert records[0]["shadow_version"] == "v2-dark"
    assert records[0]["status_code"] == 200
