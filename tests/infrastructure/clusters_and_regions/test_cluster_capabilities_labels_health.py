"""Tests for Cluster Capabilities, Labels, and Health Aggregation."""

from datetime import datetime, timezone, timedelta
from app.infrastructure.clusters.capabilities import ClusterCapabilityRegistry
from app.infrastructure.clusters.labels import ClusterLabelingSystem
from app.infrastructure.clusters.health import (
    ClusterHealthAggregator,
    SubComponentHealth,
)
from app.infrastructure.clusters.models import Cluster, ClusterLease, ClusterStatus


def test_cluster_capability_registry():
    cap_reg = ClusterCapabilityRegistry()
    cap_reg.register_capabilities("cls-1", {"gpu_a100", "nvme_ssd", "arm64", "isolated_vpc"})
    cap_reg.register_capabilities("cls-2", {"gpu_t4", "nvme_ssd", "x86_64"})

    assert cap_reg.has_capabilities("cls-1", {"gpu_a100", "arm64"}) is True
    assert cap_reg.has_capabilities("cls-1", {"gpu_t4"}) is False

    results = cap_reg.query_clusters({"nvme_ssd"})
    assert "cls-1" in results and "cls-2" in results

    results_a100 = cap_reg.query_clusters({"gpu_a100"})
    assert results_a100 == ["cls-1"]


def test_cluster_labeling_system():
    lbl_sys = ClusterLabelingSystem()

    valid_labels = {
        "env": "production",
        "docutask.io/tier": "frontend",
        "region": "us-east-1",
    }
    is_valid, errs = lbl_sys.validate_labels(valid_labels)
    assert is_valid is True
    assert len(errs) == 0

    # Invalid characters in key
    invalid_labels = {"invalid$$key": "val"}
    is_valid, errs = lbl_sys.validate_labels(invalid_labels)
    assert is_valid is False

    # Selector matching
    selector = {"env": "production", "region": "us-east-1"}
    matches, match_errs = lbl_sys.matches_selector(valid_labels, selector)
    assert matches is True

    mismatch_selector = {"env": "staging"}
    matches, match_errs = lbl_sys.matches_selector(valid_labels, mismatch_selector)
    assert matches is False


def test_cluster_health_aggregator():
    aggregator = ClusterHealthAggregator()

    # 1. All healthy components
    healthy_subs = [
        SubComponentHealth(component_name="node", is_healthy=True),
        SubComponentHealth(component_name="service", is_healthy=True),
        SubComponentHealth(component_name="worker", is_healthy=True),
        SubComponentHealth(component_name="queue", is_healthy=True),
        SubComponentHealth(component_name="database", is_healthy=True),
    ]
    report = aggregator.evaluate_health(healthy_subs)
    assert report.is_healthy is True
    assert report.status == "HEALTHY"
    assert len(report.degraded_components) == 0

    # 2. Degraded component
    degraded_subs = [
        SubComponentHealth(component_name="node", is_healthy=True),
        SubComponentHealth(component_name="service", is_healthy=False, message="High error rate"),
    ]
    report_deg = aggregator.evaluate_health(degraded_subs)
    assert report_deg.is_healthy is False
    assert report_deg.status == "DEGRADED"
    assert "service" in report_deg.degraded_components

    # 3. Heartbeat lease creation and expiration
    lease = aggregator.create_or_renew_lease("cls-test", ttl_seconds=10)
    assert lease.is_valid is True
    assert aggregator.is_lease_valid(lease) is True

    # Manually backdate lease to test expiration
    expired_lease = ClusterLease(
        cluster_id="cls-test",
        ttl_seconds=10,
        last_renewed=datetime.now(timezone.utc) - timedelta(seconds=20),
        is_valid=True,
    )
    assert aggregator.is_lease_valid(expired_lease) is False
