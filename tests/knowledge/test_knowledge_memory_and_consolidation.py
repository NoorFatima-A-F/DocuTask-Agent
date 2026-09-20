"""
Tests for MemoryIntelligencePlatform and MemoryConsolidationEngine.
"""

import time
import pytest
from app.knowledge.memory.consolidation import MemoryConsolidationEngine
from app.knowledge.memory.engine import MemoryIntelligencePlatform, MemoryTier


def test_memory_intelligence_tiers_and_expiration():
    platform = MemoryIntelligencePlatform()

    # Store in WORKING memory with short TTL
    platform.store(
        tier=MemoryTier.WORKING,
        key="temp_agent_thought",
        value={"step": 1, "hypothesis": "Invoice is valid"},
        ttl_seconds=1,
    )

    # Store in PROCEDURAL memory
    platform.store(
        tier=MemoryTier.PROCEDURAL,
        key="invoice_processing_recipe",
        value=["step1_ocr", "step2_validate_vat", "step3_post_to_erp"],
        importance_score=0.9,
    )

    # Immediate retrieval
    assert platform.retrieve(MemoryTier.WORKING, "temp_agent_thought") is not None
    assert platform.retrieve(MemoryTier.PROCEDURAL, "invoice_processing_recipe")[0] == "step1_ocr"

    # Verify access count updated
    item = platform.get_item(MemoryTier.PROCEDURAL, "invoice_processing_recipe")
    assert item.access_count == 1

    # Promotion
    platform.promote(MemoryTier.PROCEDURAL, MemoryTier.ORGANIZATION, "invoice_processing_recipe")
    assert platform.retrieve(MemoryTier.PROCEDURAL, "invoice_processing_recipe") is None
    assert platform.retrieve(MemoryTier.ORGANIZATION, "invoice_processing_recipe") is not None

    # TTL Expiration test
    time.sleep(1.1)
    assert platform.retrieve(MemoryTier.WORKING, "temp_agent_thought") is None


def test_memory_consolidation_engine():
    platform = MemoryIntelligencePlatform()
    consolidation = MemoryConsolidationEngine(platform)

    # Low-importance item in WORKING memory
    platform.store(
        tier=MemoryTier.WORKING,
        key="scratchpad_notes",
        value="raw calculation scratchpad",
        importance_score=0.2,
    )

    # High-importance item in WORKING memory
    platform.store(
        tier=MemoryTier.WORKING,
        key="critical_customer_preference",
        value="Prefers monthly consolidated PDF statements",
        importance_score=0.85,
    )

    # High-access item in SHORT_TERM memory
    st_item = platform.store(
        tier=MemoryTier.SHORT_TERM,
        key="frequent_vendor_vat",
        value="US-TAX-99887766",
        importance_score=0.4,
    )
    # Simulate 4 reads to exceed access_count_threshold
    for _ in range(4):
        platform.retrieve(MemoryTier.SHORT_TERM, "frequent_vendor_vat")

    # Run consolidation batch
    report = consolidation.consolidate(importance_threshold_for_promotion=0.7, access_count_threshold=3)

    assert report.items_scanned >= 3
    assert report.items_promoted >= 2

    # Verify critical_customer_preference was promoted to SHORT_TERM
    assert platform.retrieve(MemoryTier.SHORT_TERM, "critical_customer_preference") is not None

    # Verify frequent_vendor_vat was promoted to EPISODIC
    assert platform.retrieve(MemoryTier.EPISODIC, "frequent_vendor_vat") == "US-TAX-99887766"
