"""Probabilistic Cognitive Domain Runtime Events for DocuTask Agent.

Defines strongly-typed, immutable runtime events emitted by all Bayesian belief state engines,
world models, active EVOI calculators, meta-planners, and formal verification solvers.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4
from app.runtime.events.base import RuntimeEvent


def _make_prob_event(event_type: str, mission_id: str, payload: Dict[str, Any], **kwargs) -> RuntimeEvent:
    return RuntimeEvent(
        event_id=f"evt_prob_{uuid4().hex[:12]}",
        mission_id=mission_id,
        event_type=event_type,
        payload=payload,
        metadata={"subsystem": "AUTONOMOUS_DECISION_INTELLIGENCE_PLATFORM", "version": "3.0.0"},
        **kwargs
    )


def BeliefInitializedEvent(mission_id: str, belief_version: int, prior_entropy: float, variable_count: int) -> RuntimeEvent:
    return _make_prob_event("BeliefInitialized", mission_id, {
        "belief_version": belief_version,
        "prior_entropy": prior_entropy,
        "variable_count": variable_count,
    })


def BeliefUpdatedEvent(mission_id: str, variable_name: str, prior_mean: float, posterior_mean: float, entropy_delta: float) -> RuntimeEvent:
    return _make_prob_event("BeliefUpdated", mission_id, {
        "variable_name": variable_name,
        "prior_mean": prior_mean,
        "posterior_mean": posterior_mean,
        "entropy_delta": entropy_delta,
    })


def PosteriorComputedEvent(mission_id: str, hypothesis: str, likelihood: float, posterior_probability: float, credible_interval: List[float]) -> RuntimeEvent:
    return _make_prob_event("PosteriorComputed", mission_id, {
        "hypothesis": hypothesis,
        "likelihood": likelihood,
        "posterior_probability": posterior_probability,
        "credible_interval": credible_interval,
    })


def EntropyReducedEvent(mission_id: str, initial_entropy: float, final_entropy: float, information_gain_bits: float) -> RuntimeEvent:
    return _make_prob_event("EntropyReduced", mission_id, {
        "initial_entropy": initial_entropy,
        "final_entropy": final_entropy,
        "information_gain_bits": information_gain_bits,
    })


def InformationRequestedEvent(mission_id: str, action_type: str, evoi_value: float, cost_usd: float, approved: bool) -> RuntimeEvent:
    return _make_prob_event("InformationRequested", mission_id, {
        "action_type": action_type,
        "evoi_value": evoi_value,
        "cost_usd": cost_usd,
        "approved": approved,
    })


def WorldPredictionGeneratedEvent(mission_id: str, horizon_minutes: int, predicted_gpu_load: float, predicted_token_burn: int, predicted_queue_depth: int) -> RuntimeEvent:
    return _make_prob_event("WorldPredictionGenerated", mission_id, {
        "horizon_minutes": horizon_minutes,
        "predicted_gpu_load": predicted_gpu_load,
        "predicted_token_burn": predicted_token_burn,
        "predicted_queue_depth": predicted_queue_depth,
    })


def PlannerConfidenceCalculatedEvent(mission_id: str, epistemic_uncertainty: float, aleatoric_uncertainty: float, composite_confidence: float) -> RuntimeEvent:
    return _make_prob_event("PlannerConfidenceCalculated", mission_id, {
        "epistemic_uncertainty": epistemic_uncertainty,
        "aleatoric_uncertainty": aleatoric_uncertainty,
        "composite_confidence": composite_confidence,
    })


def ExpectedValueInformationComputedEvent(mission_id: str, candidate_action: str, expected_gain: float, net_evoi: float) -> RuntimeEvent:
    return _make_prob_event("ExpectedValueInformationComputed", mission_id, {
        "candidate_action": candidate_action,
        "expected_gain": expected_gain,
        "net_evoi": net_evoi,
    })


def MetaPlanningStartedEvent(mission_id: str, planner_strategy: str, search_depth: int, beam_width: int) -> RuntimeEvent:
    return _make_prob_event("MetaPlanningStarted", mission_id, {
        "planner_strategy": planner_strategy,
        "search_depth": search_depth,
        "beam_width": beam_width,
    })


def PlannerCritiquedEvent(mission_id: str, mistake_count: int, bias_detected: bool, critique_score: float) -> RuntimeEvent:
    return _make_prob_event("PlannerCritiqued", mission_id, {
        "mistake_count": mistake_count,
        "bias_detected": bias_detected,
        "critique_score": critique_score,
    })


def RegretComputedEvent(mission_id: str, expected_regret: float, counterfactual_regret: float, opportunity_cost: float) -> RuntimeEvent:
    return _make_prob_event("RegretComputed", mission_id, {
        "expected_regret": expected_regret,
        "counterfactual_regret": counterfactual_regret,
        "opportunity_cost": opportunity_cost,
    })


def ExplorationTriggeredEvent(mission_id: str, chosen_arm: str, ucb_score: float, novelty_reward: float) -> RuntimeEvent:
    return _make_prob_event("ExplorationTriggered", mission_id, {
        "chosen_arm": chosen_arm,
        "ucb_score": ucb_score,
        "novelty_reward": novelty_reward,
    })


def FormalVerificationCompletedEvent(mission_id: str, is_satisfiable: bool, invariant_count: int, solver_latency_ms: float) -> RuntimeEvent:
    return _make_prob_event("FormalVerificationCompleted", mission_id, {
        "is_satisfiable": is_satisfiable,
        "invariant_count": invariant_count,
        "solver_latency_ms": solver_latency_ms,
    })


def GovernanceApprovedEvent(mission_id: str, policy_name: str, merkle_root: str, auto_approved: bool) -> RuntimeEvent:
    return _make_prob_event("GovernanceApproved", mission_id, {
        "policy_name": policy_name,
        "merkle_root": merkle_root,
        "auto_approved": auto_approved,
    })
