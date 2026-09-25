"""
Scientific Feature Store - Feature Engine
Computes, aggregates, and transforms raw telemetry and context into runtime features.
"""

from typing import Dict, Any, Optional
from app.runtime.feature_store.feature_registry import feature_registry


class FeatureEngine:
    """Extracts and computes structured runtime features from mission & execution telemetry."""

    @staticmethod
    def extract_from_telemetry(telemetry: Dict[str, Any], document_context: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        """Extracts canonical feature vector from runtime telemetry objects."""
        doc = document_context or {}
        defaults = feature_registry.get_defaults()

        extracted: Dict[str, float] = {}

        # 1. OCR Confidence
        extracted["ocr_confidence"] = float(telemetry.get("ocr_confidence", doc.get("ocr_confidence", defaults["ocr_confidence"])))

        # 2. Schema Validation Score
        extracted["schema_validation_score"] = float(telemetry.get("schema_validation_score", doc.get("validation_score", defaults["schema_validation_score"])))

        # 3. Latency p95 in ms
        extracted["latency_p95_ms"] = float(telemetry.get("latency_ms", telemetry.get("latency_p95_ms", defaults["latency_p95_ms"])))

        # 4. Historical Success Rate
        extracted["historical_success_rate"] = float(telemetry.get("historical_success_rate", defaults["historical_success_rate"]))

        # 5. Retry Count
        extracted["retry_count"] = float(telemetry.get("retry_count", 0.0))

        # 6. Memory Similarity
        extracted["memory_similarity"] = float(telemetry.get("memory_similarity", doc.get("memory_similarity", defaults["memory_similarity"])))

        # 7. Document Complexity
        page_count = float(doc.get("page_count", 1.0))
        table_count = float(doc.get("table_count", 0.0))
        calculated_complexity = min(1.0, 0.1 * page_count + 0.15 * table_count + 0.2)
        extracted["document_complexity"] = float(telemetry.get("document_complexity", doc.get("complexity", calculated_complexity)))

        # 8. Worker Reliability
        extracted["worker_reliability"] = float(telemetry.get("worker_reliability", defaults["worker_reliability"]))

        # 9. GPU Load
        extracted["gpu_load"] = float(telemetry.get("gpu_load", defaults["gpu_load"]))

        # 10. Queue Length
        extracted["queue_length"] = float(telemetry.get("queue_length", defaults["queue_length"]))

        # 11. API Cost USD
        extracted["api_cost_usd"] = float(telemetry.get("api_cost_usd", telemetry.get("cost", defaults["api_cost_usd"])))

        # 12. Token Count
        extracted["token_count"] = float(telemetry.get("token_count", defaults["token_count"]))

        # 13. Human Validation Rate
        extracted["human_validation_rate"] = float(telemetry.get("human_validation_rate", defaults["human_validation_rate"]))

        # 14. Compliance Flags
        extracted["compliance_flags"] = float(telemetry.get("compliance_flags", 0.0))

        # 15. Anomaly Score
        extracted["anomaly_score"] = float(telemetry.get("anomaly_score", defaults["anomaly_score"]))

        # 16. Epistemic Uncertainty
        extracted["epistemic_uncertainty"] = float(telemetry.get("epistemic_uncertainty", defaults["epistemic_uncertainty"]))

        # Ensure all defined canonical features exist
        for k, v in defaults.items():
            if k not in extracted:
                extracted[k] = v

        return extracted
