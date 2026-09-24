"""
Planning Domain Runtime Events for DocuTask Agent.
Defines strongly-typed, immutable runtime events emitted by all 16 autonomous planning subsystems.
"""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4
from app.runtime.events.base import RuntimeEvent


def _make_event(event_type: str, mission_id: str, payload: Dict[str, Any], agent_id: str = "PLANNER", **kwargs) -> RuntimeEvent:
    return RuntimeEvent(
        event_id=f"evt_plan_{uuid4().hex[:12]}",
        mission_id=mission_id,
        agent_id=agent_id,
        event_type=event_type,
        payload=payload,
        metadata={"subsystem": "AUTONOMOUS_PLANNING_PLATFORM", "version": "2.0.0"},
        **kwargs
    )


def GoalParsedEvent(mission_id: str, goal_text: str, domain: str, priority: str, deliverables: List[str]) -> RuntimeEvent:
    return _make_event("GoalParsed", mission_id, {
        "goal_text": goal_text,
        "domain": domain,
        "priority": priority,
        "deliverables": deliverables,
    })


def GoalGraphCreatedEvent(mission_id: str, node_count: int, edge_count: int, completion_criteria: List[str]) -> RuntimeEvent:
    return _make_event("GoalGraphCreated", mission_id, {
        "node_count": node_count,
        "edge_count": edge_count,
        "completion_criteria": completion_criteria,
    })


def ConstraintsExtractedEvent(mission_id: str, hard_constraints: List[str], soft_constraints: List[str], max_budget_usd: float, max_latency_ms: float) -> RuntimeEvent:
    return _make_event("ConstraintsExtracted", mission_id, {
        "hard_constraints": hard_constraints,
        "soft_constraints": soft_constraints,
        "max_budget_usd": max_budget_usd,
        "max_latency_ms": max_latency_ms,
    })


def CapabilityDiscoveredEvent(mission_id: str, capability_id: str, capability_type: str, health_score: float, latency_p50_ms: float) -> RuntimeEvent:
    return _make_event("CapabilityDiscovered", mission_id, {
        "capability_id": capability_id,
        "capability_type": capability_type,
        "health_score": health_score,
        "latency_p50_ms": latency_p50_ms,
    })


def CandidateStrategyGeneratedEvent(mission_id: str, strategy_id: str, strategy_name: str, task_count: int, paradigm: str) -> RuntimeEvent:
    return _make_event("CandidateStrategyGenerated", mission_id, {
        "strategy_id": strategy_id,
        "strategy_name": strategy_name,
        "task_count": task_count,
        "paradigm": paradigm,
    })


def StrategySimulationCompletedEvent(mission_id: str, strategy_id: str, expected_duration_ms: float, expected_cost_usd: float, failure_probability: float) -> RuntimeEvent:
    return _make_event("StrategySimulationCompleted", mission_id, {
        "strategy_id": strategy_id,
        "expected_duration_ms": expected_duration_ms,
        "expected_cost_usd": expected_cost_usd,
        "failure_probability": failure_probability,
    })


def UtilityCalculatedEvent(mission_id: str, strategy_id: str, utility_score: float, utility_version: str, components: Dict[str, float]) -> RuntimeEvent:
    return _make_event("UtilityCalculated", mission_id, {
        "strategy_id": strategy_id,
        "utility_score": utility_score,
        "utility_version": utility_version,
        "components": components,
    })


def RiskEstimatedEvent(mission_id: str, strategy_id: str, overall_risk_score: float, top_risk_vector: str, mitigation: str) -> RuntimeEvent:
    return _make_event("RiskEstimated", mission_id, {
        "strategy_id": strategy_id,
        "overall_risk_score": overall_risk_score,
        "top_risk_vector": top_risk_vector,
        "mitigation": mitigation,
    })


def StrategyRankedEvent(mission_id: str, ranked_strategy_ids: List[str], selected_strategy_id: str, selection_margin: float) -> RuntimeEvent:
    return _make_event("StrategyRanked", mission_id, {
        "ranked_strategy_ids": ranked_strategy_ids,
        "selected_strategy_id": selected_strategy_id,
        "selection_margin": selection_margin,
    })


def CounterfactualGeneratedEvent(mission_id: str, chosen_strategy_id: str, rejected_strategy_id: str, counterfactual_reason: str, sensitivity_parameter: str) -> RuntimeEvent:
    return _make_event("CounterfactualGenerated", mission_id, {
        "chosen_strategy_id": chosen_strategy_id,
        "rejected_strategy_id": rejected_strategy_id,
        "counterfactual_reason": counterfactual_reason,
        "sensitivity_parameter": sensitivity_parameter,
    })


def StrategySelectedEvent(mission_id: str, strategy_id: str, strategy_name: str, utility_score: float, expected_confidence: float) -> RuntimeEvent:
    return _make_event("StrategySelected", mission_id, {
        "strategy_id": strategy_id,
        "strategy_name": strategy_name,
        "utility_score": utility_score,
        "expected_confidence": expected_confidence,
    })


def DAGCreatedEvent(mission_id: str, dag_id: str, node_count: int, critical_path_duration_ms: float) -> RuntimeEvent:
    return _make_event("DAGCreated", mission_id, {
        "dag_id": dag_id,
        "node_count": node_count,
        "critical_path_duration_ms": critical_path_duration_ms,
    })


def DAGMutatedEvent(mission_id: str, dag_id: str, mutation_type: str, affected_node_ids: List[str], reason: str) -> RuntimeEvent:
    return _make_event("DAGMutated", mission_id, {
        "dag_id": dag_id,
        "mutation_type": mutation_type,
        "affected_node_ids": affected_node_ids,
        "reason": reason,
    })


def WorkerLeasedEvent(mission_id: str, worker_id: str, task_id: str, lease_duration_ms: float, priority: int) -> RuntimeEvent:
    return _make_event("WorkerLeased", mission_id, {
        "worker_id": worker_id,
        "task_id": task_id,
        "lease_duration_ms": lease_duration_ms,
        "priority": priority,
    }, worker_id=worker_id)


def WorkerReleasedEvent(mission_id: str, worker_id: str, task_id: str, active_duration_ms: float, success: bool) -> RuntimeEvent:
    return _make_event("WorkerReleased", mission_id, {
        "worker_id": worker_id,
        "task_id": task_id,
        "active_duration_ms": active_duration_ms,
        "success": success,
    }, worker_id=worker_id)


def ReplanningStartedEvent(mission_id: str, trigger_reason: str, affected_subgraph_nodes: List[str]) -> RuntimeEvent:
    return _make_event("ReplanningStarted", mission_id, {
        "trigger_reason": trigger_reason,
        "affected_subgraph_nodes": affected_subgraph_nodes,
    })


def ReplanningCompletedEvent(mission_id: str, replan_duration_ms: float, nodes_added: int, nodes_pruned: int, new_expected_utility: float) -> RuntimeEvent:
    return _make_event("ReplanningCompleted", mission_id, {
        "replan_duration_ms": replan_duration_ms,
        "nodes_added": nodes_added,
        "nodes_pruned": nodes_pruned,
        "new_expected_utility": new_expected_utility,
    })


def PlanningMemoryRetrievedEvent(mission_id: str, query_similarity: float, past_mission_id: str, strategy_pattern: str) -> RuntimeEvent:
    return _make_event("PlanningMemoryRetrieved", mission_id, {
        "query_similarity": query_similarity,
        "past_mission_id": past_mission_id,
        "strategy_pattern": strategy_pattern,
    })


def PlanningMemoryStoredEvent(mission_id: str, mission_signature: str, utility_delta: float, lessons_learned: str) -> RuntimeEvent:
    return _make_event("PlanningMemoryStored", mission_id, {
        "mission_signature": mission_signature,
        "utility_delta": utility_delta,
        "lessons_learned": lessons_learned,
    })


def PlannerSelfEvaluationCompletedEvent(mission_id: str, utility_regret: float, cost_error_pct: float, latency_error_pct: float, calibration_score: float) -> RuntimeEvent:
    return _make_event("PlannerSelfEvaluationCompleted", mission_id, {
        "utility_regret": utility_regret,
        "cost_error_pct": cost_error_pct,
        "latency_error_pct": latency_error_pct,
        "calibration_score": calibration_score,
    })
