"""Strongly-typed events for Autonomous Cognitive Evolution Platform (ACOS).

Emitted across Strategy Discovery, Planner Self-Evolution, Digital Twin Simulation,
Structural Causal Reasoning, and Multi-Agent Council Deliberation.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CognitiveEvolutionEventType(str, Enum):
    HTN_SYNTHESIS_STARTED = "HTN_SYNTHESIS_STARTED"
    HTN_SYNTHESIS_COMPLETED = "HTN_SYNTHESIS_COMPLETED"
    OPERATOR_SYNTHESIZED = "OPERATOR_SYNTHESIZED"
    OPERATOR_VERIFIED = "OPERATOR_VERIFIED"
    GRAPH_MUTATED = "GRAPH_MUTATED"
    STRATEGY_DISCOVERED = "STRATEGY_DISCOVERED"
    PLANNER_MUTATION_GENERATED = "PLANNER_MUTATION_GENERATED"
    PLANNER_EVALUATION_SIMULATED = "PLANNER_EVALUATION_SIMULATED"
    PLANNER_GENERATION_PROMOTED = "PLANNER_GENERATION_PROMOTED"
    PLANNER_GENERATION_ROLLED_BACK = "PLANNER_GENERATION_ROLLED_BACK"
    SIMULATION_BATCH_COMPLETED = "SIMULATION_BATCH_COMPLETED"
    CHAOS_FAULT_INJECTED = "CHAOS_FAULT_INJECTED"
    CAUSAL_MODEL_INDUCED = "CAUSAL_MODEL_INDUCED"
    DO_INTERVENTION_EVALUATED = "DO_INTERVENTION_EVALUATED"
    COUNCIL_DELIBERATION_CONVENED = "COUNCIL_DELIBERATION_CONVENED"
    COUNCIL_VOTE_RECORDED = "COUNCIL_VOTE_RECORDED"
    COUNCIL_CONSENSUS_REACHED = "COUNCIL_CONSENSUS_REACHED"


class StrategySynthesizedEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_syn_{uuid.uuid4().hex[:8]}")
    strategy_id: str
    goal_intent: str
    node_count: int
    edge_count: int
    novelty_score: float
    expected_utility: float
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class OperatorSynthesizedEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_op_{uuid.uuid4().hex[:8]}")
    operator_name: str
    input_schema: Dict[str, str]
    output_schema: Dict[str, str]
    ast_verified: bool
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PlannerEvolvedEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_evo_{uuid.uuid4().hex[:8]}")
    previous_version: str
    new_version: str
    fitness_score: float
    brier_improvement_pct: float
    simulated_trials_count: int
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DigitalTwinSimulatedEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_sim_{uuid.uuid4().hex[:8]}")
    simulation_id: str
    virtual_workers_count: int
    simulated_missions_count: int
    p99_latency_ms: float
    queue_overflow_count: int
    chaos_resilience_score: float
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CausalInterventionEvaluatedEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_cau_{uuid.uuid4().hex[:8]}")
    target_variable: str
    intervention_variable: str
    intervention_value: float
    expected_outcome: float
    counterfactual_delta: float
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CouncilDeliberatedEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_cou_{uuid.uuid4().hex[:8]}")
    mission_id: str
    agents_participated: List[str]
    winning_strategy_id: str
    borda_tally: Dict[str, int]
    consensus_entropy: float
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
