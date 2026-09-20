"""
In-process REST API Router for Observability Verification.
"""
from typing import Dict, Any, Optional


class ObservabilityVerificationApi:
    """In-process mockable REST API for observability verification."""

    def __init__(self, runtime):
        self.runtime = runtime

    def post_scan(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """POST /architecture/observability/scan"""
        package = self.runtime.run_full_verification(
            commit_sha=request_payload.get("commit_sha", "main-head"),
        )
        return {
            "status": "COMPLETED",
            "package_id": package.package_id,
            "composite_score": package.scorecard.composite_score,
            "tier": package.scorecard.tier.value,
            "package_sha256": package.package_sha256,
        }

    def get_report(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """GET /architecture/observability/report/{scan_id}"""
        package = self.runtime.evidence_store.retrieve_evidence(scan_id)
        if not package:
            return None
        return {
            "package_id": package.package_id,
            "commit_sha": package.commit_sha,
            "scorecard": {
                "logging_quality_score": package.scorecard.logging_quality_score,
                "metrics_coverage_score": package.scorecard.metrics_coverage_score,
                "distributed_tracing_score": package.scorecard.distributed_tracing_score,
                "alerting_score": package.scorecard.alerting_score,
                "slo_management_score": package.scorecard.slo_management_score,
                "incident_response_score": package.scorecard.incident_response_score,
                "composite_score": package.scorecard.composite_score,
                "tier": package.scorecard.tier.value,
            },
            "architecture_status": package.architecture_report.status,
            "logging_status": package.logging_report.status,
            "tracing_status": package.tracing_report.status,
            "slo_status": package.slo_report.status,
            "package_sha256": package.package_sha256,
        }

    def get_metrics(self) -> Dict[str, Any]:
        """GET /architecture/observability/metrics"""
        return {
            "framework": "Part 3E - Enterprise Observability & Reliability Verifier",
            "pillars_evaluated": [
                "logging_quality_pii_security",
                "golden_signals_and_ai_metrics",
                "opentelemetry_distributed_tracing",
                "ai_workflow_telemetry",
                "actionable_alerting",
                "slo_error_budgets",
                "incident_mttd_mttr_chaos",
            ],
        }
