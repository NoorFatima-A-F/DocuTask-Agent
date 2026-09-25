"""
Predictive Mission Intelligence for Phase 10 (AISLCOP).

Predicts expected latency, cost, retries, confidence, escalation risk, and planner depth
prior to mission execution, then verifies predictions against runtime reality.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional

from app.runtime.intelligence.experience.experience_record import ExperienceRecord


@dataclass
class MissionPrediction:
    prediction_id: str
    mission_id: str
    document_type: str
    predicted_at: float = field(default_factory=time.time)
    
    # Pre-execution Forecasts
    predicted_latency_ms: float = 1200.0
    predicted_cost_usd: float = 0.012
    predicted_confidence: float = 0.95
    predicted_retries: int = 0
    escalation_risk_prob: float = 0.05  # [0.0, 1.0]
    expected_dag_depth: int = 3
    expected_memory_reuse_rate: float = 0.75
    
    # Actual Post-execution Telemetry (populated when mission finishes)
    actual_latency_ms: Optional[float] = None
    actual_cost_usd: Optional[float] = None
    actual_confidence: Optional[float] = None
    actual_retries: Optional[int] = None
    actual_escalated: Optional[bool] = None
    
    # Prediction Error Evaluation
    latency_abs_error_ms: Optional[float] = None
    cost_abs_error_usd: Optional[float] = None
    confidence_abs_error: Optional[float] = None
    prediction_accuracy_score: float = 1.0
    prediction_hash: str = ""

    def __post_init__(self):
        if not self.prediction_hash:
            self.prediction_hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = {
            "prediction_id": self.prediction_id,
            "mission_id": self.mission_id,
            "document_type": self.document_type,
            "predicted_latency_ms": self.predicted_latency_ms,
            "predicted_cost_usd": self.predicted_cost_usd,
            "predicted_confidence": self.predicted_confidence,
            "predicted_at": self.predicted_at,
        }
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PredictiveMissionEngine:
    """
    Generates pre-execution forecasts and evaluates predictive accuracy convergence.
    """

    def __init__(self):
        self._predictions: Dict[str, MissionPrediction] = {}

    def forecast_mission(
        self,
        mission_id: str,
        document_type: str,
        task_type: str = "extraction",
        doc_size_bytes: int = 150000,
        historical_experiences: Optional[List[ExperienceRecord]] = None,
    ) -> MissionPrediction:
        """
        Calculates pre-execution predictions based on historical distributions and document heuristics.
        """
        exps = [e for e in (historical_experiences or []) if e.document_type.lower() == document_type.lower()]
        
        if exps:
            base_lat = sum(e.total_latency_ms for e in exps) / len(exps)
            base_cost = sum(e.total_cost_usd for e in exps) / len(exps)
            base_conf = sum(e.final_confidence for e in exps) / len(exps)
            base_retries = int(round(sum(e.retries_count for e in exps) / len(exps)))
        else:
            # Domain-based initial priors
            priors = {
                "invoice": (950.0, 0.008, 0.96, 0),
                "contract": (2200.0, 0.035, 0.92, 0),
                "medical": (1800.0, 0.028, 0.94, 0),
            }
            base_lat, base_cost, base_conf, base_retries = priors.get(document_type.lower(), (1200.0, 0.012, 0.95, 0))

        # Size scaling factor
        size_factor = max(0.8, min(2.5, doc_size_bytes / 100000.0))
        predicted_lat = round(base_lat * (0.7 + 0.3 * size_factor), 2)
        predicted_cost = round(base_cost * (0.8 + 0.2 * size_factor), 6)

        pred = MissionPrediction(
            prediction_id=f"pred_{hashlib.sha256(mission_id.encode('utf-8')).hexdigest()[:10]}",
            mission_id=mission_id,
            document_type=document_type,
            predicted_at=time.time(),
            predicted_latency_ms=predicted_lat,
            predicted_cost_usd=predicted_cost,
            predicted_confidence=round(base_conf, 4),
            predicted_retries=base_retries,
            escalation_risk_prob=0.04 if base_conf > 0.95 else 0.12,
            expected_dag_depth=3 if document_type.lower() == "invoice" else 5,
            expected_memory_reuse_rate=0.82,
        )

        self._predictions[pred.prediction_id] = pred
        return pred

    def evaluate_actuals(
        self,
        prediction_id: str,
        actual_telemetry: Dict[str, Any],
    ) -> Optional[MissionPrediction]:
        """
        Evaluates forecast error once actual mission telemetry is received.
        """
        pred = self._predictions.get(prediction_id)
        if not pred:
            return None

        act_lat = actual_telemetry.get("total_latency_ms", pred.predicted_latency_ms)
        act_cost = actual_telemetry.get("total_cost_usd", pred.predicted_cost_usd)
        act_conf = actual_telemetry.get("final_confidence", pred.predicted_confidence)
        act_ret = actual_telemetry.get("retries_count", pred.predicted_retries)

        lat_err = abs(act_lat - pred.predicted_latency_ms)
        cost_err = abs(act_cost - pred.predicted_cost_usd)
        conf_err = abs(act_conf - pred.predicted_confidence)

        # Accuracy score: bounded [0.0, 1.0] based on relative errors
        rel_lat_err = lat_err / max(act_lat, 1.0)
        rel_cost_err = cost_err / max(act_cost, 0.0001)
        acc_score = max(0.0, 1.0 - 0.5 * rel_lat_err - 0.5 * rel_cost_err - conf_err)

        pred.actual_latency_ms = act_lat
        pred.actual_cost_usd = act_cost
        pred.actual_confidence = act_conf
        pred.actual_retries = act_ret
        pred.actual_escalated = actual_telemetry.get("escalated", False)
        pred.latency_abs_error_ms = round(lat_err, 2)
        pred.cost_abs_error_usd = round(cost_err, 6)
        pred.confidence_abs_error = round(conf_err, 4)
        pred.prediction_accuracy_score = round(acc_score, 4)

        return pred

    def get(self, prediction_id: str) -> Optional[MissionPrediction]:
        return self._predictions.get(prediction_id)

    def list_all(self, limit: int = 50) -> List[MissionPrediction]:
        return list(self._predictions.values())[-limit:]
