"""
Scientific Model Router - Routing History
Maintains provenance records for model routing decisions and predicted vs actual metrics.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class ModelRoutingDecisionRecord:
    decision_id: str
    timestamp_utc: str
    task_id: str
    selected_model: str
    expected_accuracy: float
    expected_cost_usd: float
    expected_latency_ms: float
    expected_utility: float
    candidate_models: List[Dict[str, Any]]
    selection_reason: str


class ModelRoutingHistory:
    """Stores queryable history of model routing decisions."""

    def __init__(self, max_entries: int = 500):
        self.max_entries = max_entries
        self._history: List[ModelRoutingDecisionRecord] = []

    def record(self, record: ModelRoutingDecisionRecord) -> None:
        self._history.append(record)
        if len(self._history) > self.max_entries:
            self._history.pop(0)

    def list_recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        return [asdict(r) for r in reversed(self._history[-limit:])]


routing_history = ModelRoutingHistory()
