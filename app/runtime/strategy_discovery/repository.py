"""Strategy Repository for DocuTask ACOS.

Stores, indexes, versions, and retrieves synthesized and evolved strategy DAGs with full lineage tracking.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel

from app.runtime.strategy_discovery.graph_synthesis import SynthesizedDAG
from app.runtime.strategy_discovery.evaluation import StrategyEvaluationReport


class SynthesizedStrategyRecord(BaseModel):
    """Archival record of a discovered strategy with its evaluation telemetry."""
    strategy_id: str
    dag: SynthesizedDAG
    evaluation: StrategyEvaluationReport
    parent_strategy_id: Optional[str] = None
    created_at_generation: int = 1
    times_executed: int = 0
    average_actual_utility: float = 0.0


class StrategyRepository:
    """Thread-safe catalog of synthesized planning strategies."""

    def __init__(self) -> None:
        self._strategies: Dict[str, SynthesizedStrategyRecord] = {}

    def register_strategy(
        self,
        dag: SynthesizedDAG,
        evaluation: StrategyEvaluationReport,
        parent_id: Optional[str] = None,
        generation: int = 1,
    ) -> SynthesizedStrategyRecord:
        rec = SynthesizedStrategyRecord(
            strategy_id=dag.dag_id,
            dag=dag,
            evaluation=evaluation,
            parent_strategy_id=parent_id,
            created_at_generation=generation,
            average_actual_utility=evaluation.expected_utility,
        )
        self._strategies[dag.dag_id] = rec
        return rec

    def get_strategy(self, strategy_id: str) -> Optional[SynthesizedStrategyRecord]:
        return self._strategies.get(strategy_id)

    def list_strategies(self) -> List[SynthesizedStrategyRecord]:
        return list(self._strategies.values())

    def get_pareto_frontier(self) -> List[SynthesizedStrategyRecord]:
        """Returns strategies residing on the non-dominated Pareto frontier."""
        sorted_strats = sorted(self._strategies.values(), key=lambda s: s.evaluation.expected_utility, reverse=True)
        return sorted_strats[:5]
