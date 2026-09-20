"""Tests for Region Models, Registry, Policies, Tenant Affinity, and Multi-Region Routing."""

import tempfile
from app.infrastructure.regions.models import (
    Geography,
    Region,
    RegionStatus,
)
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.regions.policies import RegionPolicyEngine
from app.infrastructure.regions.affinity import (
    TenantAffinityManager,
    TenantAffinityRule,
)
from app.infrastructure.regions.routing import MultiRegionRouter


def test_region_registry_operations():
    with tempfile.TemporaryDirectory() as tmpdir:
        persistence_path = f"{tmpdir}/regions.json"
        registry = RegionRegistry(persistence_path=persistence_path)

        r1 = Region(
            region_id="us-east-1",
            name="us-east-1",
            display_name="US East (N. Virginia)",
            provider="aws",
            data_residency_jurisdiction="US",
            is_primary=True,
            status=RegionStatus.ACTIVE,
        )
        r2 = Region(
            region_id="eu-west-1",
            name="eu-west-1",
            display_name="Europe (Ireland)",
            provider="aws",
            data_residency_jurisdiction="EU",
            geography=Geography(continent="Europe", country="IE", jurisdiction="EU"),
            status=RegionStatus.ACTIVE,
        )

        registry.register_region(r1)
        registry.register_region(r2)

        # Filtering
        eu_regions = registry.list_regions(jurisdiction="EU")
        assert len(eu_regions) == 1
        assert eu_regions[0].region_id == "eu-west-1"

        # Cluster association
        registry.assign_cluster_to_region("us-east-1", "cls-us-1")
        assert "cls-us-1" in registry.get_region("us-east-1").active_cluster_ids

        registry.remove_cluster_from_region("us-east-1", "cls-us-1")
        assert "cls-us-1" not in registry.get_region("us-east-1").active_cluster_ids

        # Reload persistence
        new_reg = RegionRegistry(persistence_path=persistence_path)
        assert new_reg.get_region("eu-west-1") is not None


def test_region_policy_engine():
    engine = RegionPolicyEngine()

    us_region = Region(
        region_id="us-east-1",
        name="us-east-1",
        display_name="US East",
        data_residency_jurisdiction="US",
        compliance_certifications=["SOC2_TYPE_II", "HIPAA"],
    )
    eu_region = Region(
        region_id="eu-west-1",
        name="eu-west-1",
        display_name="EU West",
        data_residency_jurisdiction="EU",
        geography=Geography(jurisdiction="EU"),
        compliance_certifications=["GDPR", "ISO_27001"],
    )

    # Data residency
    assert engine.evaluate_data_residency(us_region, "US")[0] is True
    assert engine.evaluate_data_residency(us_region, "EU")[0] is False
    assert engine.evaluate_data_residency(eu_region, "GLOBAL")[0] is True

    # Compliance
    assert engine.validate_compliance(us_region, ["SOC2_TYPE_II"])[0] is True
    assert engine.validate_compliance(us_region, ["GDPR"])[0] is False

    # Egress Policy (EU to US without gateway fails)
    assert engine.validate_egress_policy(eu_region, us_region)[0] is False

    # Regional quorum
    assert engine.check_regional_quorum([us_region, eu_region], min_quorum_count=2) is True
    us_region.status = RegionStatus.OFFLINE
    assert engine.check_regional_quorum([us_region, eu_region], min_quorum_count=2) is False


def test_tenant_affinity_and_multi_region_router():
    affinity_mgr = TenantAffinityManager()
    affinity_mgr.set_tenant_affinity(
        TenantAffinityRule(
            tenant_id="tenant-eu-only",
            allowed_region_ids=["eu-west-1", "eu-central-1"],
            exclusive=True,
            required_jurisdiction="EU",
        )
    )

    assert affinity_mgr.is_region_allowed_for_tenant("tenant-eu-only", "eu-west-1") is True
    assert affinity_mgr.is_region_allowed_for_tenant("tenant-eu-only", "us-east-1") is False

    router = MultiRegionRouter(affinity_manager=affinity_mgr)
    candidates = [
        Region(
            region_id="us-east-1",
            name="us-east-1",
            display_name="US East",
            data_residency_jurisdiction="US",
            routing_priority=10,
            is_primary=True,
        ),
        Region(
            region_id="eu-west-1",
            name="eu-west-1",
            display_name="EU West",
            data_residency_jurisdiction="EU",
            geography=Geography(jurisdiction="EU"),
            routing_priority=20,
        ),
    ]

    # For tenant-eu-only, only EU should be ranked
    ranked = router.rank_regions(candidates, tenant_id="tenant-eu-only")
    assert len(ranked) == 1
    assert ranked[0].region_id == "eu-west-1"

    # For unrestricted tenant, primary US East should rank first
    ranked_unrestricted = router.rank_regions(candidates, tenant_id="tenant-general")
    assert len(ranked_unrestricted) == 2
    assert ranked_unrestricted[0].region_id == "us-east-1"
