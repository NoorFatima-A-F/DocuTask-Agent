"""
Decision Provenance Engine.
Constructs first-class DecisionRecord objects answering Why, What, Based On, and Why Not Others.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from app.runtime.decision.utility_breakdown import PlanUtilityScore
from app.runtime.decision.decision_serializer import DecisionSerializer


class DecisionRecord(BaseModel):
    decision_id: str = Field(..., description="Unique decision ID")
    mission_id: str = Field(..., description="Mission identifier")
    planner_version: str = Field(default="v2.1-APDLE", description="Active planner version")
    planner_generation: int = Field(default=1, description="Planner graph generation")
    goal: str = Field(..., description="Goal under deliberation")
    selected_plan: str = Field(..., description="Name of the selected plan")
    alternative_plans: List[PlanUtilityScore] = Field(default_factory=list, description="Candidate alternatives with utility scores")
    utility_scores: Dict[str, float] = Field(default_factory=dict, description="Selected plan utility metrics")
    constraints: List[str] = Field(default_factory=list, description="Evaluated constraints")
    evidence_ids: List[str] = Field(default_factory=list, description="Supporting evidence IDs")
    supporting_memories: List[str] = Field(default_factory=list, description="Retrieved experience memory IDs")
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list, description="Associated tool invocations")
    assigned_worker: str = Field(default="worker_general", description="Target worker assigned")
    confidence: float = Field(default=0.95, ge=0.0, le=1.0, description="Confidence score")
    parent_decision_id: Optional[str] = Field(default=None, description="Causal parent decision ID")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    why_chosen: str = Field(..., description="Observable rationale for selected action")
    why_not_others: Dict[str, str] = Field(default_factory=dict, description="Rejection rationale for each alternative")
    based_on: List[str] = Field(default_factory=list, description="Causal evidence references")
    decision_hash: Optional[str] = Field(default=None, description="SHA-256 cryptographic hash")


class DecisionProvenanceEngine:
    """Creates tamper-evident DecisionRecord instances."""

    @staticmethod
    def create_decision(
        decision_id: str,
        mission_id: str,
        goal: str,
        selected_plan: str,
        why_chosen: str,
        alternative_plans: Optional[List[PlanUtilityScore]] = None,
        utility_scores: Optional[Dict[str, float]] = None,
        constraints: Optional[List[str]] = None,
        evidence_ids: Optional[List[str]] = None,
        supporting_memories: Optional[List[str]] = None,
        tool_calls: Optional[List[Dict[str, Any]]] = None,
        assigned_worker: str = "worker_general",
        confidence: float = 0.95,
        parent_decision_id: Optional[str] = None,
        planner_generation: int = 1,
        planner_version: str = "v2.1-APDLE",
    ) -> DecisionRecord:
        alts = alternative_plans or []
        why_not = {alt.plan_name: alt.rejection_reason or "Sub-optimal Pareto utility" for alt in alts if alt.plan_name != selected_plan}
        based = list(evidence_ids or []) + list(constraints or [])

        raw_dict = {
            "decision_id": decision_id,
            "mission_id": mission_id,
            "planner_version": planner_version,
            "planner_generation": planner_generation,
            "goal": goal,
            "selected_plan": selected_plan,
            "alternative_plans": [a.model_dump() for a in alts],
            "utility_scores": utility_scores or {},
            "constraints": constraints or [],
            "evidence_ids": evidence_ids or [],
            "supporting_memories": supporting_memories or [],
            "tool_calls": tool_calls or [],
            "assigned_worker": assigned_worker,
            "confidence": confidence,
            "parent_decision_id": parent_decision_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "why_chosen": why_chosen,
            "why_not_others": why_not,
            "based_on": based,
        }

        d_hash = DecisionSerializer.compute_decision_hash(raw_dict)
        raw_dict["decision_hash"] = d_hash

        return DecisionRecord.model_validate(raw_dict)
