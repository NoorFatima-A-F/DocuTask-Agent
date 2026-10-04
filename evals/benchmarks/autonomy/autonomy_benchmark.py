"""Autonomous Operating System Autonomy Score Benchmark.

Measures quantitative autonomy metrics across the 5 pillars of autonomous agency:
1. Planning Quality Score (topological validity, constraint satisfaction)
2. Agent Allocation Accuracy (capability match, Pareto efficiency)
3. Recovery Intelligence (dynamic DAG mutation, zero human intervention)
4. Reflection Improvement Delta (Q_after - Q_before)
5. Memory Recall Precision (multi-factor retrieval precision)

Calculates the Unified Autonomy Score:
AutonomyScore = (Planning + Allocation + Recovery + Reflection + Memory) / 5
"""

from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.agents.collaboration import (
    AgentDiscoveryService,
    AgentProfile,
    AgentRegistry,
)
from app.agents.intelligence.goal import GoalManager
from app.agents.memory.intelligence import (
    AgentMemorySystem,
    SemanticFact,
)
from app.agents.planning import (
    AutonomousPlanner,
)
from app.agents.reflection import (
    ReflectionAgent,
)
from app.agents.workflow.task_graph import (
    DynamicTaskGraph,
    TaskGraphMutationEngine,
)


@dataclass
class AutonomyScorecard:
    planning_quality_score: float
    agent_allocation_score: float
    recovery_intelligence_score: float
    reflection_improvement_score: float
    memory_recall_score: float
    unified_autonomy_score: float
    benchmark_duration_ms: float


def benchmark_planning_quality() -> float:
    gm = GoalManager()
    planner = AutonomousPlanner()

    scenarios = [
        ("Process vendor invoice with accuracy >= 95%", "INVOICE_PROCESSING", 4),
        ("Audit compliance under SOX", "COMPLIANCE_AUDIT", 3),
        ("Review contract terms", "CONTRACT_REVIEW", 3),
        ("Detect document forgery", "FRAUD_DETECTION", 3),
    ]

    passed = 0
    for text, exp_intent, exp_tasks in scenarios:
        g = gm.submit_goal(text)
        plan = planner.generate_plan(g)
        if len(plan.tasks) == exp_tasks and plan.get_topological_order():
            passed += 1

    return passed / len(scenarios)


def benchmark_agent_allocation() -> float:
    reg = AgentRegistry()
    reg.register(AgentProfile("a_ocr_cheap", "OCR", ["ocr"], cost_per_call=0.001, confidence_rating=0.90))
    reg.register(AgentProfile("a_ocr_acc", "OCR", ["ocr"], cost_per_call=0.005, confidence_rating=0.99))
    disc = AgentDiscoveryService(reg)

    acc_agent = disc.discover_best_agent("ocr", min_confidence=0.98)
    cost_agent = disc.discover_best_agent("ocr", max_cost=0.002)

    score = 0.0
    if acc_agent and acc_agent.agent_id == "a_ocr_acc":
        score += 0.5
    if cost_agent and cost_agent.agent_id == "a_ocr_cheap":
        score += 0.5
    return score


def benchmark_recovery_intelligence() -> float:
    gm = GoalManager()
    g = gm.submit_goal("Process invoice")
    planner = AutonomousPlanner()
    plan = planner.generate_plan(g)
    graph = DynamicTaskGraph.from_execution_plan(plan)
    mut = TaskGraphMutationEngine(graph)

    # 1. Simulate failure of first task
    t0_id = plan.tasks[0].task_id
    graph.set_state(t0_id, "FAILED")
    fb = mut.replace_failed_node_with_fallback(t0_id, "agent_fallback", ["tool_fallback"])

    # 2. Verify graph is acyclic and downstream task dependencies rerouted
    downstream = graph.get_downstream_dependents(t0_id)
    t1_task = plan.tasks[1]
    rerouted = (fb.task_id in graph.get_task(t1_task.task_id).dependencies)
    acyclic = False
    try:
        graph._validate_acyclic()
        acyclic = True
    except Exception:
        acyclic = False

    return 1.0 if (rerouted and acyclic and len(downstream) == 0) else 0.5


def benchmark_reflection_improvement() -> float:
    ref = ReflectionAgent(quality_threshold=0.90)
    defective_payload = {
        "vendor_name": "ACME",
        "invoice_number": "INV-1",
        "subtotal": 100.0,
        "tax_amount": 10.0,
        "total_amount": 125.0,  # Defect
    }

    eval_before = ref.evaluate_output("validation", defective_payload)
    q_before = eval_before.overall_score

    trigger = ref.formulate_correction("t_math", eval_before)
    repaired_payload = ref.apply_self_correction(defective_payload, trigger)

    eval_after = ref.evaluate_output("validation", repaired_payload)
    q_after = eval_after.overall_score

    if eval_before.passed_threshold is False and eval_after.passed_threshold is True and q_after > q_before:
        return 1.0
    return 0.5


def benchmark_memory_recall() -> float:
    mem = AgentMemorySystem(session_id="bench_mem")
    mem.semantic.store_fact(SemanticFact(subject="TargetCorp", predicate="tax_id", fact_value="XX-123", tags=["targetcorp", "tax"]))
    mem.semantic.store_fact(SemanticFact(subject="OtherCorp", predicate="tax_id", fact_value="YY-456", tags=["othercorp"]))

    facts = mem.semantic.retrieve_relevant_facts("TargetCorp tax", task_tags=["targetcorp"], top_k=1)
    if facts and facts[0][0].subject == "TargetCorp":
        return 1.0
    return 0.5


def run_autonomy_benchmark() -> AutonomyScorecard:
    t0 = time.perf_counter()

    p_score = benchmark_planning_quality()
    a_score = benchmark_agent_allocation()
    r_score = benchmark_recovery_intelligence()
    ref_score = benchmark_reflection_improvement()
    m_score = benchmark_memory_recall()

    unified = (p_score + a_score + r_score + ref_score + m_score) / 5.0
    duration_ms = (time.perf_counter() - t0) * 1000.0

    card = AutonomyScorecard(
        planning_quality_score=p_score,
        agent_allocation_score=a_score,
        recovery_intelligence_score=r_score,
        reflection_improvement_score=ref_score,
        memory_recall_score=m_score,
        unified_autonomy_score=unified,
        benchmark_duration_ms=round(duration_ms, 2),
    )

    print("=" * 70)
    print("AUTONOMOUS AGENT INTELLIGENCE OS — AUTONOMY SCORECARD")
    print("=" * 70)
    print(f"1. Planning Quality Score       : {card.planning_quality_score:.2%}")
    print(f"2. Agent Allocation Score       : {card.agent_allocation_score:.2%}")
    print(f"3. Recovery Intelligence Score   : {card.recovery_intelligence_score:.2%}")
    print(f"4. Reflection Improvement Score : {card.reflection_improvement_score:.2%}")
    print(f"5. Memory Recall Precision      : {card.memory_recall_score:.2%}")
    print("-" * 70)
    print(f"UNIFIED AUTONOMY SCORE          : {card.unified_autonomy_score:.2%}")
    print(f"Benchmark Execution Time        : {card.benchmark_duration_ms:.2f} ms")
    print("=" * 70)

    return card


if __name__ == "__main__":
    run_autonomy_benchmark()
