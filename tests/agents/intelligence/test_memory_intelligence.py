"""Tests for 4-Tier Memory Intelligence Engine (Phase 25.0).

Covers:
- RetrievalScorer (Similarity, Importance, Recency decay, Task relevance)
- ShortTermMemory (ephemeral scratchpad, eviction, TTL)
- WorkingMemory (session state, goal context, variable/finding/error tracking)
- EpisodicMemory (episode logs, multi-factor ranked retrieval)
- SemanticMemory (domain facts, rules, learned heuristics)
- AgentMemorySystem (unified context assembly, cross-tier promotion and learning)
"""

from __future__ import annotations

import time
import pytest

from app.agents.memory.intelligence import (
    AgentMemorySystem,
    EpisodeRecord,
    EpisodicMemory,
    MemoryContextBundle,
    RetrievalScorer,
    RetrievalScoringConfig,
    SemanticFact,
    SemanticMemory,
    ShortTermMemory,
    WorkingMemory,
)


class TestRetrievalScorer:
    @pytest.fixture
    def scorer(self):
        return RetrievalScorer()

    def test_tokenize(self, scorer):
        tokens = scorer.tokenize("Hello, World! ACME invoice 2026.")
        assert tokens == {"hello", "world", "acme", "invoice", "2026"}

    def test_compute_similarity_identical(self, scorer):
        sim = scorer.compute_similarity("invoice tax", "invoice tax")
        assert sim == 1.0

    def test_compute_similarity_disjoint(self, scorer):
        sim = scorer.compute_similarity("invoice tax", "quantum physics")
        assert sim == 0.0

    def test_compute_similarity_partial(self, scorer):
        sim = scorer.compute_similarity("invoice tax total", "invoice total amount")
        # tokens: {invoice, tax, total} & {invoice, total, amount} = {invoice, total} (2)
        # union = {invoice, tax, total, amount} (4) -> 2/4 = 0.5
        assert sim == 0.5

    def test_compute_similarity_empty(self, scorer):
        assert scorer.compute_similarity("", "some text") == 0.0
        assert scorer.compute_similarity("some text", "") == 0.0

    def test_compute_recency_immediate(self, scorer):
        now = time.time()
        rec = scorer.compute_recency(now, current_time=now)
        assert rec == 1.0

    def test_compute_recency_decay_over_time(self, scorer):
        now = 100000.0
        past = now - 3600.0  # 1 hour ago
        rec = scorer.compute_recency(past, current_time=now)
        assert 0.0 < rec < 1.0

    def test_compute_task_relevance_full_match(self, scorer):
        rel = scorer.compute_task_relevance(["invoice", "sox"], ["invoice", "sox"])
        assert rel == 1.0

    def test_compute_task_relevance_partial_match(self, scorer):
        rel = scorer.compute_task_relevance(["invoice", "other"], ["invoice", "sox"])
        assert rel == 0.5

    def test_compute_task_relevance_empty(self, scorer):
        rel = scorer.compute_task_relevance([], ["invoice"])
        assert rel == 0.2  # baseline

    def test_calculate_score_bounds(self, scorer):
        score = scorer.calculate_score(
            query="invoice",
            memory_content="invoice tax",
            importance=0.8,
            timestamp=time.time(),
            memory_tags=["invoice"],
            current_task_tags=["invoice"],
        )
        assert 0.0 <= score <= 1.0


class TestShortTermMemory:
    def test_get_and_set(self):
        stm = ShortTermMemory()
        stm.set("key1", "val1")
        assert stm.get("key1") == "val1"
        assert stm.get("nonexistent") is None

    def test_delete_and_clear(self):
        stm = ShortTermMemory()
        stm.set("k1", 1)
        stm.set("k2", 2)
        assert stm.delete("k1") is True
        assert stm.delete("k1") is False
        assert stm.get("k1") is None
        stm.clear()
        assert stm.list_keys() == []

    def test_ttl_expiration(self):
        stm = ShortTermMemory()
        stm.set("temp", "data", ttl_seconds=0.05)
        assert stm.get("temp") == "data"
        time.sleep(0.08)
        assert stm.get("temp") is None

    def test_eviction_when_max_entries_exceeded(self):
        stm = ShortTermMemory(max_entries=3)
        stm.set("k1", 1)
        time.sleep(0.01)
        stm.set("k2", 2)
        time.sleep(0.01)
        stm.set("k3", 3)
        time.sleep(0.01)
        # Adding 4th should evict oldest (k1)
        stm.set("k4", 4)
        assert stm.get("k1") is None
        assert stm.get("k2") == 2
        assert stm.get("k3") == 3
        assert stm.get("k4") == 4


class TestWorkingMemory:
    def test_working_memory_state(self):
        wm = WorkingMemory(session_id="sess_1")
        wm.set_goal_context("g_100", "p_100")
        wm.set_current_task("t_ocr")
        wm.update_variable("doc_type", "INVOICE")
        assert wm.get_variable("doc_type") == "INVOICE"
        assert wm.get_variable("unknown", "default") == "default"

    def test_record_findings_and_errors(self):
        wm = WorkingMemory(session_id="sess_1")
        wm.record_finding("vendor", "ACME Corp")
        wm.record_error("t_math", "Mismatch 100+10!=120", details={"diff": 10})

        findings = wm.get_findings()
        assert findings["vendor"] == "ACME Corp"
        errors = wm.get_errors()
        assert len(errors) == 1
        assert errors[0]["task_id"] == "t_math"

    def test_export_snapshot(self):
        wm = WorkingMemory(session_id="sess_snap")
        wm.set_goal_context("g1", "p1")
        wm.update_variable("var1", "val1")
        snap = wm.export_snapshot()
        assert snap["session_id"] == "sess_snap"
        assert snap["goal_id"] == "g1"
        assert snap["variables"]["var1"] == "val1"


class TestEpisodicMemory:
    @pytest.fixture
    def episodic(self):
        return EpisodicMemory()

    def test_record_and_get_episode(self, episodic):
        ep = EpisodeRecord(
            goal_description="Process ACME invoice",
            intent="INVOICE_PROCESSING",
            task_name="t_extract",
            outcome="SUCCESS",
        )
        ep_id = episodic.record_episode(ep)
        assert episodic.count() == 1
        assert episodic.get_episode(ep_id) == ep

    def test_retrieve_relevant_episodes_ranked(self, episodic):
        ep1 = EpisodeRecord(
            goal_description="Process ACME invoice with math validation",
            intent="INVOICE_PROCESSING",
            tags=["invoice", "acme", "math"],
            importance=0.9,
        )
        ep2 = EpisodeRecord(
            goal_description="Audit GDPR compliance on contract",
            intent="COMPLIANCE_AUDIT",
            tags=["contract", "gdpr"],
            importance=0.5,
        )
        episodic.record_episode(ep1)
        episodic.record_episode(ep2)

        results = episodic.retrieve_relevant_episodes("invoice math acme", task_tags=["invoice"], top_k=2)
        assert len(results) >= 1
        top_ep, top_score = results[0]
        assert top_ep == ep1
        assert top_score > 0.4


class TestSemanticMemory:
    @pytest.fixture
    def semantic(self):
        return SemanticMemory()

    def test_default_facts_seeded(self, semantic):
        assert semantic.count() >= 4
        # ACME, standard invoice rule, SOX, Tesseract heuristic
        facts = semantic.retrieve_relevant_facts("SOX compliance audit", top_k=5)
        subjects = [f.subject for f, _ in facts]
        assert "SOX Compliance Standard" in subjects

    def test_store_and_retrieve_custom_fact(self, semantic):
        fact = SemanticFact(
            subject="VendorXYZ",
            predicate="discount_rate",
            fact_value=0.05,
            tags=["vendorxyz", "discount"],
        )
        fid = semantic.store_fact(fact)
        assert semantic.get_fact(fid) == fact

        matches = semantic.retrieve_relevant_facts("VendorXYZ discount", task_tags=["vendorxyz"], top_k=1)
        assert len(matches) == 1
        assert matches[0][0].subject == "VendorXYZ"


class TestAgentMemorySystem:
    @pytest.fixture
    def memory_system(self):
        return AgentMemorySystem(session_id="unified_session")

    def test_assemble_context_bundle(self, memory_system):
        memory_system.short_term.set("token_buf", "123")
        memory_system.working.set_goal_context("g_active", "p_active")

        bundle = memory_system.assemble_context_bundle("invoice total", task_tags=["invoice"])
        assert isinstance(bundle, MemoryContextBundle)
        assert bundle.working_context["goal_id"] == "g_active"
        assert "token_buf" in bundle.scratchpad_summary
        assert len(bundle.relevant_facts) >= 1

    def test_finalize_and_learn_promotion(self, memory_system):
        memory_system.working.record_error("t_math", "Calculated total mismatch")
        new_fact = SemanticFact(
            subject="Supplier123",
            predicate="vat_rate",
            fact_value=0.20,
            tags=["supplier123", "vat"],
        )

        ep_id = memory_system.finalize_and_learn(
            goal_description="Process supplier invoice",
            intent="INVOICE_PROCESSING",
            outcome="RECOVERED",
            reflection_notes="Corrected total by applying 20% VAT",
            learned_facts=[new_fact],
        )

        assert ep_id.startswith("ep_")
        assert memory_system.episodic.count() == 1
        ep = memory_system.episodic.get_episode(ep_id)
        assert ep.outcome == "RECOVERED"
        assert "Calculated total mismatch" in ep.error_summary

        # Check fact was stored in semantic memory
        facts = memory_system.semantic.retrieve_relevant_facts("Supplier123 vat rate")
        assert any(f.subject == "Supplier123" for f, _ in facts)


class TestExpandedMemoryScenarios:
    def test_custom_scoring_config(self):
        config = RetrievalScoringConfig(
            w_similarity=0.50,
            w_importance=0.20,
            w_recency=0.15,
            w_task_relevance=0.15,
        )
        scorer = RetrievalScorer(config)
        assert scorer.config.w_similarity == 0.50
        assert scorer.config.w_importance == 0.20

    def test_similarity_case_insensitivity(self):
        scorer = RetrievalScorer()
        sim1 = scorer.compute_similarity("INVOICE TAX", "invoice tax")
        assert sim1 == 1.0

    def test_similarity_punctuation_stripping(self):
        scorer = RetrievalScorer()
        sim = scorer.compute_similarity("invoice, tax! (total)", "invoice tax total")
        assert sim == 1.0

    def test_zero_decay_lambda(self):
        config = RetrievalScoringConfig(recency_decay_lambda=0.0)
        scorer = RetrievalScorer(config)
        # With lambda=0, exp(0) = 1.0 regardless of time delta
        rec = scorer.compute_recency(time.time() - 100000.0)
        assert rec == 1.0

    def test_short_term_memory_default_max_entries(self):
        stm = ShortTermMemory()
        assert stm.max_entries == 1000

    def test_short_term_memory_list_keys_order(self):
        stm = ShortTermMemory()
        stm.set("a", 1)
        stm.set("b", 2)
        keys = set(stm.list_keys())
        assert keys == {"a", "b"}

    def test_working_memory_multiple_errors(self):
        wm = WorkingMemory(session_id="sess_err")
        for i in range(5):
            wm.record_error(f"task_{i}", f"Error {i}")
        assert len(wm.get_errors()) == 5
        assert wm.get_errors()[2]["task_id"] == "task_2"

    def test_working_memory_variables_overwrite(self):
        wm = WorkingMemory(session_id="sess_var")
        wm.update_variable("step", 1)
        assert wm.get_variable("step") == 1
        wm.update_variable("step", 2)
        assert wm.get_variable("step") == 2

    def test_episodic_memory_retrieve_empty_query(self):
        em = EpisodicMemory()
        ep = EpisodeRecord(goal_description="Process file", importance=0.8)
        em.record_episode(ep)
        # Even with empty query, importance and recency give baseline score
        res = em.retrieve_relevant_episodes("", min_score=0.1)
        assert len(res) == 1

    def test_episodic_memory_top_k_bounds(self):
        em = EpisodicMemory()
        for i in range(10):
            em.record_episode(EpisodeRecord(goal_description=f"Task {i}", tags=["batch"]))
        res = em.retrieve_relevant_episodes("Task", task_tags=["batch"], top_k=3)
        assert len(res) == 3

    def test_semantic_memory_domains(self):
        sm = SemanticMemory()
        f1 = SemanticFact(subject="S1", predicate="P1", domain="LEGAL", tags=["law"])
        f2 = SemanticFact(subject="S2", predicate="P2", domain="TAX", tags=["tax"])
        sm.store_fact(f1)
        sm.store_fact(f2)
        legal_facts = sm.retrieve_relevant_facts("law", task_tags=["law"])
        assert any(f.subject == "S1" for f, _ in legal_facts)

    def test_semantic_fact_to_searchable_text(self):
        fact = SemanticFact(
            subject="VendorA",
            predicate="country",
            fact_value="DE",
            domain="VENDOR",
            tags=["europe", "eu"],
        )
        text = fact.to_searchable_text()
        assert "VendorA" in text
        assert "country" in text
        assert "DE" in text
        assert "VENDOR" in text
        assert "europe" in text

    def test_episode_record_to_searchable_text(self):
        ep = EpisodeRecord(
            goal_description="Goal X",
            intent="INTENT_Y",
            task_name="Task Z",
            agent_id="Agent W",
            outcome="RECOVERED",
            error_summary="Timeout error",
            reflection_notes="Switched to async",
            tags=["resilience"],
        )
        text = ep.to_searchable_text()
        assert "Goal X" in text
        assert "Timeout error" in text
        assert "Switched to async" in text
        assert "resilience" in text

    def test_agent_memory_system_empty_search(self):
        sys_mem = AgentMemorySystem(session_id="empty_search_sess")
        bundle = sys_mem.assemble_context_bundle("random nonexistent phrase xyz")
        assert bundle.working_context["session_id"] == "empty_search_sess"

    @pytest.mark.parametrize("outcome", ["SUCCESS", "FAILURE", "RECOVERED"])
    def test_finalize_and_learn_all_outcomes(self, outcome):
        sys_mem = AgentMemorySystem(session_id=f"sess_{outcome}")
        ep_id = sys_mem.finalize_and_learn(
            goal_description="Goal",
            intent="INVOICE_PROCESSING",
            outcome=outcome,
        )
        assert sys_mem.episodic.get_episode(ep_id).outcome == outcome

    def test_importance_bounds_in_scorer(self):
        scorer = RetrievalScorer()
        # importance clamped to [0, 1]
        s_low = scorer.calculate_score("q", "d", -5.0, time.time(), [], [])
        s_high = scorer.calculate_score("q", "d", 5.0, time.time(), [], [])
        assert s_low >= 0.0
        assert s_high <= 1.0

    def test_task_relevance_case_insensitive(self):
        scorer = RetrievalScorer()
        rel = scorer.compute_task_relevance(["INVOICE", "SOX"], ["invoice", "sox"])
        assert rel == 1.0

    def test_working_memory_findings_overwrite(self):
        wm = WorkingMemory(session_id="wm_f")
        wm.record_finding("vendor", "ACME 1")
        wm.record_finding("vendor", "ACME 2")
        assert wm.get_findings()["vendor"] == "ACME 2"

    def test_short_term_memory_delete_nonexistent_returns_false(self):
        stm = ShortTermMemory()
        assert stm.delete("not_there") is False

