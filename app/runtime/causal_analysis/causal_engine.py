"""
Causal Analysis - Master Causal Engine Facade
Unifies SCM DAG inspection, do-calculus estimation, and root-cause attribution.
"""

from typing import Dict, List, Any
from app.runtime.causal_analysis.scm import StructuralCausalModel
from app.runtime.causal_analysis.do_calculus import DoCalculusEngine, CausalInterventionResult
from app.runtime.causal_analysis.attribution import CausalAttributionEngine, CausalAttributionItem


class CausalAnalysisEngine:
    """Master engine for causal reasoning and do-calculus interventions."""

    def __init__(self):
        self.scm = StructuralCausalModel()
        self.do_engine = DoCalculusEngine()
        self.attribution_engine = CausalAttributionEngine()

    def get_causal_graph(self) -> Dict[str, Any]:
        return {
            "nodes": self.scm.list_nodes(),
            "graph_type": "Directed Acyclic Graph (DAG)",
            "causal_framework": "Pearl's SCM & Structural Equation Modeling",
        }

    def simulate_do_intervention(
        self,
        treatment: str = "model_choice",
        treatment_value: str = "gemini-1.5-pro",
        outcome: str = "accuracy",
        baseline_value: str = "gemini-2.5-flash",
    ) -> Dict[str, Any]:
        result = self.do_engine.estimate_intervention(
            treatment=treatment,
            treatment_val=treatment_value,
            outcome=outcome,
            baseline_val=baseline_value,
        )
        return result.to_dict()

    def run_root_cause_attribution(
        self,
        target_metric: str = "latency_ms",
        observed_value: float = 2450.0,
        expected_baseline: float = 480.0,
        observed_retry_count: int = 3,
        observed_ocr_confidence: float = 0.68,
        selected_model: str = "gemini-1.5-pro",
    ) -> List[Dict[str, Any]]:
        items = self.attribution_engine.attribute_anomaly(
            target_metric=target_metric,
            observed_value=observed_value,
            expected_baseline=expected_baseline,
            observed_retry_count=observed_retry_count,
            observed_ocr_confidence=observed_ocr_confidence,
            selected_model=selected_model,
        )
        return [item.to_dict() for item in items]
