"""
Policy Engine for Phase 13.5 (ARLP-KIP).
Coordinates candidate policy synthesis, simulation evaluation, and differential matrix comparisons.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field

from app.runtime.learning.policy.policy_generator import PolicyGenerator, PolicyAdjustment
from app.runtime.learning.policy.policy_evaluator import PolicyEvaluator, PolicySimulationResult
from app.runtime.learning.policy.policy_comparator import PolicyComparator, PolicyComparisonReport


class CandidatePolicy(BaseModel):
    candidate_id: str = Field(default_factory=lambda: f"cand_{uuid.uuid4().hex[:8]}")
    policy_name: str
    target_component: str
    version: str = "1.1.0"
    status: str = "PROPOSED"  # PROPOSED | EVALUATED | APPROVED | PROMOTED | REJECTED
    parameters: Dict[str, Any] = Field(default_factory=dict)
    adjustments: List[PolicyAdjustment] = Field(default_factory=list)
    simulation_result: Optional[PolicySimulationResult] = None
    comparison_report: Optional[PolicyComparisonReport] = None
    evidence_lessons: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PolicyEngine:
    """
    Coordinates candidate policy synthesis and counterfactual simulation evaluations.
    """

    def __init__(self):
        self._candidates: Dict[str, CandidatePolicy] = {}
        self._seed_default_candidate()

    def _seed_default_candidate(self):
        cand = self.propose_candidate(
            target_component="planner",
            policy_name="High-Throughput Wavefront Partitioning Policy",
            parameters={"max_retries": 3, "concurrency_limit": 8, "confidence_threshold": 0.88},
            evidence_lessons=["lsn_default_001"],
        )
        self.evaluate_candidate(cand.candidate_id)

    def propose_candidate(
        self,
        target_component: str,
        policy_name: str,
        parameters: Dict[str, Any],
        evidence_lessons: Optional[List[str]] = None,
    ) -> CandidatePolicy:
        adjustments = PolicyGenerator.generate_adjustments(target_component, parameters)
        cand_id = f"cand_{uuid.uuid4().hex[:8]}"

        cand = CandidatePolicy(
            candidate_id=cand_id,
            policy_name=policy_name,
            target_component=target_component,
            parameters=parameters,
            adjustments=adjustments,
            evidence_lessons=evidence_lessons or [],
            status="PROPOSED",
        )
        self._candidates[cand_id] = cand
        return cand

    def evaluate_candidate(self, candidate_id: str) -> PolicySimulationResult:
        cand = self._candidates.get(candidate_id)
        if not cand:
            # Create a placeholder if not found
            cand = self.propose_candidate("planner", "Dynamic Policy", {"max_retries": 3, "concurrency_limit": 6})
        
        sim = PolicyEvaluator.evaluate(cand.candidate_id, cand.parameters)
        comp = PolicyComparator.compare(
            cand.candidate_id,
            gain=sim.projected_throughput_gain_pct,
            risk=sim.risk_score,
            conf=sim.confidence_posterior_estimate,
        )

        cand.simulation_result = sim
        cand.comparison_report = comp
        cand.status = "EVALUATED"
        return sim

    def list_candidates(self) -> List[CandidatePolicy]:
        return list(self._candidates.values())

    def get_candidate(self, candidate_id: str) -> Optional[CandidatePolicy]:
        return self._candidates.get(candidate_id)


policy_engine = PolicyEngine()
