"""
Test suite for Forensic AAOS Cognitive & Architectural Evolution modules:
1. Cognitive Memory Evolution Engine (Decay, Contradictions, Deduplication)
2. Tree-of-Thought Explorer & Counterfactual Reasoner
3. CNCF CloudEvents 1.0 Formatter & W3C Distributed Tracing
4. OpenTelemetry Tracing Bridge & SLO Metrics
"""

import time

from app.agents.events.cloudevents_formatter import CloudEventsFormatter
from app.agents.events.event_types import GoalReceivedEvent
from app.agents.intelligence.reasoning.counterfactual_reasoner import TreeOfThoughtExplorer
from app.agents.memory.intelligence.cognitive_memory_evolution import (
    CognitiveMemoryEvolutionEngine,
)
from app.agents.memory.intelligence.semantic_memory import SemanticFact, SemanticMemory
from app.agents.runtime.cloud.opentelemetry_bridge import OpenTelemetryBridge


def test_cognitive_memory_evolution_deduplication():
    """Test merging and deduplication of redundant semantic facts."""
    mem = SemanticMemory()
    engine = CognitiveMemoryEvolutionEngine()

    f1 = SemanticFact(subject="VendorX", predicate="tax_id", fact_value="111-222", confidence=0.8, tags=["tag1"])
    f2 = SemanticFact(subject="VendorX", predicate="tax_id", fact_value="111-222", confidence=0.9, tags=["tag2"])
    mem.store_fact(f1)
    mem.store_fact(f2)

    deduped = engine.deduplicate_facts(mem)
    assert deduped == 1
    remaining = [f for f in mem._facts.values() if f.subject == "VendorX"]
    assert len(remaining) == 1
    assert remaining[0].confidence == 0.9
    assert "tag1" in remaining[0].tags and "tag2" in remaining[0].tags


def test_cognitive_memory_contradiction_detection():
    """Test detecting conflicting facts and preferring higher confidence."""
    mem = SemanticMemory()
    engine = CognitiveMemoryEvolutionEngine()

    f_old = SemanticFact(subject="AlphaCorp", predicate="address", fact_value="100 Main St", confidence=0.6)
    f_new = SemanticFact(subject="AlphaCorp", predicate="address", fact_value="200 Broadway", confidence=0.95)
    mem.store_fact(f_old)
    mem.store_fact(f_new)

    reports = engine.detect_and_resolve_contradictions(mem)
    assert len(reports) == 1
    assert reports[0].subject == "alphacorp"
    assert reports[0].resolution_applied == "PREFER_HIGHER_CONFIDENCE"
    assert reports[0].resolved_value == "200 Broadway"


def test_cognitive_memory_temporal_decay():
    """Test exponential temporal decay on unverified facts."""
    mem = SemanticMemory()
    engine = CognitiveMemoryEvolutionEngine(decay_half_life_days=1.0)

    now = time.time()
    # Fact created 2 days ago (2 half-lives -> confidence should drop to ~0.25 of original)
    f_old = SemanticFact(subject="BetaCorp", predicate="discount", fact_value="10%", confidence=0.8, created_at=now - (2 * 86400))
    # Verified ground truth fact (confidence=1.0) should NOT decay
    f_ground = SemanticFact(subject="BetaCorp", predicate="tax_id", fact_value="999-888", confidence=1.0, created_at=now - (2 * 86400))
    mem.store_fact(f_old)
    mem.store_fact(f_ground)

    decayed_count = engine.apply_temporal_decay(mem, current_time=now)
    assert decayed_count >= 1
    assert mem.get_fact(f_old.fact_id).confidence < 0.40
    assert mem.get_fact(f_ground.fact_id).confidence == 1.0


def test_tree_of_thought_counterfactual_explorer():
    """Test multi-branch exploration and Pareto utility scoring."""
    explorer = TreeOfThoughtExplorer()
    report = explorer.explore_hypotheses(
        goal_description="Extract complex multi-table financial statement",
        available_tools=["tesseract_ocr", "advanced_vision_ocr", "llm_extractor"],
        constraints={"max_cost_usd": 0.05, "max_latency_ms": 1000.0},
    )

    assert report.total_simulated_paths == 3
    assert report.winning_branch is not None
    assert report.winning_branch.utility_score > 0.0
    assert report.decision_confidence > 0.50
    assert "Selected" in report.rationale


def test_cloudevents_formatter_and_w3c_tracing():
    """Test CNCF CloudEvents 1.0 serialization and W3C traceparent formatting."""
    event = GoalReceivedEvent(
        execution_id="exec_777",
        trace_id="4bf92f3577b34da6a3ce929d0e0e4736",
        payload={"goal": "Process balance sheet"},
    )
    ce = CloudEventsFormatter.from_agent_event(event)

    assert ce.specversion == "1.0"
    assert ce.type == "com.google.aaos.event.goalreceived"
    assert "4bf92f3577b34da6a3ce929d0e0e4736" in ce.traceparent
    assert ce.idempotencykey is not None

    ce_dict = ce.to_dict()
    assert CloudEventsFormatter.validate_cloudevent(ce_dict) is True


def test_opentelemetry_bridge_and_slo_snapshot():
    """Test span lifecycle and SLO calculation."""
    bridge = OpenTelemetryBridge()
    span1 = bridge.start_span("goal_parsing", attributes={"phase": "understanding"})
    time.sleep(0.01)
    bridge.end_span(span1, status="OK")

    span2 = bridge.start_span("tool_execution", attributes={"tool": "ocr"})
    bridge.end_span(span2, status="ERROR", error=RuntimeError("OCR failure"))

    assert len(bridge.finished_spans) == 2
    snapshot = bridge.get_slo_snapshot()
    assert snapshot.total_requests == 2
    assert snapshot.failed_requests == 1
    assert snapshot.current_availability_pct == 50.0
    assert snapshot.p95_latency_ms > 0.0
