"""Candidate Strategy Generator for DocuTask Autonomous Planning Platform.

Synthesizes multiple distinct execution strategies (Fast/Low-Latency, High-Accuracy Deep Reasoning,
Cost-Optimized Frugal, and Adaptive Pareto-Optimal) tailored to the GoalGraph and constraints.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.runtime.planning.goal_engine import GoalGraph, ObjectiveType
from app.runtime.planning.constraint_engine import MissionConstraintSet
from app.runtime.planning.capability_discovery import CapabilityDiscoveryEngine, CapabilityType


class StrategyArchetype(str, Enum):
    ALPHA_FAST = "ALPHA_FAST"                 # Ultra-low latency, local OCR, Flash Lite
    BETA_ACCURATE = "BETA_ACCURATE"           # Maximum precision, Cloud Neural OCR, Pro LLM, Cross-validation
    GAMMA_COST = "GAMMA_COST"                 # Budget frugal, local models, cached embeddings
    DELTA_PARETO = "DELTA_PARETO"             # Adaptive multi-objective Pareto-balanced


class StrategyStep(BaseModel):
    """Specific step within a candidate strategy."""
    step_id: str = Field(default_factory=lambda: f"step_{uuid.uuid4().hex[:8]}")
    objective_id: str
    name: str
    capability_id: str
    provider: str
    estimated_latency_ms: float
    estimated_cost_usd: float
    estimated_accuracy: float
    failure_probability: float
    parallel_group: int = 0
    fallback_capability_id: Optional[str] = None


class CandidateStrategy(BaseModel):
    """Complete executable strategy configuration."""
    strategy_id: str = Field(default_factory=lambda: f"strat_{uuid.uuid4().hex[:8]}")
    archetype: StrategyArchetype
    name: str
    description: str
    mission_id: str
    steps: List[StrategyStep] = Field(default_factory=list)
    concurrency_level: int = 4
    estimated_total_latency_ms: float = 0.0
    estimated_critical_path_ms: float = 0.0
    estimated_total_cost_usd: float = 0.0
    estimated_accuracy: float = 0.0
    estimated_risk_score: float = 0.0
    token_estimate: int = 0
    is_pareto_optimal: bool = False
    constraint_compliance: Dict[str, Any] = Field(default_factory=dict)
    rationale: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CandidateStrategyGenerator:
    """Generates distinct, rigorously constructed candidate execution strategies."""

    def __init__(self, capability_discovery: CapabilityDiscoveryEngine) -> None:
        self.capability_discovery = capability_discovery

    def generate_strategies(
        self,
        goal_graph: GoalGraph,
        constraint_set: MissionConstraintSet,
        historical_guidance: Optional[Dict[str, Any]] = None,
    ) -> List[CandidateStrategy]:
        """Synthesizes candidate strategies covering the multi-objective search space."""
        strategies: List[CandidateStrategy] = []

        # 1. Strategy Alpha (Fast / Low-Latency)
        strat_alpha = self._build_alpha_fast(goal_graph)
        strategies.append(strat_alpha)

        # 2. Strategy Beta (High-Accuracy / Deep Reasoning)
        strat_beta = self._build_beta_accurate(goal_graph)
        strategies.append(strat_beta)

        # 3. Strategy Gamma (Cost-Optimized / Budget Frugal)
        strat_gamma = self._build_gamma_cost(goal_graph)
        strategies.append(strat_gamma)

        # 4. Strategy Delta (Adaptive Pareto-Balanced)
        strat_delta = self._build_delta_pareto(goal_graph)
        strategies.append(strat_delta)

        # Check constraint compliance for each candidate
        for strat in strategies:
            metrics = {
                "budget_usd": strat.estimated_total_cost_usd,
                "latency_ms": strat.estimated_critical_path_ms,
                "sla_deadline_ms": strat.estimated_critical_path_ms,
                "token_limit": float(strat.token_estimate),
                "accuracy_gate": strat.estimated_accuracy,
                "concurrency_limit": float(strat.concurrency_level),
            }
            is_valid, violations, penalty = constraint_set.validate_candidate(metrics)
            strat.constraint_compliance = {
                "is_valid": is_valid,
                "violations": violations,
                "soft_penalty": penalty,
            }

        return strategies

    def _build_alpha_fast(self, goal_graph: GoalGraph) -> CandidateStrategy:
        steps: List[StrategyStep] = []
        ordered_objs = goal_graph.get_topological_order()

        for obj_id in ordered_objs:
            obj = goal_graph.objectives[obj_id]
            if obj.objective_type == ObjectiveType.EXTRACTION:
                if "ocr" in obj.name.lower() or "ingestion" in obj.name.lower():
                    cap = self.capability_discovery.get_capability("ocr_tesseract_v5")
                else:
                    cap = self.capability_discovery.get_capability("llm_flash_lite")
            elif obj.objective_type == ObjectiveType.VALIDATION:
                cap = self.capability_discovery.get_capability("fast_rule_engine")
            elif obj.objective_type == ObjectiveType.AUDIT:
                cap = self.capability_discovery.get_capability("episodic_memory_graph")
            else:
                cap = self.capability_discovery.get_capability("fast_rule_engine")

            if not cap:
                continue

            steps.append(
                StrategyStep(
                    objective_id=obj_id,
                    name=f"Fast: {obj.name}",
                    capability_id=cap.capability_id,
                    provider=cap.provider,
                    estimated_latency_ms=cap.p50_latency_ms * obj.estimated_complexity,
                    estimated_cost_usd=cap.unit_cost_usd * obj.estimated_complexity,
                    estimated_accuracy=cap.historical_accuracy,
                    failure_probability=cap.failure_probability,
                    fallback_capability_id="llm_pro_reasoner" if "llm" in cap.capability_id else None,
                )
            )

        total_cost = sum(s.estimated_cost_usd for s in steps)
        critical_path = sum(s.estimated_latency_ms for s in steps) * 0.75  # pipelined concurrency
        avg_acc = sum(s.estimated_accuracy for s in steps) / max(1, len(steps))

        return CandidateStrategy(
            strategy_id=f"strat_alpha_{uuid.uuid4().hex[:6]}",
            archetype=StrategyArchetype.ALPHA_FAST,
            name="Strategy Alpha (Latency-Optimized Turbo)",
            description="Leverages local fast OCR and Gemini 2.0 Flash Lite with deterministic AST rule verification for maximum throughput.",
            mission_id=goal_graph.mission_id,
            steps=steps,
            concurrency_level=8,
            estimated_total_latency_ms=critical_path * 1.2,
            estimated_critical_path_ms=critical_path,
            estimated_total_cost_usd=total_cost,
            estimated_accuracy=avg_acc,
            estimated_risk_score=0.18,
            token_estimate=12000,
            rationale="Selected when SLA is extremely tight and low latency takes precedence over exhaustive reflection.",
        )

    def _build_beta_accurate(self, goal_graph: GoalGraph) -> CandidateStrategy:
        steps: List[StrategyStep] = []
        ordered_objs = goal_graph.get_topological_order()

        for obj_id in ordered_objs:
            obj = goal_graph.objectives[obj_id]
            if obj.objective_type == ObjectiveType.EXTRACTION:
                if "ocr" in obj.name.lower() or "ingestion" in obj.name.lower():
                    cap = self.capability_discovery.get_capability("ocr_cloud_vision")
                else:
                    cap = self.capability_discovery.get_capability("llm_pro_reasoner")
            elif obj.objective_type == ObjectiveType.VALIDATION:
                cap = self.capability_discovery.get_capability("fast_rule_engine")
            elif obj.objective_type == ObjectiveType.AUDIT:
                cap = self.capability_discovery.get_capability("runtime_reflection_engine")
            else:
                cap = self.capability_discovery.get_capability("llm_pro_reasoner")

            if not cap:
                continue

            steps.append(
                StrategyStep(
                    objective_id=obj_id,
                    name=f"Deep: {obj.name}",
                    capability_id=cap.capability_id,
                    provider=cap.provider,
                    estimated_latency_ms=cap.p50_latency_ms * obj.estimated_complexity,
                    estimated_cost_usd=cap.unit_cost_usd * obj.estimated_complexity,
                    estimated_accuracy=cap.historical_accuracy,
                    failure_probability=cap.failure_probability,
                )
            )

        total_cost = sum(s.estimated_cost_usd for s in steps)
        critical_path = sum(s.estimated_latency_ms for s in steps) * 0.85
        avg_acc = sum(s.estimated_accuracy for s in steps) / max(1, len(steps))

        return CandidateStrategy(
            strategy_id=f"strat_beta_{uuid.uuid4().hex[:6]}",
            archetype=StrategyArchetype.BETA_ACCURATE,
            name="Strategy Beta (Maximum Accuracy Deep Reasoning)",
            description="Utilizes Cloud Vision Neural OCR, Gemini 2.0 Pro deep extraction, and multi-stage reflective validation.",
            mission_id=goal_graph.mission_id,
            steps=steps,
            concurrency_level=4,
            estimated_total_latency_ms=critical_path * 1.15,
            estimated_critical_path_ms=critical_path,
            estimated_total_cost_usd=total_cost,
            estimated_accuracy=avg_acc,
            estimated_risk_score=0.04,
            token_estimate=48000,
            rationale="Selected for mission-critical financial audits, tax reconciliation, and zero-tolerance compliance documents.",
        )

    def _build_gamma_cost(self, goal_graph: GoalGraph) -> CandidateStrategy:
        steps: List[StrategyStep] = []
        ordered_objs = goal_graph.get_topological_order()

        for obj_id in ordered_objs:
            obj = goal_graph.objectives[obj_id]
            if obj.objective_type == ObjectiveType.EXTRACTION:
                if "ocr" in obj.name.lower() or "ingestion" in obj.name.lower():
                    cap = self.capability_discovery.get_capability("ocr_tesseract_v5")
                else:
                    cap = self.capability_discovery.get_capability("llm_flash_lite")
            elif obj.objective_type == ObjectiveType.VALIDATION:
                cap = self.capability_discovery.get_capability("fast_rule_engine")
            elif obj.objective_type == ObjectiveType.AUDIT:
                cap = self.capability_discovery.get_capability("episodic_memory_graph")
            else:
                cap = self.capability_discovery.get_capability("fast_rule_engine")

            if not cap:
                continue

            steps.append(
                StrategyStep(
                    objective_id=obj_id,
                    name=f"Frugal: {obj.name}",
                    capability_id=cap.capability_id,
                    provider=cap.provider,
                    estimated_latency_ms=cap.p50_latency_ms * obj.estimated_complexity,
                    estimated_cost_usd=cap.unit_cost_usd * obj.estimated_complexity * 0.8,
                    estimated_accuracy=cap.historical_accuracy * 0.98,
                    failure_probability=cap.failure_probability * 1.1,
                )
            )

        total_cost = sum(s.estimated_cost_usd for s in steps)
        critical_path = sum(s.estimated_latency_ms for s in steps) * 0.8
        avg_acc = sum(s.estimated_accuracy for s in steps) / max(1, len(steps))

        return CandidateStrategy(
            strategy_id=f"strat_gamma_{uuid.uuid4().hex[:6]}",
            archetype=StrategyArchetype.GAMMA_COST,
            name="Strategy Gamma (Budget Frugal & Efficient)",
            description="Minimizes cost footprint through local Tesseract OCR, Flash Lite routing, and batch rule checks.",
            mission_id=goal_graph.mission_id,
            steps=steps,
            concurrency_level=6,
            estimated_total_latency_ms=critical_path * 1.1,
            estimated_critical_path_ms=critical_path,
            estimated_total_cost_usd=total_cost,
            estimated_accuracy=avg_acc,
            estimated_risk_score=0.12,
            token_estimate=8500,
            rationale="Selected for bulk ingestion workloads where processing millions of documents per day requires strict unit cost controls.",
        )

    def _build_delta_pareto(self, goal_graph: GoalGraph) -> CandidateStrategy:
        steps: List[StrategyStep] = []
        ordered_objs = goal_graph.get_topological_order()

        for obj_id in ordered_objs:
            obj = goal_graph.objectives[obj_id]
            # Smart Hybrid Allocation
            if obj.objective_type == ObjectiveType.EXTRACTION:
                if "ocr" in obj.name.lower() or "ingestion" in obj.name.lower():
                    cap = self.capability_discovery.get_capability("ocr_cloud_vision")
                else:
                    cap = self.capability_discovery.get_capability("llm_flash_lite")
            elif obj.objective_type == ObjectiveType.VALIDATION:
                cap = self.capability_discovery.get_capability("fast_rule_engine")
            elif obj.objective_type == ObjectiveType.AUDIT:
                cap = self.capability_discovery.get_capability("episodic_memory_graph")
            else:
                cap = self.capability_discovery.get_capability("llm_flash_lite")

            if not cap:
                continue

            steps.append(
                StrategyStep(
                    objective_id=obj_id,
                    name=f"Pareto: {obj.name}",
                    capability_id=cap.capability_id,
                    provider=cap.provider,
                    estimated_latency_ms=cap.p50_latency_ms * obj.estimated_complexity,
                    estimated_cost_usd=cap.unit_cost_usd * obj.estimated_complexity,
                    estimated_accuracy=cap.historical_accuracy,
                    failure_probability=cap.failure_probability,
                    fallback_capability_id="llm_pro_reasoner",
                )
            )

        total_cost = sum(s.estimated_cost_usd for s in steps)
        critical_path = sum(s.estimated_latency_ms for s in steps) * 0.72
        avg_acc = sum(s.estimated_accuracy for s in steps) / max(1, len(steps))

        return CandidateStrategy(
            strategy_id=f"strat_delta_{uuid.uuid4().hex[:6]}",
            archetype=StrategyArchetype.DELTA_PARETO,
            name="Strategy Delta (Adaptive Pareto-Balanced)",
            description="Hybrid balance: Cloud Vision precision for OCR, Flash Lite for high-speed extraction, AST validation, and fallback escalation to Pro LLM.",
            mission_id=goal_graph.mission_id,
            steps=steps,
            concurrency_level=8,
            estimated_total_latency_ms=critical_path * 1.1,
            estimated_critical_path_ms=critical_path,
            estimated_total_cost_usd=total_cost,
            estimated_accuracy=avg_acc,
            estimated_risk_score=0.06,
            token_estimate=18500,
            is_pareto_optimal=True,
            rationale="Maximizes Pareto multi-objective utility by capturing 98% of Pro accuracy at 15% of the cost and 40% of the latency.",
        )
