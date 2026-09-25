"""
In-process REST API Router for Service Communication Verification.
"""
from typing import Dict, Any, Optional


class ServiceCommunicationApi:
    """In-process mockable REST API for service communication platform."""

    def __init__(self, runtime):
        self.runtime = runtime

    def post_scan(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """POST /architecture/communication/scan"""
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
        """GET /architecture/communication/report/{scan_id}"""
        package = self.runtime.evidence_store.retrieve_evidence(scan_id)
        if not package:
            return None
        return {
            "package_id": package.package_id,
            "commit_sha": package.commit_sha,
            "scorecard": {
                "communication_reliability_score": package.scorecard.communication_reliability_score,
                "failure_handling_score": package.scorecard.failure_handling_score,
                "consistency_score": package.scorecard.consistency_score,
                "scalability_score": package.scorecard.scalability_score,
                "observability_score": package.scorecard.observability_score,
                "composite_score": package.scorecard.composite_score,
                "tier": package.scorecard.tier.value,
            },
            "dependency_status": package.dependency_graph.status,
            "contract_status": package.contract_report.status,
            "circuit_breaker_status": package.circuit_breaker_report.status,
            "consistency_status": package.consistency_report.status,
            "traceability_status": package.traceability_report.status,
            "package_sha256": package.package_sha256,
        }

    def get_metrics(self) -> Dict[str, Any]:
        """GET /architecture/communication/metrics"""
        return {
            "framework": "Part 3B - Service Communication & Distributed System Verifier",
            "supported_protocols": ["HTTP_REST", "GRPC", "REDIS_QUEUE", "SQL_CONNECTION", "S3_STORAGE"],
            "checks_enabled": [
                "dependency_graph_cycle_detection",
                "communication_contracts",
                "timeout_exponential_backoff",
                "circuit_breaker_state_machine",
                "network_chaos_simulation",
                "distributed_idempotency_consistency",
                "end_to_end_traceability",
            ],
        }
