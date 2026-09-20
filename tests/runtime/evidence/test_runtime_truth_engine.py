"""Tests for Runtime Truth Engine."""

import pytest
from app.runtime.truth_engine.truth_metrics_aggregator import (
    TruthMetricsAggregator,
)


def test_truth_metrics_aggregation():
    metrics = TruthMetricsAggregator.aggregate_truth()
    assert metrics.total_evidence_nodes > 0
    assert metrics.merkle_tree_root is not None
    assert metrics.graph_tamper_status in ["SECURE", "TAMPERED"]
    assert metrics.total_planner_decisions > 0
    assert metrics.total_tool_executions > 0
    assert metrics.total_snapshots_captured > 0
    assert metrics.cryptographic_integrity_pct >= 90.0
