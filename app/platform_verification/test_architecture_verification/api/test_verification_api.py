"""
In-process REST API Router for Test Architecture Verification.
"""
from typing import Dict, Any, Optional


class TestVerificationApi:
    """In-process mockable REST API for test verification platform."""
    __test__ = False

    def __init__(self, runtime):
        self.runtime = runtime

    def post_scan(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """POST /architecture/tests/scan"""
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
        """GET /architecture/tests/report/{scan_id}"""
        package = self.runtime.evidence_store.retrieve_evidence(scan_id)
        if not package:
            return None
        return {
            "package_id": package.package_id,
            "commit_sha": package.commit_sha,
            "scorecard": {
                "coverage_quality_score": package.scorecard.coverage_quality_score,
                "reliability_score": package.scorecard.reliability_score,
                "organization_pyramid_score": package.scorecard.organization_pyramid_score,
                "ai_evaluation_score": package.scorecard.ai_evaluation_score,
                "reproducibility_score": package.scorecard.reproducibility_score,
                "composite_score": package.scorecard.composite_score,
                "tier": package.scorecard.tier.value,
            },
            "pyramid_status": package.pyramid_report.status,
            "ai_eval_status": package.ai_evaluation_report.status,
            "flakiness_status": package.flakiness_report.status,
            "environment_status": package.environment_report.status,
            "package_sha256": package.package_sha256,
        }

    def get_metrics(self) -> Dict[str, Any]:
        """GET /architecture/tests/metrics"""
        return {
            "framework": "Part 2G - Enterprise Test Architecture Verifier",
            "supported_layers": ["unit", "component", "integration", "api", "e2e", "performance", "security", "ai_evaluation", "regression"],
            "checks_enabled": [
                "test_pyramid_distribution",
                "unit_mock_isolation",
                "line_branch_mutation_coverage",
                "ai_prompt_regression_eval",
                "flakiness_order_independence",
                "environment_reproducibility",
            ],
        }
