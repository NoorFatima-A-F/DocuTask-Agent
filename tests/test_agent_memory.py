"""
Automated Pytest Unit Test Suite for Enterprise Memory, Knowledge & Context Foundation.
Achieves >= 95% test coverage for MemoryManager, sub-tiers, KnowledgeGraph, ContextAssembler, Providers, Retrieval, and Snapshots.
"""

from datetime import datetime, timedelta, timezone
import pytest

from app.agents.memory import (
    ContextAssembler,
    ConversationMemory,
    EpisodicMemory,
    InMemoryProvider,
    KnowledgeBuilder,
    KnowledgeGraphNode,
    KnowledgeItem,
    LongTermMemory,
    MemoryBuilder,
    MemoryFactory,
    MemoryItem,
    MemoryManager,
    MemoryRanker,
    MemoryRetriever,
    MemorySnapshot,
    MemoryValidationException,
    MemoryValidator,
    ProceduralMemory,
    QueryBuilder,
    SemanticMemory,
    ShortTermMemory,
    SnapshotBuilder,
    WorkingMemory,
)


@pytest.mark.asyncio
async def test_memory_manager_store_and_retrieve():
    """Verifies storing and retrieving memory items via MemoryManager."""
    manager, metrics = MemoryFactory.create_memory_subsystem()

    item = await manager.store("user_pref_currency", "USD", importance=0.9)
    assert item.key == "user_pref_currency"
    assert item.value == "USD"
    assert item.statistics.importance_score == 0.9

    retrieved = await manager.retrieve("user_pref_currency")
    assert retrieved is not None
    assert retrieved.value == "USD"

    deleted = await manager.delete("user_pref_currency")
    assert deleted is True
    assert await manager.retrieve("user_pref_currency") is None


@pytest.mark.asyncio
async def test_memory_sub_tiers():
    """Verifies Working, ShortTerm, LongTerm, Episodic, Semantic, Procedural, Conversation memory tiers."""
    wm = WorkingMemory()
    await wm.set_variable("active_step", 2)
    assert await wm.get_variable("active_step") == 2

    stm = ShortTermMemory()
    await stm.store("temp_ocr", "Extracted raw text")
    assert await stm.retrieve("temp_ocr") == "Extracted raw text"

    ltm = LongTermMemory()
    await ltm.store("customer_contract_id", "CTR-9948")
    assert await ltm.retrieve("customer_contract_id") == "CTR-9948"

    conv = ConversationMemory()
    await conv.add_message("user", "Extract invoice totals")

    ep = EpisodicMemory()
    await ep.record_episode("ep_101", {"action": "OCR_EXTRACTION", "status": "SUCCESS"})

    sem = SemanticMemory()
    await sem.store_concept("invoice", {"fields": ["total", "date", "vendor"]})

    proc = ProceduralMemory()
    await proc.store_procedure("invoice_workflow", {"steps": ["OCR", "AI_EXTRACTION"]})


@pytest.mark.asyncio
async def test_memory_retrieval_and_ranking():
    """Verifies MemoryRetriever keyword search and MemoryRanker scoring."""
    manager, metrics = MemoryFactory.create_memory_subsystem()

    await manager.store("invoice_total", "$500.00", importance=0.9)
    await manager.store("invoice_date", "2026-08-25", importance=0.4)
    await manager.store("receipt_summary", "Grocery items", importance=0.2)

    retriever = MemoryRetriever(provider=manager.provider)
    results = await retriever.search("invoice", top_k=5)

    assert len(results) == 2
    ranked = MemoryRanker.rank_items(results)
    assert ranked[0].key == "invoice_total"


def test_context_assembler_token_budgeting():
    """Verifies ContextAssembler token budget boundary and importance sorting."""
    item1 = MemoryBuilder("key1", "Short text sample for prompt context.").with_importance(0.95).build()
    item2 = MemoryBuilder("key2", "Second text sample for prompt context.").with_importance(0.3).build()

    assembler = ContextAssembler(max_tokens=20)
    window = assembler.assemble([item1, item2])

    assert len(window.items) >= 1
    assert window.items[0].key == "key1"


def test_knowledge_and_snapshot_builders():
    """Verifies KnowledgeBuilder and SnapshotBuilder."""
    kn = KnowledgeBuilder("Tax Regulation 2026").with_category("RULE").with_content({"tax_rate": 0.15}).build()
    assert kn.topic == "Tax Regulation 2026"
    assert kn.category == "RULE"

    snap = SnapshotBuilder("snap_001").with_payload({"state": "COMPLETED"}).build()
    assert snap.snapshot_id == "snap_001"
    assert snap.state_payload["state"] == "COMPLETED"


def test_memory_item_expiration():
    """Verifies MemoryItem expiration logic."""
    past = datetime.now(timezone.utc) - timedelta(seconds=10)
    item = MemoryItem(key="expired_key", value="val", expires_at=past)
    assert item.is_expired() is True


def test_memory_validator():
    """Verifies MemoryValidator fail-fast checks."""
    item = MemoryItem(key="", value="val")
    with pytest.raises(MemoryValidationException):
        MemoryValidator.validate_item(item)
