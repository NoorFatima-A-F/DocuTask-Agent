"""
Scientific Risk Engine - Failure Predictor
Forecasts execution path failure likelihood along DAG task nodes.
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class NodeRiskPrediction:
    node_id: str
    failure_probability: float
    critical_factor: str
    risk_level: str


class DAGFailurePredictor:
    """Predicts failure risks along planned DAG execution nodes."""

    @staticmethod
    def predict_dag_nodes(nodes: List[Dict[str, Any]], features: Dict[str, float]) -> List[NodeRiskPrediction]:
        predictions: List[NodeRiskPrediction] = []
        base_ocr_risk = (1.0 - features.get("ocr_confidence", 0.85))
        base_val_risk = (1.0 - features.get("schema_validation_score", 1.0))

        for node in nodes:
            node_id = node.get("id", "task_node")
            task_type = node.get("type", "generic").lower()

            if "ocr" in task_type or "extract" in task_type:
                p_fail = min(0.95, base_ocr_risk * 1.5 + 0.05)
                crit = "OCR scan degradation"
            elif "validate" in task_type or "schema" in task_type:
                p_fail = min(0.95, base_val_risk * 2.0 + 0.02)
                crit = "Strict schema invariant violation"
            elif "reconcile" in task_type or "llm" in task_type:
                p_fail = min(0.95, 0.10 + 0.4 * features.get("epistemic_uncertainty", 0.1))
                crit = "Complex entity reconciliation ambiguity"
            else:
                p_fail = min(0.95, 0.05 + 0.2 * features.get("anomaly_score", 0.05))
                crit = "System queue pressure"

            level = "CRITICAL" if p_fail > 0.4 else ("HIGH" if p_fail > 0.2 else ("MEDIUM" if p_fail > 0.08 else "LOW"))

            predictions.append(
                NodeRiskPrediction(
                    node_id=node_id,
                    failure_probability=round(p_fail, 4),
                    critical_factor=crit,
                    risk_level=level,
                )
            )

        return predictions
