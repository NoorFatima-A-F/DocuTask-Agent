"""
Tests for 8-Tier Enterprise Memory Platform (Working, Short-Term, Long-Term,
Semantic, Procedural, Episodic, Knowledge, Organization), Promotion, Demotion, and Expiration.
"""

from datetime import datetime, timedelta, timezone
from app.agents.memory.lifecycle import MemoryLifecycleState
from app.agents.memory.platform import EnterpriseMemoryPlatform, MemoryTier


def test_memory_tier_storage_and_hierarchical_retrieval():
    platform = EnterpriseMemoryPlatform()

    # Store across various tiers
    platform.store(key="active_task", value={"step": 1}, tier=MemoryTier.WORKING)
    platform.store(key="session_user", value="admin@acme.com", tier=MemoryTier.SHORT_TERM)
    platform.store(key="vendor_policy", value="Net 30 terms", tier=MemoryTier.ORGANIZATION)

    # Specific tier retrieval
    rec_work = platform.retrieve("active_task", tier=MemoryTier.WORKING)
    assert rec_work is not None
    assert rec_work.value["step"] == 1

    # Hierarchical retrieval
    rec_org = platform.retrieve("vendor_policy")
    assert rec_org is not None
    assert rec_org.tier == MemoryTier.ORGANIZATION
    assert rec_org.value == "Net 30 terms"


def test_memory_promotion_and_demotion():
    platform = EnterpriseMemoryPlatform()

    platform.store(key="tax_calc_routine", value="Multiply by 0.18", tier=MemoryTier.WORKING)
    assert platform.retrieve("tax_calc_routine", tier=MemoryTier.WORKING) is not None

    # Promote from WORKING to PROCEDURAL
    promoted = platform.promote("tax_calc_routine", from_tier=MemoryTier.WORKING, to_tier=MemoryTier.PROCEDURAL)
    assert promoted is not None
    assert promoted.tier == MemoryTier.PROCEDURAL
    assert promoted.state == MemoryLifecycleState.PROMOTED
    assert platform.retrieve("tax_calc_routine", tier=MemoryTier.WORKING) is None
    assert platform.retrieve("tax_calc_routine", tier=MemoryTier.PROCEDURAL) is not None

    # Demote
    demoted = platform.demote("tax_calc_routine", from_tier=MemoryTier.PROCEDURAL, to_tier=MemoryTier.SHORT_TERM)
    assert demoted is not None
    assert demoted.tier == MemoryTier.SHORT_TERM
    assert demoted.state == MemoryLifecycleState.DEMOTED


def test_memory_consolidation_merge_and_expiration():
    platform = EnterpriseMemoryPlatform()

    platform.store(key="fact_1", value="Acme is vendor A", tier=MemoryTier.SEMANTIC, importance=0.6)
    platform.store(key="fact_2", value="Acme payment term is 30 days", tier=MemoryTier.SEMANTIC, importance=0.8)

    merged = platform.merge(
        target_key="consolidated_acme",
        source_keys=["fact_1", "fact_2"],
        tier=MemoryTier.SEMANTIC,
    )
    assert merged is not None
    assert len(merged.value["merged_entries"]) == 2
    assert merged.importance == 0.8
    assert merged.state == MemoryLifecycleState.SUMMARIZED

    # Expiration check
    past_time = datetime.now(timezone.utc) - timedelta(minutes=5)
    platform.store(key="transient_token", value="xyz", tier=MemoryTier.WORKING, expires_at=past_time)

    expired_count = platform.expire_records()
    assert expired_count >= 1
    assert platform.retrieve("transient_token") is None
