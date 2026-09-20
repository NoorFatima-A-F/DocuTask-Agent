"""
Counterfactual Simulator - Scenario Generator
Generates realistic alternative environmental scenarios (network load, OCR degradation, API latency spikes).
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class EnvironmentalScenario:
    scenario_id: str
    name: str
    description: str
    latency_multiplier: float
    ocr_confidence_offset: float
    cost_multiplier: float
    anomaly_injection_score: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


CANONICAL_SCENARIOS = [
    EnvironmentalScenario(
        scenario_id="sc_nominal",
        name="Nominal Production",
        description="Standard operational conditions with stable low-latency API responses",
        latency_multiplier=1.0,
        ocr_confidence_offset=0.0,
        cost_multiplier=1.0,
        anomaly_injection_score=0.0,
    ),
    EnvironmentalScenario(
        scenario_id="sc_peak_load",
        name="Extreme Peak Queue Congestion",
        description="Heavy queue backpressure causing 2.5x latency inflation on external LLM calls",
        latency_multiplier=2.5,
        ocr_confidence_offset=-0.02,
        cost_multiplier=1.0,
        anomaly_injection_score=0.25,
    ),
    EnvironmentalScenario(
        scenario_id="sc_degraded_scan",
        name="Degraded Physical Scan Quality",
        description="Severe visual noise, skew, and low DPI lowering base OCR recognition by 15%",
        latency_multiplier=1.2,
        ocr_confidence_offset=-0.15,
        cost_multiplier=1.0,
        anomaly_injection_score=0.35,
    ),
    EnvironmentalScenario(
        scenario_id="sc_cloud_rate_limit",
        name="Cloud API Rate-Limit Throttling",
        description="Transient HTTP 429 throttling causing exponential backoff retries",
        latency_multiplier=3.0,
        ocr_confidence_offset=0.0,
        cost_multiplier=1.1,
        anomaly_injection_score=0.40,
    ),
]


class ScenarioGenerator:
    """Generates environmental perturbations for counterfactual stress testing."""

    @staticmethod
    def list_scenarios() -> List[EnvironmentalScenario]:
        return list(CANONICAL_SCENARIOS)

    @staticmethod
    def apply_scenario_to_features(features: Dict[str, float], scenario: EnvironmentalScenario) -> Dict[str, float]:
        modified = dict(features)
        if "latency_p95_ms" in modified:
            modified["latency_p95_ms"] = min(1.0, modified["latency_p95_ms"] * scenario.latency_multiplier)
        if "ocr_confidence" in modified:
            modified["ocr_confidence"] = max(0.0, min(1.0, modified["ocr_confidence"] + scenario.ocr_confidence_offset))
        if "api_cost_usd" in modified:
            modified["api_cost_usd"] = min(1.0, modified["api_cost_usd"] * scenario.cost_multiplier)
        if "anomaly_score" in modified:
            modified["anomaly_score"] = min(1.0, modified["anomaly_score"] + scenario.anomaly_injection_score)
        return modified
