"""Tests for Cluster Policies, Diagnostics, and Persistent Cluster Registry."""

import tempfile
from app.infrastructure.clusters.models import (
    CapacityModel,
    Cluster,
    ClusterStatus,
    ClusterType,
)
from app.infrastructure.clusters.policies import ClusterPolicyEngine
from app.infrastructure.clusters.diagnostics import ClusterDiagnosticsService
from app.infrastructure.clusters.registry import ClusterRegistry


def test_cluster_policy_engine():
    engine = ClusterPolicyEngine()

    cluster = Cluster(
        cluster_id="cls-policy",
        name="Policy Test Cluster",
        region_id="us-east-1",
        cluster_type=ClusterType.PRODUCTION,
        capacity=CapacityModel(allocatable_cpu_cores=100.0, utilized_cpu_cores=40.0),
        compliance_profiles=["SOC2_TYPE_II", "HIPAA"],
        supported_workloads=["ocr", "agent"],
        tenant_affinity=["tenant-a", "tenant-b"],
    )

    # Workload support
    assert engine.validate_workload_support(cluster, "ocr")[0] is True
    assert engine.validate_workload_support(cluster, "video_transcoding")[0] is False

    # Compliance
    assert engine.validate_compliance(cluster, ["SOC2_TYPE_II"])[0] is True
    assert engine.validate_compliance(cluster, ["FEDRAMP"])[0] is False

    # Tenant affinity
    assert engine.validate_tenant_affinity(cluster, "tenant-a")[0] is True
    assert engine.validate_tenant_affinity(cluster, "tenant-other")[0] is False

    # Capacity threshold
    assert engine.validate_capacity_threshold(cluster, max_utilization_pct=0.85)[0] is True
    assert engine.validate_capacity_threshold(cluster, max_utilization_pct=0.30)[0] is False


def test_cluster_registry_and_persistence():
    with tempfile.TemporaryDirectory() as tmpdir:
        persistence_path = f"{tmpdir}/clusters.json"
        registry = ClusterRegistry(persistence_path=persistence_path)

        c1 = Cluster(
            cluster_id="cls-reg-1",
            name="Cluster 1",
            region_id="us-east-1",
            environment="PRODUCTION",
            status=ClusterStatus.REGISTERED,
        )
        c2 = Cluster(
            cluster_id="cls-reg-2",
            name="Cluster 2",
            region_id="eu-west-1",
            environment="STAGING",
            status=ClusterStatus.REGISTERED,
        )

        registry.register_cluster(c1)
        registry.register_cluster(c2)

        # Filtering
        us_clusters = registry.list_clusters(region_id="us-east-1")
        assert len(us_clusters) == 1
        assert us_clusters[0].cluster_id == "cls-reg-1"

        # Lifecycle transition
        updated = registry.transition_state(
            "cls-reg-1", ClusterStatus.VALIDATING, reason="System check"
        )
        assert updated is not None
        assert updated.status == ClusterStatus.VALIDATING

        # Diagnostics
        diag_svc = ClusterDiagnosticsService(registry)
        report = diag_svc.generate_cluster_report("cls-reg-1")
        assert report.cluster_id == "cls-reg-1"
        assert report.status == ClusterStatus.VALIDATING.value

        # Test reloading from persistence file
        new_registry = ClusterRegistry(persistence_path=persistence_path)
        loaded_c1 = new_registry.get_cluster("cls-reg-1")
        assert loaded_c1 is not None
        assert loaded_c1.status == ClusterStatus.VALIDATING
