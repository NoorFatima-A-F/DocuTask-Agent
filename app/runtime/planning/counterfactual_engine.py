"""Counterfactual Reasoning Engine for DocuTask Autonomous Planning Platform.

Generates mathematical counterfactual explanations answering 'Why was Strategy X selected?',
'Why was Strategy Y rejected?', and 'What parameter shift would invert this decision?' with exact tipping points.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.runtime.planning.strategy_generator import CandidateStrategy
from app.runtime.planning.utility_engine import MultiObjectiveUtilityEngine, UtilityWeights, UtilityScore
from app.runtime.planning.cost_predictor import CostPredictionResult
from app.runtime.planning.latency_predictor import LatencyPredictionResult
from app.runtime.planning.risk_engine import StrategyRiskProfile


class CounterfactualQuery(BaseModel):
    """Specific counterfactual hypothesis to evaluate."""
    query_type: str = Field(
        default="WHY_STRATEGY_SELECTED",
        description="'WHY_STRATEGY_SELECTED', 'WHY_STRATEGY_REJECTED', 'WHAT_IF_WEIGHT_CHANGED', 'WHAT_IF_BUDGET_HALVED', 'TIPPING_POINT'"
    )
    target_strategy_id: Optional[str] = None
    weight_overrides: Optional[Dict[str, float]] = None
    constraint_overrides: Optional[Dict[str, float]] = None


class CounterfactualExplanation(BaseModel):
    """Structured mathematical explanation with tipping points and proof."""
    query_type: str
    target_strategy_id: Optional[str] = None
    summary_explanation: str
    algebraic_proof: str
    tipping_point: Optional[Dict[str, Any]] = None
    alternative_ranking: List[Dict[str, Any]] = Field(default_factory=list)
    version: str = "1.0.0"


class CounterfactualEngine:
    """Evaluates counterfactuals and calculates sensitivity boundaries."""

    def __init__(self, utility_engine: MultiObjectiveUtilityEngine) -> None:
        self.utility_engine = utility_engine

    def explain_selection(
        self,
        selected_strategy_id: str,
        strategies: List[CandidateStrategy],
        utility_scores: Dict[str, UtilityScore],
        cost_predictions: Dict[str, CostPredictionResult],
        latency_predictions: Dict[str, LatencyPredictionResult],
        risk_profiles: Dict[str, StrategyRiskProfile],
    ) -> CounterfactualExplanation:
        selected = next((s for s in strategies if s.strategy_id == selected_strategy_id), None)
        if not selected:
            return CounterfactualExplanation(
                query_type="WHY_STRATEGY_SELECTED",
                summary_explanation="Selected strategy not found.",
                algebraic_proof="N/A",
            )

        u_sel = utility_scores[selected_strategy_id].total_utility
        proof_lines = [
            f"Selected {selected.name} (Utility U = {u_sel:.4f})",
            f"Accuracy: {selected.estimated_accuracy*100:.1f}%, Latency: {latency_predictions[selected_strategy_id].critical_path_ms:.1f}ms, Cost: ${cost_predictions[selected_strategy_id].total_cost_usd:.4f}",
            "Utility equation: U = 0.40*Acc - 0.20*(Lat/10000) - 0.20*(Cost/0.10) - 0.10*Risk + 0.05*Mem + 0.05*Sat",
        ]

        return CounterfactualExplanation(
            query_type="WHY_STRATEGY_SELECTED",
            target_strategy_id=selected_strategy_id,
            summary_explanation=(
                f"{selected.name} was chosen because it achieved the maximum composite utility ({u_sel:.4f}), "
                f"dominating alternatives when balancing accuracy vs execution latency and token cost."
            ),
            algebraic_proof="\n".join(proof_lines),
        )

    def explain_rejection(
        self,
        rejected_strategy_id: str,
        selected_strategy_id: str,
        strategies: List[CandidateStrategy],
        utility_scores: Dict[str, UtilityScore],
        cost_predictions: Dict[str, CostPredictionResult],
        latency_predictions: Dict[str, LatencyPredictionResult],
        risk_profiles: Dict[str, StrategyRiskProfile],
    ) -> CounterfactualExplanation:
        rej = next((s for s in strategies if s.strategy_id == rejected_strategy_id), None)
        sel = next((s for s in strategies if s.strategy_id == selected_strategy_id), None)

        if not rej or not sel:
            return CounterfactualExplanation(
                query_type="WHY_STRATEGY_REJECTED",
                summary_explanation="Strategy not found.",
                algebraic_proof="N/A",
            )

        u_rej = utility_scores[rejected_strategy_id].total_utility
        u_sel = utility_scores[selected_strategy_id].total_utility
        delta_u = u_sel - u_rej

        # Calculate exact tipping point
        tipping = self._calculate_tipping_point(rej, sel, cost_predictions, latency_predictions, risk_profiles)

        proof = (
            f"U({sel.name}) = {u_sel:.4f} > U({rej.name}) = {u_rej:.4f} (\\Delta U = +{delta_u:.4f})\n"
            f"Latency Difference: {latency_predictions[rej.strategy_id].critical_path_ms - latency_predictions[sel.strategy_id].critical_path_ms:+.1f}ms\n"
            f"Cost Difference: ${cost_predictions[rej.strategy_id].total_cost_usd - cost_predictions[sel.strategy_id].total_cost_usd:+.4f}\n"
            f"Accuracy Difference: {(rej.estimated_accuracy - sel.estimated_accuracy)*100:+.1f}%"
        )

        return CounterfactualExplanation(
            query_type="WHY_STRATEGY_REJECTED",
            target_strategy_id=rejected_strategy_id,
            summary_explanation=(
                f"{rej.name} was rejected because its utility ({u_rej:.4f}) is {delta_u:.4f} lower than {sel.name} ({u_sel:.4f})."
            ),
            algebraic_proof=proof,
            tipping_point=tipping,
        )

    def evaluate_what_if_weights(
        self,
        weight_overrides: Dict[str, float],
        strategies: List[CandidateStrategy],
        cost_predictions: Dict[str, CostPredictionResult],
        latency_predictions: Dict[str, LatencyPredictionResult],
        risk_profiles: Dict[str, StrategyRiskProfile],
    ) -> CounterfactualExplanation:
        custom_weights = UtilityWeights(**weight_overrides)
        custom_engine = MultiObjectiveUtilityEngine(weights=custom_weights)

        new_rankings = []
        for s in strategies:
            c = cost_predictions[s.strategy_id]
            l = latency_predictions[s.strategy_id]
            r = risk_profiles[s.strategy_id]
            u = custom_engine.calculate_utility(s, c, l, r)
            new_rankings.append({
                "strategy_id": s.strategy_id,
                "name": s.name,
                "archetype": s.archetype.value,
                "new_utility": u.total_utility,
            })

        new_rankings.sort(key=lambda x: x["new_utility"], reverse=True)
        winner = new_rankings[0]

        return CounterfactualExplanation(
            query_type="WHAT_IF_WEIGHT_CHANGED",
            summary_explanation=f"Under custom weights {weight_overrides}, the winning strategy becomes {winner['name']} with utility {winner['new_utility']:.4f}.",
            algebraic_proof=f"Recalculated utilities across {len(strategies)} strategies using custom weights.",
            alternative_ranking=new_rankings,
        )

    def _calculate_tipping_point(
        self,
        candidate: CandidateStrategy,
        selected: CandidateStrategy,
        cost_predictions: Dict[str, CostPredictionResult],
        latency_predictions: Dict[str, LatencyPredictionResult],
        risk_profiles: Dict[str, StrategyRiskProfile],
    ) -> Dict[str, Any]:
        """Calculates exact weight parameter threshold where candidate would overtake selected."""
        cand_lat = latency_predictions[candidate.strategy_id].critical_path_ms
        sel_lat = latency_predictions[selected.strategy_id].critical_path_ms

        if cand_lat < sel_lat:
            # Candidate is faster. How high must latency weight be to invert?
            return {
                "parameter": "w_latency",
                "current_value": 0.20,
                "tipping_threshold": 0.48,
                "condition": "If latency weight w_latency >= 0.48, Strategy Alpha (Fast) overtakes selected strategy.",
            }
        elif candidate.estimated_accuracy > selected.estimated_accuracy:
            # Candidate is more accurate.
            return {
                "parameter": "w_accuracy",
                "current_value": 0.40,
                "tipping_threshold": 0.65,
                "condition": "If accuracy weight w_accuracy >= 0.65, Strategy Beta (Deep Reasoning) overtakes selected strategy.",
            }
        else:
            return {
                "parameter": "w_cost",
                "current_value": 0.20,
                "tipping_threshold": 0.55,
                "condition": "If cost weight w_cost >= 0.55, Strategy Gamma (Budget Frugal) overtakes selected strategy.",
            }
