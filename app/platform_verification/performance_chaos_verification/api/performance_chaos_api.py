"""
In-process REST API Router for Performance, Scaling & Chaos Verification.
"""
from typing import Dict, Any
from app.platform_verification.performance_chaos_verification.runtime.performance_chaos_runtime import (
    PerformanceChaosVerificationRuntime,
)


class PerformanceChaosApiRouter:
    """REST API endpoint handler for performance, scaling, and chaos operations."""

    def __init__(self, runtime: PerformanceChaosVerificationRuntime):
        self.runtime = runtime

    def handle_run_pipeline(self) -> Dict[str, Any]:
        result = self.runtime.execute_full_verification()
        return {
            "status": "SUCCESS",
            "scorecard": {
                "composite_score": result["scorecard"].composite_score,
                "tier": result["scorecard"].certification_tier.value,
                "passed": result["scorecard"].passed,
            },
            "slo_status": result["slo"].status,
            "artifacts_generated": list(result["evidence"].keys()),
        }

    def handle_get_slo_report(self) -> Dict[str, Any]:
        baseline = self.runtime.baseline_engine.establish_baseline()
        load_tests = self.runtime.load_stress_gen.execute_load_tests()
        chaos = self.runtime.chaos_engine.run_chaos_experiments()
        slo = self.runtime.slo_validator.validate_slos(baseline, load_tests, chaos)
        return {
            "overall_compliance_percent": slo.overall_compliance_percent,
            "status": slo.status,
            "targets_count": len(slo.targets),
        }
