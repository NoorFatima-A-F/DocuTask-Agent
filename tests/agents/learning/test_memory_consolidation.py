"""
Production Tests for Memory Consolidation Intelligence and Dynamic Agent Reputation.
Covers PatternMiner, KnowledgeExtractor, MemoryPromoter, ConsolidationAgent, PerformanceTracker, and ReputationEngine.
"""

import pytest

from app.agents.collaboration.agent_profile import AgentProfile
from app.agents.collaboration.agent_registry import AgentRegistry
from app.agents.collaboration.reputation.agent_metrics import (
    AgentExecutionMetrics,
    RollingPerformanceWindow,
    SingleExecutionOutcome,
)
from app.agents.collaboration.reputation.performance_tracker import PerformanceTracker
from app.agents.collaboration.reputation.reputation_engine import ReputationEngine
from app.agents.memory.consolidation.consolidation_agent import (
    ConsolidationCycleReport,
    MemoryConsolidationAgent,
)
from app.agents.memory.consolidation.knowledge_extractor import (
    ExtractedKnowledgeRule,
    KnowledgeExtractor,
)
from app.agents.memory.consolidation.memory_promoter import MemoryPromoter
from app.agents.memory.consolidation.pattern_miner import MinedPattern, PatternMiner
from app.agents.memory.intelligence.episodic_memory import EpisodeRecord, EpisodicMemory
from app.agents.memory.intelligence.semantic_memory import SemanticFact, SemanticMemory


@pytest.fixture
def sample_episodes() -> list[EpisodeRecord]:
    return [
        EpisodeRecord(
            episode_id="ep-1",
            task_name="table_ocr",
            tools_used=["tesseract_ocr"],
            outcome="FAILURE",
            error_summary="Low contrast table cells",
            metadata={"vendor_name": "Acme Corp"},
            reflection_notes="Vendor Acme Corp places VAT ID in bottom-right corner",
        ),
        EpisodeRecord(
            episode_id="ep-2",
            task_name="table_ocr",
            tools_used=["tesseract_ocr"],
            outcome="FAILURE",
            error_summary="Table boundary missing",
            metadata={"vendor_name": "Acme Corp"},
            reflection_notes="Vendor Acme Corp places VAT ID in bottom-right corner",
        ),
        EpisodeRecord(
            episode_id="ep-3",
            task_name="extract_header",
            tools_used=["pdf_plumber"],
            outcome="SUCCESS",
            metadata={"vendor_name": "Beta Inc"},
        ),
        EpisodeRecord(
            episode_id="ep-4",
            task_name="validate_totals",
            outcome="RECOVERED",
            reflection_notes="Recalculated line items sum to match invoice total",
            metadata={"vendor_name": "Gamma LLC"},
        ),
        EpisodeRecord(
            episode_id="ep-5",
            task_name="validate_totals",
            outcome="RECOVERED",
            reflection_notes="Recalculated line items sum to match invoice total",
            metadata={"vendor_name": "Gamma LLC"},
        ),
    ]


class TestPatternMiner:
    def test_mine_tool_failures(self, sample_episodes):
        miner = PatternMiner(min_support=2)
        patterns = miner.mine_patterns(sample_episodes)
        tool_pat = next((p for p in patterns if p.pattern_type == "TOOL_INEFFICIENCY"), None)
        assert tool_pat is not None
        assert tool_pat.frequency >= 2
        assert "tesseract_ocr" in tool_pat.description
        assert len(tool_pat.supporting_episode_ids) == 2

    def test_mine_vendor_heuristics(self, sample_episodes):
        miner = PatternMiner(min_support=2)
        patterns = miner.mine_patterns(sample_episodes)
        vendor_pat = next((p for p in patterns if p.pattern_type == "VENDOR_HEURISTIC"), None)
        assert vendor_pat is not None
        assert "Acme Corp" in vendor_pat.description
        assert vendor_pat.confidence >= 0.6

    def test_mine_recovery_patterns(self, sample_episodes):
        miner = PatternMiner(min_support=2)
        patterns = miner.mine_patterns(sample_episodes)
        rec_pat = next((p for p in patterns if p.pattern_type == "FAILURE_CORRELATION"), None)
        assert rec_pat is not None
        assert rec_pat.frequency == 2

    def test_min_support_threshold(self, sample_episodes):
        miner_high = PatternMiner(min_support=5)
        patterns = miner_high.mine_patterns(sample_episodes)
        assert len(patterns) == 0


class TestKnowledgeExtractor:
    def test_extract_rules_from_patterns(self):
        extractor = KnowledgeExtractor()
        patterns = [
            MinedPattern(
                pattern_id="pat_1",
                pattern_type="VENDOR_HEURISTIC",
                description="Acme uses custom VAT position",
                frequency=3,
                confidence=0.9,
                attributes={"vendor": "Acme Corp"},
            ),
            MinedPattern(
                pattern_id="pat_2",
                pattern_type="TOOL_INEFFICIENCY",
                description="Tesseract fails on low DPI tables",
                frequency=4,
                confidence=0.92,
                attributes={"tool": "tesseract_ocr", "task": "table_ocr"},
            ),
        ]
        rules = extractor.extract_rules(patterns)
        assert len(rules) == 2
        assert rules[0].subject == "Acme Corp"
        assert rules[0].domain == "DOCUMENT_LAYOUT"
        assert rules[1].subject == "tesseract_ocr"
        assert rules[1].domain == "TOOL_GOVERNANCE"


class TestMemoryPromoter:
    def test_promote_high_confidence_rules(self):
        sem_mem = SemanticMemory()
        promoter = MemoryPromoter(semantic_memory=sem_mem, min_promotion_confidence=0.70)

        rules = [
            ExtractedKnowledgeRule(
                rule_id="r1",
                subject="Acme Corp",
                predicate="tax_location",
                rule_value="bottom_right",
                confidence=0.85,
                tags=["vendor"],
            ),
            ExtractedKnowledgeRule(
                rule_id="r2",
                subject="Uncertain Rule",
                predicate="guess",
                rule_value=None,
                confidence=0.50,  # Below threshold
            ),
        ]

        promoted = promoter.promote_rules(rules)
        assert len(promoted) == 1
        assert promoted[0].subject == "Acme Corp"
        assert "auto_promoted" in promoted[0].tags

        # Query semantic memory to confirm persistence
        facts_with_scores = sem_mem.retrieve_relevant_facts(query="Acme Corp")
        assert any(f.subject == "Acme Corp" for f, _ in facts_with_scores)


class TestMemoryConsolidationAgent:
    def test_end_to_end_consolidation(self, sample_episodes):
        ep_mem = EpisodicMemory()
        for ep in sample_episodes:
            ep_mem.record_episode(ep)

        sem_mem = SemanticMemory()
        agent = MemoryConsolidationAgent(
            episodic_memory=ep_mem,
            semantic_memory=sem_mem,
            pattern_miner=PatternMiner(min_support=2),
        )

        report = agent.run_consolidation(cycle_id="cycle-test-1")
        assert report.cycle_id == "cycle-test-1"
        assert report.episodes_analyzed == 5
        assert report.patterns_mined >= 2
        assert report.rules_extracted >= 2
        assert report.facts_promoted >= 1
        assert len(agent.get_history()) == 1


class TestDynamicAgentReputation:
    def test_rolling_performance_window(self):
        window = RollingPerformanceWindow(capacity=3)
        window.record(SingleExecutionOutcome(task_id="t1", success=False, latency_ms=100.0))
        window.record(SingleExecutionOutcome(task_id="t2", success=True, latency_ms=200.0))
        window.record(SingleExecutionOutcome(task_id="t3", success=True, latency_ms=150.0))

        assert len(window) == 3
        assert window.rolling_success_rate == pytest.approx(2 / 3)
        assert window.rolling_average_latency_ms == pytest.approx(150.0)

        # Eviction test: appending t4 evicts t1 (False), leaving (True, True, True)
        window.record(SingleExecutionOutcome(task_id="t4", success=True, latency_ms=50.0))
        assert len(window) == 3
        assert window.rolling_success_rate == 1.0

    def test_performance_tracker_drift_detection(self):
        tracker = PerformanceTracker(rolling_window_size=10, drift_threshold=0.15)
        agent_id = "agent_drift_test"

        # Baseline: 10 successes
        for i in range(10):
            tracker.record_outcome(agent_id, f"task_{i}", success=True, latency_ms=100.0)

        metrics = tracker.get_metrics(agent_id)
        assert metrics.success_rate == 1.0

        # Inject failures to trigger drift
        for i in range(10, 20):
            tracker.record_outcome(agent_id, f"task_{i}", success=False, latency_ms=100.0)

        drift = tracker.check_drift(agent_id)
        assert drift["has_drift"] is True
        assert "Success rate dropped" in drift["reason"]

    def test_reputation_engine_computation(self):
        tracker = PerformanceTracker()
        registry = AgentRegistry()
        profile = AgentProfile(agent_id="ag_rep", role="Extractor", latency_p95_ms=200.0)
        registry.register(profile)

        engine = ReputationEngine(performance_tracker=tracker, registry=registry)

        # 10 successful executions
        for i in range(10):
            tracker.record_outcome("ag_rep", f"t_{i}", success=True, latency_ms=150.0, accuracy_score=1.0)

        score = engine.compute_reputation_score("ag_rep", baseline_latency_ms=200.0)
        assert 0.90 <= score <= 1.0

        # Sync with profile
        synced_profile = engine.sync_agent_profile("ag_rep")
        assert synced_profile.confidence_rating == score

        # Adjust negotiation bid confidence
        adjusted = engine.adjust_bid_confidence("ag_rep", proposed_confidence=0.85)
        assert adjusted > 0.85

    def test_reputation_unhealthy_transition(self):
        tracker = PerformanceTracker()
        registry = AgentRegistry()
        profile = AgentProfile(agent_id="ag_failing", role="Extractor", is_healthy=True)
        registry.register(profile)

        engine = ReputationEngine(performance_tracker=tracker, registry=registry)

        # 10 failures
        for i in range(10):
            tracker.record_outcome("ag_failing", f"t_{i}", success=False, latency_ms=500.0, accuracy_score=0.0)

        synced = engine.sync_agent_profile("ag_failing")
        assert synced.confidence_rating < 0.50
        assert synced.is_healthy is False

    @pytest.mark.parametrize(
        "n_success,n_fail,expected_min_rep,expected_max_rep",
        [
            (20, 0, 0.95, 1.0),
            (15, 5, 0.65, 0.85),
            (10, 10, 0.40, 0.60),
            (5, 15, 0.20, 0.45),
            (0, 20, 0.0, 0.25),
        ],
    )
    def test_reputation_spectrum_parameterized(self, n_success, n_fail, expected_min_rep, expected_max_rep):
        tracker = PerformanceTracker()
        registry = AgentRegistry()
        agent_id = f"agent_spec_{n_success}_{n_fail}"
        profile = AgentProfile(agent_id=agent_id, role="Processor")
        registry.register(profile)
        engine = ReputationEngine(performance_tracker=tracker, registry=registry)

        for i in range(n_success):
            tracker.record_outcome(agent_id, f"succ_{i}", success=True, latency_ms=100.0, accuracy_score=1.0)
        for i in range(n_fail):
            tracker.record_outcome(agent_id, f"fail_{i}", success=False, latency_ms=400.0, accuracy_score=0.0)

        rep = engine.compute_reputation_score(agent_id, baseline_latency_ms=100.0)
        assert expected_min_rep <= rep <= expected_max_rep

    @pytest.mark.parametrize(
        "raw_bid,rep_score,expected_direction",
        [
            (0.80, 0.95, 1),   # Boosted
            (0.80, 0.80, 0),   # Neutral / minor
            (0.80, 0.30, -1),  # Penalized
            (0.50, 0.98, 1),   # Boosted
            (0.90, 0.20, -1),  # Penalized
        ],
    )
    def test_adjust_bid_confidence_dynamics(self, raw_bid, rep_score, expected_direction):
        tracker = PerformanceTracker()
        registry = AgentRegistry()
        agent_id = f"agent_bid_{rep_score}"
        profile = AgentProfile(agent_id=agent_id, role="Auditor")
        registry.register(profile)
        engine = ReputationEngine(performance_tracker=tracker, registry=registry)

        if rep_score > 0.8:
            for i in range(15):
                tracker.record_outcome(agent_id, f"t_{i}", success=True, latency_ms=80.0, accuracy_score=1.0)
        elif rep_score < 0.5:
            for i in range(15):
                tracker.record_outcome(agent_id, f"t_{i}", success=False, latency_ms=500.0, accuracy_score=0.2)
        else:
            for i in range(10):
                tracker.record_outcome(agent_id, f"t_{i}", success=(i % 2 == 0), latency_ms=120.0, accuracy_score=0.7)

        adjusted = engine.adjust_bid_confidence(agent_id, proposed_confidence=raw_bid)
        if expected_direction > 0:
            assert adjusted >= raw_bid
        elif expected_direction < 0:
            assert adjusted <= raw_bid

    def test_knowledge_extractor_domain_mapping(self):
        extractor = KnowledgeExtractor()
        patterns = [
            MinedPattern(pattern_id="p1", pattern_type="VENDOR_HEURISTIC", description="Vendor X uses OCR template Y", frequency=3, confidence=0.88, attributes={"vendor": "VendorX"}),
            MinedPattern(pattern_id="p2", pattern_type="TOOL_INEFFICIENCY", description="Tool T slow on large PDFs", frequency=4, confidence=0.91, attributes={"tool": "ToolT"}),
            MinedPattern(pattern_id="p3", pattern_type="FAILURE_CORRELATION", description="Failure when DPI < 100", frequency=2, confidence=0.80, attributes={"cause": "low_dpi"}),
        ]
        rules = extractor.extract_rules(patterns)
        assert len(rules) == 3
        assert rules[0].domain == "DOCUMENT_LAYOUT"
        assert rules[1].domain == "TOOL_GOVERNANCE"
        assert rules[2].domain == "RECOVERY"

    def test_consolidation_agent_empty_episodes(self):
        ep_mem = EpisodicMemory()
        sem_mem = SemanticMemory()
        agent = MemoryConsolidationAgent(episodic_memory=ep_mem, semantic_memory=sem_mem)
        report = agent.run_consolidation(cycle_id="empty_cycle")
        assert report.episodes_analyzed == 0
        assert report.patterns_mined == 0
        assert report.facts_promoted == 0

    def test_memory_promoter_deduplication(self):
        sem_mem = SemanticMemory()
        promoter = MemoryPromoter(semantic_memory=sem_mem, min_promotion_confidence=0.60)
        rule1 = ExtractedKnowledgeRule(rule_id="r1", subject="VendorA", predicate="tax_code", rule_value="VAT_STANDARD", confidence=0.9)
        rule2 = ExtractedKnowledgeRule(rule_id="r2", subject="VendorA", predicate="tax_code", rule_value="VAT_STANDARD", confidence=0.95)

        promoted1 = promoter.promote_rules([rule1])
        assert len(promoted1) == 1
        promoted2 = promoter.promote_rules([rule2])
        # Verify persistence and retrieval
        facts = sem_mem.retrieve_relevant_facts("VendorA")
        assert len(facts) >= 1

