"""Strategy Ranking Engine & Comparison Matrix for DocuTask Autonomous Planning Platform.

Computes the Pareto efficiency frontier, ranks candidate strategies by composite utility,
and produces an auditable selection justification with exact rejection reasons for every discarded alternative.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.runtime.planning.strategy_generator import CandidateStrategy
from app.runtime.planning.utility_engine import UtilityScore
from app.runtime.planning.cost_predictor import CostPredictionResult
from app.runtime.planning.latency_predictor import LatencyPredictionResult
from app.runtime.planning.risk_engine import StrategyRiskProfile


class StrategyComparisonEntry(BaseModel):
    """Single row in the Strategy Comparison Matrix."""
    strategy_id: str
    archetype: str
    name: str
    rank: int
    utility_score: float
    accuracy: float
    critical_path_ms: float
    total_cost_usd: float
    risk_score: float
    token_estimate: int
    is_pareto_optimal: bool
    is_valid: bool
    violations: List[str] = Field(default_factory=list)
    rejection_reason: Optional[str] = None


class StrategyComparisonMatrix(BaseModel):
    """Full comparative evaluation matrix across all candidate strategies."""
    mission_id: str
    entries: List[StrategyComparisonEntry] = Field(default_factory=list)
    pareto_frontier_strategy_ids: List[str] = Field(default_factory=list)
    selected_strategy_id: str
    version: str = "1.0.0"


class StrategySelectionRecord(BaseModel):
    """Complete auditable selection decision package."""
    selected_strategy_id: str
    selected_archetype: str
    selection_rationale: str
    rejection_reasons: Dict[str, str] = Field(default_factory=dict)
    comparison_matrix: StrategyComparisonMatrix
    utility_breakdown: UtilityScore


class StrategyRankingEngine:
    """Ranks candidate strategies, computes Pareto efficiency, and explains selection trade-offs."""

    def evaluate_and_rank(
        self,
        mission_id: str,
        strategies: List[CandidateStrategy],
        utility_scores: Dict[str, UtilityScore],
        cost_predictions: Dict[str, CostPredictionResult],
        latency_predictions: Dict[str, LatencyPredictionResult],
        risk_profiles: Dict[str, StrategyRiskProfile],
    ) -> StrategySelectionRecord:
        # 1. Identify Pareto Frontier
        pareto_ids = self._compute_pareto_frontier(strategies)

        # 2. Sort candidates by utility (highest first)
        # Invalid strategies get demoted
        def sort_key(s: CandidateStrategy) -> float:
            is_val = s.constraint_compliance.get("is_valid", True)
            u_score = utility_scores.get(s.strategy_id).total_utility if s.strategy_id in utility_scores else -1.0
            return u_score if is_val else u_score - 1000.0

        sorted_strategies = sorted(strategies, key=sort_key, reverse=True)
        selected = sorted_strategies[0]

        # 3. Construct comparison entries and rejection explanations
        entries: List[StrategyComparisonEntry] = []
        rejection_reasons: Dict[str, str] = {}

        for rank, strat in enumerate(sorted_strategies, start=1):
            is_sel = (strat.strategy_id == selected.strategy_id)
            u_score = utility_scores[strat.strategy_id].total_utility
            cost_p = cost_predictions[strat.strategy_id]
            lat_p = latency_predictions[strat.strategy_id]
            risk_p = risk_profiles[strat.strategy_id]
            is_val = strat.constraint_compliance.get("is_valid", True)
            violations = strat.constraint_compliance.get("violations", [])

            rejection_msg = None
            if not is_sel:
                if not is_val:
                    rejection_msg = f"Hard constraint violation: {'; '.join(violations)}"
                elif u_score < utility_scores[selected.strategy_id].total_utility:
                    delta_u = utility_scores[selected.strategy_id].total_utility - u_score
                    rejection_msg = f"Suboptimal utility (\\Delta U = -{delta_u:.3f}): Higher net penalty from {self._identify_tradeoff(strat, selected)}."
                rejection_reasons[strat.strategy_id] = rejection_msg or "Lower overall multi-objective score."

            entries.append(
                StrategyComparisonEntry(
                    strategy_id=strat.strategy_id,
                    archetype=strat.archetype.value,
                    name=strat.name,
                    rank=rank,
                    utility_score=u_score,
                    accuracy=strat.estimated_accuracy,
                    critical_path_ms=lat_p.critical_path_ms,
                    total_cost_usd=cost_p.total_cost_usd,
                    risk_score=risk_p.overall_risk_score,
                    token_estimate=strat.token_estimate,
                    is_pareto_optimal=strat.strategy_id in pareto_ids,
                    is_valid=is_val,
                    violations=violations,
                    rejection_reason=rejection_msg,
                )
            )

        matrix = StrategyComparisonMatrix(
            mission_id=mission_id,
            entries=entries,
            pareto_frontier_strategy_ids=pareto_ids,
            selected_strategy_id=selected.strategy_id,
        )

        rationale = (
            f"Selected {selected.name} with highest multi-objective utility score ({utility_scores[selected.strategy_id].total_utility:.4f}). "
            f"Provides optimal trade-off: {selected.estimated_accuracy*100:.1f}% accuracy at ${cost_predictions[selected.strategy_id].total_cost_usd:.4f} cost "
            f"and {latency_predictions[selected.strategy_id].critical_path_ms:.1f}ms critical path latency."
        )

        return StrategySelectionRecord(
            selected_strategy_id=selected.strategy_id,
            selected_archetype=selected.archetype.value,
            selection_rationale=rationale,
            rejection_reasons=rejection_reasons,
            comparison_matrix=matrix,
            utility_breakdown=utility_scores[selected.strategy_id],
        )

    def _compute_pareto_frontier(self, strategies: List[CandidateStrategy]) -> List[str]:
        """Identifies non-dominated strategies across (Accuracy [max], Latency [min], Cost [min], Risk [min])."""
        pareto_ids: List[str] = []
        for s1 in strategies:
            dominated = False
            for s2 in strategies:
                if s1.strategy_id == s2.strategy_id:
                    continue
                # s2 dominates s1 if s2 is as good or better in all 4 dimensions AND strictly better in at least one
                better_or_equal = (
                    s2.estimated_accuracy >= s1.estimated_accuracy and
                    s2.estimated_critical_path_ms <= s1.estimated_critical_path_ms and
                    s2.estimated_total_cost_usd <= s1.estimated_total_cost_usd and
                    s2.estimated_risk_score <= s1.estimated_risk_score
                )
                strictly_better = (
                    s2.estimated_accuracy > s1.estimated_accuracy or
                    s2.estimated_critical_path_ms < s1.estimated_critical_path_ms or
                    s2.estimated_total_cost_usd < s1.estimated_total_cost_usd or
                    s2.estimated_risk_score < s1.estimated_risk_score
                )
                if better_or_equal and strictly_better:
                    dominated = True
                    break
            if not dominated:
                pareto_ids.append(s1.strategy_id)
        return pareto_ids

    def _identify_tradeoff(self, cand: CandidateStrategy, best: CandidateStrategy) -> str:
        reasons = []
        if cand.estimated_total_cost_usd > best.estimated_total_cost_usd * 1.5:
            reasons.append("excessive cost")
        if cand.estimated_critical_path_ms > best.estimated_critical_path_ms * 1.5:
            reasons.append("excessive latency")
        if cand.estimated_risk_score > best.estimated_risk_score * 1.5:
            reasons.append("elevated risk")
        if cand.estimated_accuracy < best.estimated_accuracy:
            reasons.append("lower accuracy")
        return ", ".join(reasons) if reasons else "lower composite score"
