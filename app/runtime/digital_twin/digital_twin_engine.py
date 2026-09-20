"""
Digital Twin Runtime - Engine Facade
Coordinates sandboxing, shadow executions, and fidelity tracking.
"""

from typing import Dict, List, Any, Optional
from app.runtime.digital_twin.safety_sandbox import SafetySandbox, SandboxSecurityPolicy
from app.runtime.digital_twin.fidelity_monitor import FidelityMonitor
from app.runtime.digital_twin.shadow_executor import ShadowExecutor, ShadowExecutionResult


class DigitalTwinEngine:
    """Master engine for the Digital Twin Shadow Execution environment."""

    def __init__(self):
        self.sandbox = SafetySandbox()
        self.fidelity_monitor = FidelityMonitor()
        self.shadow_executor = ShadowExecutor()
        self.history: List[ShadowExecutionResult] = []

    def run_shadow_simulation(
        self,
        mission_id: str,
        prod_policy: str = "v4.2-pareto",
        shadow_policy: str = "v5.0-bayesian-candidate",
        prod_output: str = "Invoice INV-2026 total $1,420.50 parsed with high confidence.",
        prod_latency_ms: float = 520.0,
        prod_tokens: int = 1250,
        prod_decision: str = "EXECUTE_PARALLEL_FLASH",
    ) -> Dict[str, Any]:
        result = self.shadow_executor.mirror_and_execute(
            mission_id=mission_id,
            prod_policy=prod_policy,
            shadow_policy=shadow_policy,
            prod_output=prod_output,
            prod_latency_ms=prod_latency_ms,
            prod_tokens=prod_tokens,
            prod_decision=prod_decision,
        )
        self.history.append(result)
        return result.to_dict()

    def get_shadow_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.history[-limit:]]

    def get_aggregated_fidelity(self) -> Dict[str, Any]:
        if not self.history:
            return {
                "total_shadow_runs": 0,
                "avg_output_agreement": 1.0,
                "avg_latency_divergence_pct": 0.0,
                "overall_status": "READY",
            }

        agreements = [h.fidelity["output_agreement_score"] for h in self.history]
        lat_divs = [h.fidelity["latency_divergence_pct"] for h in self.history]

        return {
            "total_shadow_runs": len(self.history),
            "avg_output_agreement": round(sum(agreements) / len(agreements), 4),
            "avg_latency_divergence_pct": round(sum(lat_divs) / len(lat_divs), 2),
            "overall_status": "OPTIMAL_FIDELITY",
        }
