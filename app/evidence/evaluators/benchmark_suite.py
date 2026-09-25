"""
Independent Benchmark Suite for Enterprise AAOS.
Executes micro-benchmarks across every subsystem:
1. Planner & Topological Graph Generation
2. Semantic Reasoner & Deduction Ledger
3. Multi-Critic Reflection Consensus
4. Memory Retrieval & Semantic Fact Indexing
5. Checkpoint Snapshot Serialization & SHA-256 Hashing
6. Adaptive Dynamic Replanning & DAG Mutation
7. Enterprise Event Bus Wildcard Dispatch
8. Distributed Lock Manager Acquisition & Leases
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

from app.evidence.collectors.benchmark_collector import BenchmarkEvidenceCollector, BenchmarkStats
from app.evidence.registry.evidence_models import EvidenceItem
from app.evidence.registry.evidence_registry import EvidenceRegistry

# Subsystem Imports
from app.agents.events.event_bus import EnterpriseEventBus
from app.agents.events.event_types import GoalReceivedEvent
from app.agents.intelligence.goal.goal_specification import GoalSpecification
from app.agents.intelligence.reasoning.semantic_reasoner import SemanticReasoner
from app.agents.memory.intelligence.semantic_memory import SemanticMemory
from app.agents.planning.adaptive.replanning_engine import AdaptiveReplanningEngine
from app.agents.planning.autonomous_planner import AutonomousPlanner
from app.agents.reflection.critics.consensus_evaluator import MultiCriticConsensusEvaluator
from app.agents.runtime.distributed.distributed_lock import DistributedLockManager
from app.agents.workflow.persistence.workflow_checkpoint import TaskGraphSnapshot
from app.agents.workflow.task_graph.dynamic_task_graph import DynamicTaskGraph

logger = logging.getLogger(__name__)


class SubsystemBenchmarkSuite:
    """Runs automated, reproducible micro-benchmarks across all AAOS subsystems."""

    def __init__(self, registry: Optional[EvidenceRegistry] = None) -> None:
        self.registry = registry or EvidenceRegistry()
        self.results: Dict[str, BenchmarkStats] = {}

    async def run_all(self, iterations_per_benchmark: int = 50) -> List[EvidenceItem]:
        """Runs benchmarks across all 8 core subsystems and returns verified EvidenceItems."""
        evidence_items: List[EvidenceItem] = []

        # 1. Planner Benchmark
        b_planner = await self.benchmark_planner(iterations=iterations_per_benchmark)
        evi_planner = BenchmarkEvidenceCollector.create_evidence_item(b_planner, "app.agents.planning.autonomous_planner")
        self.registry.register(evi_planner)
        evidence_items.append(evi_planner)

        # 2. Reasoner Benchmark
        b_reasoner = await self.benchmark_reasoner(iterations=iterations_per_benchmark)
        evi_reasoner = BenchmarkEvidenceCollector.create_evidence_item(b_reasoner, "app.agents.intelligence.reasoning.semantic_reasoner")
        self.registry.register(evi_reasoner)
        evidence_items.append(evi_reasoner)

        # 3. Reflection Consensus Benchmark
        b_reflection = await self.benchmark_reflection(iterations=iterations_per_benchmark)
        evi_reflection = BenchmarkEvidenceCollector.create_evidence_item(b_reflection, "app.agents.reflection.critics.consensus_evaluator")
        self.registry.register(evi_reflection)
        evidence_items.append(evi_reflection)

        # 4. Memory Retrieval Benchmark
        b_memory = await self.benchmark_memory(iterations=iterations_per_benchmark)
        evi_memory = BenchmarkEvidenceCollector.create_evidence_item(b_memory, "app.agents.memory.intelligence.semantic_memory")
        self.registry.register(evi_memory)
        evidence_items.append(evi_memory)

        # 5. Checkpoint Serialization & Hash Benchmark
        b_checkpoint = await self.benchmark_checkpoint(iterations=iterations_per_benchmark)
        evi_checkpoint = BenchmarkEvidenceCollector.create_evidence_item(b_checkpoint, "app.agents.workflow.persistence.workflow_checkpoint")
        self.registry.register(evi_checkpoint)
        evidence_items.append(evi_checkpoint)

        # 6. Adaptive Replanning Benchmark
        b_replanning = await self.benchmark_replanning(iterations=iterations_per_benchmark)
        evi_replanning = BenchmarkEvidenceCollector.create_evidence_item(b_replanning, "app.agents.planning.adaptive.replanning_engine")
        self.registry.register(evi_replanning)
        evidence_items.append(evi_replanning)

        # 7. Event Bus Dispatch Benchmark
        b_eventbus = await self.benchmark_event_bus(iterations=iterations_per_benchmark)
        evi_eventbus = BenchmarkEvidenceCollector.create_evidence_item(b_eventbus, "app.agents.events.event_bus")
        self.registry.register(evi_eventbus)
        evidence_items.append(evi_eventbus)

        # 8. Distributed Lock Manager Benchmark
        b_lock = await self.benchmark_lock_manager(iterations=iterations_per_benchmark)
        evi_lock = BenchmarkEvidenceCollector.create_evidence_item(b_lock, "app.agents.runtime.distributed.distributed_lock")
        self.registry.register(evi_lock)
        evidence_items.append(evi_lock)

        return evidence_items

    async def benchmark_planner(self, iterations: int = 50) -> BenchmarkStats:
        """Benchmarks AutonomousPlanner plan generation and topological sorting."""
        planner = AutonomousPlanner()
        goal = GoalSpecification(goal_id="g_bench", objective="Extract invoice with high accuracy", domain="FINANCIAL")
        latencies: List[float] = []
        failures = 0
        t0 = time.perf_counter()

        for _ in range(iterations):
            s = time.perf_counter()
            try:
                plan = planner.generate_plan(goal)
                if not plan or len(plan.tasks) == 0:
                    failures += 1
            except Exception:
                failures += 1
            latencies.append((time.perf_counter() - s) * 1000.0)

        total_time = time.perf_counter() - t0
        stats = BenchmarkEvidenceCollector.compute_stats("Autonomous Planner", latencies, total_time, failures)
        self.results["planner"] = stats
        return stats

    async def benchmark_reasoner(self, iterations: int = 50) -> BenchmarkStats:
        """Benchmarks SemanticReasoner hypothesis deduction and intent classification."""
        reasoner = SemanticReasoner()
        latencies: List[float] = []
        failures = 0
        t0 = time.perf_counter()

        for _ in range(iterations):
            s = time.perf_counter()
            try:
                res = await reasoner.reason_about_goal("Process MedTech Medical invoice #MED-9021")
                if not res.primary_intent:
                    failures += 1
            except Exception:
                failures += 1
            latencies.append((time.perf_counter() - s) * 1000.0)

        total_time = time.perf_counter() - t0
        stats = BenchmarkEvidenceCollector.compute_stats("Semantic Reasoner", latencies, total_time, failures)
        self.results["reasoner"] = stats
        return stats

    async def benchmark_reflection(self, iterations: int = 50) -> BenchmarkStats:
        """Benchmarks MultiCriticConsensusEvaluator consensus scoring."""
        evaluator = MultiCriticConsensusEvaluator()
        sample_data = {"invoice_number": "INV-100", "subtotal": 100.0, "tax": 10.0, "total_amount": 110.0}
        latencies: List[float] = []
        failures = 0
        t0 = time.perf_counter()

        for _ in range(iterations):
            s = time.perf_counter()
            try:
                res = await evaluator.evaluate_extraction(sample_data, "Process standard invoice")
                if res.overall_score < 0.0:
                    failures += 1
            except Exception:
                failures += 1
            latencies.append((time.perf_counter() - s) * 1000.0)

        total_time = time.perf_counter() - t0
        stats = BenchmarkEvidenceCollector.compute_stats("Multi-Critic Reflection", latencies, total_time, failures)
        self.results["reflection"] = stats
        return stats

    async def benchmark_memory(self, iterations: int = 50) -> BenchmarkStats:
        """Benchmarks SemanticMemory query retrieval."""
        memory = SemanticMemory()
        latencies: List[float] = []
        failures = 0
        t0 = time.perf_counter()

        for _ in range(iterations):
            s = time.perf_counter()
            try:
                results = memory.retrieve_relevant_facts("ACME Corporation tax_id", top_k=3)
                if not results:
                    failures += 1
            except Exception:
                failures += 1
            latencies.append((time.perf_counter() - s) * 1000.0)

        total_time = time.perf_counter() - t0
        stats = BenchmarkEvidenceCollector.compute_stats("Semantic Memory Retrieval", latencies, total_time, failures)
        self.results["memory"] = stats
        return stats

    async def benchmark_checkpoint(self, iterations: int = 50) -> BenchmarkStats:
        """Benchmarks TaskGraphSnapshot creation and SHA-256 state hashing."""
        planner = AutonomousPlanner()
        goal = GoalSpecification(goal_id="g_snap", objective="Process invoice", domain="FINANCIAL")
        plan = planner.generate_plan(goal)
        graph = DynamicTaskGraph.from_execution_plan(plan)

        latencies: List[float] = []
        failures = 0
        t0 = time.perf_counter()

        for i in range(iterations):
            s = time.perf_counter()
            try:
                snap = TaskGraphSnapshot.create(graph, session_id=f"sess_{i}", step_index=i)
                if not snap.state_hash:
                    failures += 1
            except Exception:
                failures += 1
            latencies.append((time.perf_counter() - s) * 1000.0)

        total_time = time.perf_counter() - t0
        stats = BenchmarkEvidenceCollector.compute_stats("Workflow Checkpoint Serialization", latencies, total_time, failures)
        self.results["checkpoint"] = stats
        return stats

    async def benchmark_replanning(self, iterations: int = 50) -> BenchmarkStats:
        """Benchmarks AdaptiveReplanningEngine DAG mutation."""
        engine = AdaptiveReplanningEngine()
        planner = AutonomousPlanner()
        goal = GoalSpecification(goal_id="g_rep", objective="Process invoice", domain="FINANCIAL")
        plan = planner.generate_plan(goal)

        latencies: List[float] = []
        failures = 0
        t0 = time.perf_counter()

        for _ in range(iterations):
            graph = DynamicTaskGraph.from_execution_plan(plan)
            first_task = list(graph._nodes.keys())[0]
            s = time.perf_counter()
            try:
                outcome = engine.evaluate_and_mutate(graph, failed_task_ids=[first_task])
                if not outcome.success:
                    failures += 1
            except Exception:
                failures += 1
            latencies.append((time.perf_counter() - s) * 1000.0)

        total_time = time.perf_counter() - t0
        stats = BenchmarkEvidenceCollector.compute_stats("Adaptive Replanning DAG Mutation", latencies, total_time, failures)
        self.results["replanning"] = stats
        return stats

    async def benchmark_event_bus(self, iterations: int = 50) -> BenchmarkStats:
        """Benchmarks EnterpriseEventBus dispatch."""
        bus = EnterpriseEventBus()
        received = 0

        async def handler(evt: Any) -> None:
            nonlocal received
            received += 1

        bus.subscribe("AgentEvent", handler)
        latencies: List[float] = []
        failures = 0
        t0 = time.perf_counter()

        for i in range(iterations):
            evt = GoalReceivedEvent(execution_id=f"exec_{i}", payload={"step": i})
            s = time.perf_counter()
            try:
                await bus.publish(evt)
            except Exception:
                failures += 1
            latencies.append((time.perf_counter() - s) * 1000.0)

        total_time = time.perf_counter() - t0
        stats = BenchmarkEvidenceCollector.compute_stats("Enterprise Event Bus Dispatch", latencies, total_time, failures)
        self.results["event_bus"] = stats
        return stats

    async def benchmark_lock_manager(self, iterations: int = 50) -> BenchmarkStats:
        """Benchmarks DistributedLockManager lock acquisition and release."""
        mgr = DistributedLockManager()
        latencies: List[float] = []
        failures = 0
        t0 = time.perf_counter()

        for i in range(iterations):
            res_id = f"doc_res_{i}"
            s = time.perf_counter()
            try:
                lease = await mgr.acquire_lock(res_id, "worker_1", ttl_seconds=2.0)
                if not lease:
                    failures += 1
                else:
                    await mgr.release_lock(lease)
            except Exception:
                failures += 1
            latencies.append((time.perf_counter() - s) * 1000.0)

        total_time = time.perf_counter() - t0
        stats = BenchmarkEvidenceCollector.compute_stats("Distributed Lock Manager", latencies, total_time, failures)
        self.results["lock_manager"] = stats
        return stats
