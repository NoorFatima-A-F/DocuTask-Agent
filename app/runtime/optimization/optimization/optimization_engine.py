"""
Optimization Engine for Phase 13.6 (ARIA-EOP).
Master coordinator managing runtime optimization runs, historical reports, and adaptive re-optimization.
"""

from typing import Dict, List, Optional
from app.runtime.optimization.optimization.optimization_pipeline import OptimizationPipeline, OptimizationReport
from app.runtime.optimization.optimization.strategy_selector import CandidateExecutionStrategy


class OptimizationEngine:
    """
    Master coordinator for ARIA-EOP decision and resource optimization.
    """

    def __init__(self):
        self._reports: Dict[str, OptimizationReport] = {}
        # Pre-seed a baseline report
        self.optimize_mission("mission-001")

    def optimize_mission(
        self,
        mission_id: str,
        candidates: Optional[List[CandidateExecutionStrategy]] = None,
        objective: str = "BALANCED_UTILITY",
        max_budget_usd: float = 0.50,
        max_latency_ms: float = 5000.0,
        min_confidence: float = 0.85,
    ) -> OptimizationReport:
        report = OptimizationPipeline.execute(
            mission_id=mission_id,
            candidates=candidates,
            objective=objective,
            max_budget_usd=max_budget_usd,
            max_latency_ms=max_latency_ms,
            min_confidence=min_confidence,
        )
        self._reports[report.optimization_id] = report
        self._reports[mission_id] = report
        return report

    def list_reports(self) -> List[OptimizationReport]:
        unique = {}
        for r in self._reports.values():
            unique[r.optimization_id] = r
        return list(unique.values())

    def get_report(self, identifier: str) -> Optional[OptimizationReport]:
        return self._reports.get(identifier)


optimization_engine = OptimizationEngine()
