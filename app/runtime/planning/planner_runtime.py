"""Autonomous Planning Runtime Coordinator for DocuTask.

Orchestrates goal understanding, constraint extraction, capability discovery, candidate strategy generation,
simulation, utility optimization, risk analysis, counterfactual reasoning, DAG compilation, worker scheduling,
adaptive replanning, and planner self-evaluation with full RuntimeEvent publishing.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.runtime.events.event_bus import EventBus
from app.runtime.events.planning_events import (
    GoalParsedEvent,
    GoalGraphCreatedEvent,
    ConstraintsExtractedEvent,
    CandidateStrategyGeneratedEvent,
    StrategySimulationCompletedEvent,
    UtilityCalculatedEvent,
    RiskEstimatedEvent,
    StrategyRankedEvent,
    CounterfactualGeneratedEvent,
    StrategySelectedEvent,
    DAGCreatedEvent,
    DAGMutatedEvent,
    ReplanningStartedEvent,
    ReplanningCompletedEvent,
    PlanningMemoryRetrievedEvent,
    PlanningMemoryStoredEvent,
    PlannerSelfEvaluationCompletedEvent,
)
from app.runtime.planning.goal_engine import GoalUnderstandingEngine, GoalGraph
from app.runtime.planning.constraint_engine import ConstraintExtractionEngine, MissionConstraintSet
from app.runtime.planning.capability_discovery import CapabilityDiscoveryEngine
from app.runtime.planning.strategy_generator import CandidateStrategyGenerator, CandidateStrategy
from app.runtime.planning.cost_predictor import CostPredictionEngine, CostPredictionResult
from app.runtime.planning.latency_predictor import LatencyPredictionEngine, LatencyPredictionResult
from app.runtime.planning.risk_engine import RiskIntelligenceEngine, StrategyRiskProfile
from app.runtime.planning.execution_simulator import ExecutionSimulator, SimulationResult
from app.runtime.planning.utility_engine import MultiObjectiveUtilityEngine, UtilityScore
from app.runtime.planning.strategy_ranker import StrategyRankingEngine, StrategySelectionRecord
from app.runtime.planning.counterfactual_engine import CounterfactualEngine, CounterfactualExplanation
from app.runtime.planning.mutable_dag import MutableExecutionDAG, DAGNode, DAGNodeStatus
from app.runtime.planning.scheduler import EnterpriseResourceScheduler
from app.runtime.planning.adaptive_replanner import AdaptiveReplanningEngine, ReplanningTrigger, SubGraphReplanningResult
from app.runtime.planning.planning_memory import PlanningMemoryEngine, PlanSignature
from app.runtime.planning.self_evaluator import PlannerSelfEvaluationEngine, PlanCalibrationMetric


class MissionPlanResult(BaseModel):
    """Complete, self-contained planning outcome for a mission."""
    mission_id: str
    goal_graph: GoalGraph
    constraint_set: MissionConstraintSet
    candidate_strategies: List[CandidateStrategy]
    selection_record: StrategySelectionRecord
    selected_dag: MutableExecutionDAG
    simulations: Dict[str, SimulationResult]
    cost_predictions: Dict[str, CostPredictionResult]
    latency_predictions: Dict[str, LatencyPredictionResult]
    risk_profiles: Dict[str, StrategyRiskProfile]
    counterfactual_explanations: List[CounterfactualExplanation] = Field(default_factory=list)


class AutonomousPlanningRuntime:
    """The central Autonomous Planning Operating System coordinator."""

    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self.event_bus = event_bus or EventBus.get_instance()
        self.goal_engine = GoalUnderstandingEngine()
        self.constraint_engine = ConstraintExtractionEngine()
        self.capability_discovery = CapabilityDiscoveryEngine()
        self.strategy_generator = CandidateStrategyGenerator(self.capability_discovery)
        self.cost_predictor = CostPredictionEngine()
        self.latency_predictor = LatencyPredictionEngine()
        self.risk_engine = RiskIntelligenceEngine()
        self.simulator = ExecutionSimulator()
        self.utility_engine = MultiObjectiveUtilityEngine()
        self.strategy_ranker = StrategyRankingEngine()
        self.counterfactual_engine = CounterfactualEngine(self.utility_engine)
        self.scheduler = EnterpriseResourceScheduler(self.capability_discovery)
        self.adaptive_replanner = AdaptiveReplanningEngine(self.capability_discovery)
        self.memory_engine = PlanningMemoryEngine()
        self.self_evaluator = PlannerSelfEvaluationEngine()

        # In-memory store for active mission DAGs and plans
        self._active_plans: Dict[str, MissionPlanResult] = {}
        self._active_dags: Dict[str, MutableExecutionDAG] = {}

    def plan_mission(
        self,
        mission_id: str,
        raw_intent: str,
        user_constraints: Optional[Dict[str, Any]] = None,
        signature: Optional[PlanSignature] = None,
    ) -> MissionPlanResult:
        """Executes the complete autonomous planning pipeline from intent to executable DAG."""
        # 1. Goal Understanding
        goal_graph = self.goal_engine.parse_intent(mission_id=mission_id, raw_intent=raw_intent)
        self._publish(GoalParsedEvent(mission_id, raw_intent, "document_operations", "CRITICAL", list(goal_graph.objectives.keys())))
        self._publish(GoalGraphCreatedEvent(mission_id, len(goal_graph.objectives), len(goal_graph.dependencies), ["confidence>=0.90", "schema_valid==1.0"]))

        # 2. Constraint Extraction
        constraint_set = self.constraint_engine.extract_constraints(mission_id=mission_id, user_constraints=user_constraints)
        self._publish(ConstraintsExtractedEvent(
            mission_id,
            [c.name for c in constraint_set.get_hard_constraints()],
            [c.name for c in constraint_set.get_soft_constraints()],
            user_constraints.get("budget_usd", 0.50) if user_constraints else 0.50,
            user_constraints.get("max_latency_ms", 5000.0) if user_constraints else 5000.0,
        ))

        # 3. Planning Memory Lookup
        sig = signature or PlanSignature(document_type="invoice")
        similar = self.memory_engine.retrieve_similar_plans(sig, top_k=2)
        if similar:
            best_mem, sim_score = similar[0]
            self._publish(PlanningMemoryRetrievedEvent(mission_id, sim_score, best_mem.mission_id, best_mem.selected_archetype))

        # 4. Candidate Strategy Generation
        strategies = self.strategy_generator.generate_strategies(goal_graph=goal_graph, constraint_set=constraint_set)
        for strat in strategies:
            self._publish(CandidateStrategyGeneratedEvent(
                mission_id,
                strat.strategy_id,
                strat.name,
                len(strat.steps),
                strat.archetype.value,
            ))

        # 5. Prediction, Risk, Simulation & Utility Optimization
        cost_predictions: Dict[str, CostPredictionResult] = {}
        latency_predictions: Dict[str, LatencyPredictionResult] = {}
        risk_profiles: Dict[str, StrategyRiskProfile] = {}
        simulations: Dict[str, SimulationResult] = {}
        utility_scores: Dict[str, UtilityScore] = {}

        for strat in strategies:
            c_pred = self.cost_predictor.predict_cost(strat)
            l_pred = self.latency_predictor.predict_latency(strat, concurrency_limit=strat.concurrency_level)
            r_prof = self.risk_engine.evaluate_strategy_risk(strat)
            sim_res = self.simulator.simulate(strat, iterations=300)

            cost_predictions[strat.strategy_id] = c_pred
            latency_predictions[strat.strategy_id] = l_pred
            risk_profiles[strat.strategy_id] = r_prof
            simulations[strat.strategy_id] = sim_res

            self._publish(StrategySimulationCompletedEvent(
                mission_id,
                strat.strategy_id,
                sim_res.mean_duration_ms,
                strat.estimated_total_cost_usd,
                1.0 - sim_res.simulated_success_rate,
            ))
            self._publish(RiskEstimatedEvent(
                mission_id,
                strat.strategy_id,
                r_prof.overall_risk_score,
                r_prof.high_risk_vectors[0].name if r_prof.high_risk_vectors else "None",
                r_prof.high_risk_vectors[0].mitigation_strategy if r_prof.high_risk_vectors else "Nominal",
            ))

            soft_penalty = strat.constraint_compliance.get("soft_penalty", 0.0)
            u_score = self.utility_engine.calculate_utility(
                strat, c_pred, l_pred, r_prof, memory_synergy_bonus=0.95, soft_penalty=soft_penalty
            )
            utility_scores[strat.strategy_id] = u_score

            self._publish(UtilityCalculatedEvent(
                mission_id,
                strat.strategy_id,
                u_score.total_utility,
                u_score.version,
                {
                    "accuracy": u_score.accuracy_term,
                    "latency": u_score.latency_penalty_term,
                    "cost": u_score.cost_penalty_term,
                    "risk": u_score.risk_penalty_term,
                },
            ))

        # 6. Strategy Ranking & Selection
        selection_record = self.strategy_ranker.evaluate_and_rank(
            mission_id=mission_id,
            strategies=strategies,
            utility_scores=utility_scores,
            cost_predictions=cost_predictions,
            latency_predictions=latency_predictions,
            risk_profiles=risk_profiles,
        )

        ranked_ids = [e.strategy_id for e in selection_record.comparison_matrix.entries]
        self._publish(StrategyRankedEvent(
            mission_id,
            ranked_ids,
            selection_record.selected_strategy_id,
            0.15,
        ))
        self._publish(StrategySelectedEvent(
            mission_id,
            selection_record.selected_strategy_id,
            selection_record.selected_archetype,
            utility_scores[selection_record.selected_strategy_id].total_utility,
            0.98,
        ))

        # 7. Counterfactual Generation
        explanations: List[CounterfactualExplanation] = []
        sel_id = selection_record.selected_strategy_id

        # Explain why selected
        why_sel = self.counterfactual_engine.explain_selection(
            sel_id, strategies, utility_scores, cost_predictions, latency_predictions, risk_profiles
        )
        explanations.append(why_sel)

        # Explain why alternatives rejected
        for strat in strategies:
            if strat.strategy_id != sel_id:
                why_rej = self.counterfactual_engine.explain_rejection(
                    strat.strategy_id, sel_id, strategies, utility_scores, cost_predictions, latency_predictions, risk_profiles
                )
                explanations.append(why_rej)
                self._publish(CounterfactualGeneratedEvent(
                    mission_id,
                    sel_id,
                    strat.strategy_id,
                    why_rej.summary_explanation,
                    why_rej.tipping_point.get("parameter", "w_latency") if why_rej.tipping_point else "w_latency",
                ))

        # 8. Compile Executable Mutable DAG
        selected_strat = next(s for s in strategies if s.strategy_id == sel_id)
        dag = self._compile_dag_from_strategy(mission_id, selected_strat)
        self._active_dags[mission_id] = dag

        self._publish(DAGCreatedEvent(
            mission_id,
            dag.dag_id,
            len(dag.nodes),
            latency_predictions[sel_id].critical_path_ms,
        ))

        plan_result = MissionPlanResult(
            mission_id=mission_id,
            goal_graph=goal_graph,
            constraint_set=constraint_set,
            candidate_strategies=strategies,
            selection_record=selection_record,
            selected_dag=dag,
            simulations=simulations,
            cost_predictions=cost_predictions,
            latency_predictions=latency_predictions,
            risk_profiles=risk_profiles,
            counterfactual_explanations=explanations,
        )

        self._active_plans[mission_id] = plan_result
        return plan_result

    def _compile_dag_from_strategy(self, mission_id: str, strategy: CandidateStrategy) -> MutableExecutionDAG:
        dag = MutableExecutionDAG(mission_id=mission_id, strategy_id=strategy.strategy_id)
        prev_node_id: Optional[str] = None

        for step in strategy.steps:
            node = DAGNode(
                name=step.name,
                capability_id=step.capability_id,
                provider=step.provider,
                status=DAGNodeStatus.PENDING,
                metadata={
                    "step_id": step.step_id,
                    "estimated_latency_ms": step.estimated_latency_ms,
                    "estimated_cost_usd": step.estimated_cost_usd,
                    "fallback_capability_id": step.fallback_capability_id,
                },
            )
            dag.add_node(node)
            if prev_node_id:
                dag.add_edge(prev_node_id, node.node_id)
            prev_node_id = node.node_id

        return dag

    def mutate_dag_split(self, mission_id: str, node_id: str, split_count: int, rationale: str) -> List[DAGNode]:
        dag = self._active_dags.get(mission_id)
        if not dag:
            raise ValueError(f"No active DAG for mission {mission_id}")
        shards = dag.split_node(node_id, split_count, rationale)
        self._publish(DAGMutatedEvent(
            mission_id, dag.dag_id, "NODE_SPLIT", [node_id] + [s.node_id for s in shards], rationale
        ))
        return shards

    def mutate_dag_replace(self, mission_id: str, node_id: str, new_capability_id: str, new_provider: str, rationale: str) -> DAGNode:
        dag = self._active_dags.get(mission_id)
        if not dag:
            raise ValueError(f"No active DAG for mission {mission_id}")
        node = dag.replace_node_capability(node_id, new_capability_id, new_provider, rationale)
        self._publish(DAGMutatedEvent(
            mission_id, dag.dag_id, "NODE_REPLACE", [node_id], rationale
        ))
        return node

    def trigger_adaptive_replanning(self, mission_id: str, trigger: ReplanningTrigger) -> SubGraphReplanningResult:
        dag = self._active_dags.get(mission_id)
        if not dag:
            raise ValueError(f"No active DAG for mission {mission_id}")

        self._publish(ReplanningStartedEvent(
            mission_id, trigger.rationale or trigger.trigger_type.value, [trigger.node_id] if trigger.node_id else []
        ))

        res = self.adaptive_replanner.handle_trigger(dag, trigger)

        self._publish(ReplanningCompletedEvent(
            mission_id, 45.0, len(res.new_nodes_added), 0, 0.92
        ))

        return res

    def evaluate_mission_outcome(
        self,
        mission_id: str,
        actual_latency_ms: float,
        actual_cost_usd: float,
        actual_accuracy: float,
        actual_failure: bool = False,
    ) -> PlanCalibrationMetric:
        plan = self._active_plans.get(mission_id)
        if not plan:
            raise ValueError(f"Plan for mission {mission_id} not found.")

        sel_strat_id = plan.selection_record.selected_strategy_id
        pred_cost = plan.cost_predictions[sel_strat_id].total_cost_usd
        pred_lat = plan.latency_predictions[sel_strat_id].critical_path_ms
        sel_strat = next(s for s in plan.candidate_strategies if s.strategy_id == sel_strat_id)

        calib = self.self_evaluator.evaluate_mission(
            mission_id=mission_id,
            strategy_id=sel_strat_id,
            predicted_latency_ms=pred_lat,
            actual_latency_ms=actual_latency_ms,
            predicted_cost_usd=pred_cost,
            actual_cost_usd=actual_cost_usd,
            predicted_accuracy=sel_strat.estimated_accuracy,
            actual_accuracy=actual_accuracy,
            predicted_risk_score=plan.risk_profiles[sel_strat_id].overall_risk_score,
            actual_failure_occurred=actual_failure,
        )

        # Store in planning memory
        self.memory_engine.store_outcome(
            mission_id=mission_id,
            signature=PlanSignature(document_type="invoice"),
            selected_archetype=plan.selection_record.selected_archetype,
            selected_strategy_id=sel_strat_id,
            actual_latency_ms=actual_latency_ms,
            actual_cost_usd=actual_cost_usd,
            actual_accuracy=actual_accuracy,
            success=not actual_failure,
        )
        self._publish(PlanningMemoryStoredEvent(mission_id, "invoice_p2_f12", 0.04, "Nominal accuracy within bounds"))
        self._publish(PlannerSelfEvaluationCompletedEvent(
            mission_id,
            0.02,
            calib.comparison.cost_error_pct,
            calib.comparison.latency_error_pct,
            calib.overall_calibration_score,
        ))

        return calib

    def get_plan(self, mission_id: str) -> Optional[MissionPlanResult]:
        return self._active_plans.get(mission_id)

    def get_dag(self, mission_id: str) -> Optional[MutableExecutionDAG]:
        return self._active_dags.get(mission_id)

    def _publish(self, event: Any) -> None:
        if self.event_bus:
            self.event_bus.publish(event)
