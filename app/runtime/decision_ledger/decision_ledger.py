"""Append-Only Planner Decision Ledger.

Records every planning event, candidate evaluation matrix, and regret calculation
in an immutable hash-chained ledger.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.runtime.decision_ledger.candidate_plan_evaluator import (
    CandidatePlan,
    CandidatePlanEvaluator,
    RegretCalculator,
    RegretReport,
)


@dataclass
class PlannerDecisionEntry:
    entry_id: str
    decision_id: str
    mission_id: str
    timestamp: float
    selected_plan: CandidatePlan
    candidate_plans: List[CandidatePlan]
    selection_rationale: str
    regret_report: Optional[RegretReport] = None
    previous_entry_hash: str = ""
    entry_hash: str = ""

    def compute_hash(self) -> str:
        payload = {
            "entry_id": self.entry_id,
            "decision_id": self.decision_id,
            "mission_id": self.mission_id,
            "timestamp": round(self.timestamp, 4),
            "selected_plan": self.selected_plan.to_dict(),
            "candidate_plans": [c.to_dict() for c in self.candidate_plans],
            "selection_rationale": self.selection_rationale,
            "previous_entry_hash": self.previous_entry_hash,
        }
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "decision_id": self.decision_id,
            "mission_id": self.mission_id,
            "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.timestamp)),
            "selected_plan": self.selected_plan.to_dict(),
            "candidate_plans": [c.to_dict() for c in self.candidate_plans],
            "selection_rationale": self.selection_rationale,
            "regret_report": self.regret_report.to_dict() if self.regret_report else None,
            "previous_entry_hash": self.previous_entry_hash,
            "entry_hash": self.entry_hash,
        }


class DecisionLedger:
    def __init__(self):
        self._entries: List[PlannerDecisionEntry] = []
        self._last_hash: str = "genesis_decision_block_0000"

    def record_decision(
        self,
        decision_id: str,
        mission_id: str,
        candidates_raw: List[Dict[str, Any]],
        selection_rationale: str = "Optimal utility under cost & latency bounds",
        realized_metrics: Optional[Dict[str, float]] = None,
    ) -> PlannerDecisionEntry:
        evaluated_candidates = CandidatePlanEvaluator.evaluate_candidates(candidates_raw)
        selected = evaluated_candidates[0] if evaluated_candidates else CandidatePlan(
            candidate_id="default-fallback",
            model="gemini-2.5-flash",
            dag_depth=1,
            parallelism=1,
            predicted_cost_usd=0.001,
            predicted_latency_ms=200.0,
            predicted_accuracy=0.95,
            estimated_utility=0.8,
            constraints_satisfied=True,
            selection_score=0.8,
        )

        regret = None
        if realized_metrics:
            regret = RegretCalculator.calculate_regret(
                decision_id=decision_id,
                selected_candidate=selected,
                realized_metrics=realized_metrics,
                all_candidates=evaluated_candidates,
            )

        entry = PlannerDecisionEntry(
            entry_id=f"pde-{len(self._entries) + 1:04d}",
            decision_id=decision_id,
            mission_id=mission_id,
            timestamp=time.time(),
            selected_plan=selected,
            candidate_plans=evaluated_candidates,
            selection_rationale=selection_rationale,
            regret_report=regret,
            previous_entry_hash=self._last_hash,
        )
        entry.entry_hash = entry.compute_hash()
        self._last_hash = entry.entry_hash
        self._entries.append(entry)
        return entry

    def list_entries(self) -> List[PlannerDecisionEntry]:
        return list(self._entries)

    def get_entry(self, entry_id: str) -> Optional[PlannerDecisionEntry]:
        for e in self._entries:
            if e.entry_id == entry_id or e.decision_id == entry_id:
                return e
        return None

    def verify_chain(self) -> bool:
        prev = "genesis_decision_block_0000"
        for e in self._entries:
            if e.previous_entry_hash != prev:
                return False
            if e.compute_hash() != e.entry_hash:
                return False
            prev = e.entry_hash
        return True

    def count(self) -> int:
        return len(self._entries)

    def clear(self) -> None:
        self._entries.clear()
        self._last_hash = "genesis_decision_block_0000"


global_decision_ledger = DecisionLedger()
