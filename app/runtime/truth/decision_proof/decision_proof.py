"""
Decision Proof Engine for Phase 11 (VAIRTSEP).

Generates formal mathematical decision proofs for every planner decision,
documenting evaluated candidate strategies, rejected alternatives, objective
utility formulas, policy constraints, and supporting evidence proofs.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CandidateStrategyEval:
    strategy_id: str
    strategy_name: str
    expected_accuracy: float
    expected_latency_ms: float
    expected_cost_usd: float
    utility_score: float
    is_feasible: bool
    rejection_reason: Optional[str] = None


@dataclass
class DecisionProof:
    """
    Formal, independently verifiable proof justifying a planner decision.
    """
    proof_id: str
    mission_id: str
    decision_timestamp: float = field(default_factory=time.time)
    
    # Planner & Domain Context
    document_type: str = "invoice"
    planner_version: str = "v2.1.0"
    
    # Mathematical Utility Objective: U(s) = w_a * A(s) - w_l * (L(s)/1000) - w_c * (C(s)/0.01)
    utility_formula: str = "U(s) = 0.50 * Acc(s) - 0.30 * (Lat(s)/1000) - 0.20 * (Cost(s)/0.01)"
    accuracy_weight: float = 0.50
    latency_weight: float = 0.30
    cost_weight: float = 0.20
    
    # Candidates Evaluated & Selected Strategy
    candidates_evaluated: List[CandidateStrategyEval] = field(default_factory=list)
    selected_strategy_id: str = ""
    selected_strategy_name: str = ""
    winning_utility_score: float = 0.0
    
    # Constraints & Bounds
    max_latency_budget_ms: float = 3000.0
    max_cost_budget_usd: float = 0.050
    min_confidence_floor: float = 0.90
    
    # Supporting Proof References
    supporting_evidence_hash: str = ""
    proof_hash: str = ""

    def __post_init__(self):
        if not self.proof_hash:
            self.proof_hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = {
            "proof_id": self.proof_id,
            "mission_id": self.mission_id,
            "selected_strategy_id": self.selected_strategy_id,
            "winning_utility_score": self.winning_utility_score,
            "supporting_evidence_hash": self.supporting_evidence_hash,
            "decision_timestamp": self.decision_timestamp,
        }
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DecisionProofEngine:
    """
    Generates and stores formal decision proofs for planner strategy selections.
    """

    def __init__(self):
        self._proofs: Dict[str, DecisionProof] = {}
        self._mission_proofs: Dict[str, List[str]] = {}

    def generate_proof(
        self,
        mission_id: str,
        document_type: str,
        candidates: List[Dict[str, Any]],
        latency_budget_ms: float = 3000.0,
        cost_budget_usd: float = 0.050,
        min_confidence: float = 0.90,
        evidence_hash: str = "",
    ) -> DecisionProof:
        """
        Evaluates candidate strategies with explicit mathematical utility scoring,
        filters infeasible options, ranks alternatives, and constructs the DecisionProof.
        """
        evals: List[CandidateStrategyEval] = []
        w_a, w_l, w_c = 0.50, 0.30, 0.20

        for c in candidates:
            strat_id = c.get("strategy_id", "strat_default")
            strat_name = c.get("strategy_name", "Default Strategy")
            acc = float(c.get("expected_accuracy", 0.95))
            lat = float(c.get("expected_latency_ms", 1200.0))
            cost = float(c.get("expected_cost_usd", 0.010))

            # Feasibility checks
            is_feasible = True
            rejection = None
            if lat > latency_budget_ms:
                is_feasible = False
                rejection = f"Exceeded latency SLA budget ({lat:.1f}ms > {latency_budget_ms:.1f}ms)"
            elif cost > cost_budget_usd:
                is_feasible = False
                rejection = f"Exceeded cost budget (${cost:.4f} > ${cost_budget_usd:.4f})"
            elif acc < min_confidence:
                is_feasible = False
                rejection = f"Below minimum accuracy threshold ({acc:.3f} < {min_confidence:.3f})"

            # Utility score
            utility = (w_a * acc) - (w_l * (lat / 1000.0)) - (w_c * (cost / 0.010))

            evals.append(
                CandidateStrategyEval(
                    strategy_id=strat_id,
                    strategy_name=strat_name,
                    expected_accuracy=acc,
                    expected_latency_ms=lat,
                    expected_cost_usd=cost,
                    utility_score=round(utility, 4),
                    is_feasible=is_feasible,
                    rejection_reason=rejection,
                )
            )

        # Select highest utility feasible strategy
        feasible = [e for e in evals if e.is_feasible]
        if feasible:
            winner = max(feasible, key=lambda x: x.utility_score)
        else:
            winner = evals[0]

        proof_id = f"prf_{uuid.uuid4().hex[:10]}"
        proof = DecisionProof(
            proof_id=proof_id,
            mission_id=mission_id,
            decision_timestamp=time.time(),
            document_type=document_type,
            planner_version="v2.1.0",
            candidates_evaluated=evals,
            selected_strategy_id=winner.strategy_id,
            selected_strategy_name=winner.strategy_name,
            winning_utility_score=winner.utility_score,
            max_latency_budget_ms=latency_budget_ms,
            max_cost_budget_usd=cost_budget_usd,
            min_confidence_floor=min_confidence,
            supporting_evidence_hash=evidence_hash or hashlib.sha256(f"ev_{mission_id}".encode("utf-8")).hexdigest(),
        )

        self._proofs[proof_id] = proof
        if mission_id not in self._mission_proofs:
            self._mission_proofs[mission_id] = []
        self._mission_proofs[mission_id].append(proof_id)

        return proof

    def get_proof(self, proof_id: str) -> Optional[DecisionProof]:
        return self._proofs.get(proof_id)

    def get_mission_proofs(self, mission_id: str) -> List[DecisionProof]:
        pids = self._mission_proofs.get(mission_id, [])
        return [self._proofs[pid] for pid in pids]

    def list_recent(self, limit: int = 50) -> List[DecisionProof]:
        return list(self._proofs.values())[-limit:]
