"""
In-process REST API Router for Database Architecture Verification.
"""
from typing import Dict, Any, Optional
from app.platform_verification.database_verification.domain.models import DatabaseVerificationEvidencePackage


class DatabaseVerificationApi:
    """In-process mockable REST interface for database verification."""

    def __init__(self, runtime):
        self.runtime = runtime

    def post_scan(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """POST /architecture/database/scan"""
        package = self.runtime.run_full_verification(
            commit_sha=request_payload.get("commit_sha", "main-head"),
            target_database=request_payload.get("target_database", "PostgreSQL-16"),
        )
        return {
            "status": "COMPLETED",
            "package_id": package.package_id,
            "composite_score": package.scorecard.composite_score,
            "tier": package.scorecard.tier.value,
            "package_sha256": package.package_sha256,
        }

    def get_report(self, scan_id: str) -> Optional[Dict[str, Any]]:
        """GET /architecture/database/report/{scan_id}"""
        package = self.runtime.evidence_store.retrieve_evidence(scan_id)
        if not package:
            return None
        return {
            "package_id": package.package_id,
            "target_database": package.target_database,
            "commit_sha": package.commit_sha,
            "scorecard": {
                "schema_score": package.scorecard.schema_score,
                "transaction_score": package.scorecard.transaction_score,
                "performance_score": package.scorecard.performance_score,
                "security_isolation_score": package.scorecard.security_isolation_score,
                "migration_recovery_score": package.scorecard.migration_recovery_score,
                "composite_score": package.scorecard.composite_score,
                "tier": package.scorecard.tier.value,
            },
            "boundary_status": package.boundary_report.status,
            "schema_status": "PASS" if package.schema_report.normalization_passed else "WARN",
            "migration_status": package.migration_report.status,
            "transaction_status": package.transaction_report.status,
            "performance_status": package.performance_report.status,
            "isolation_status": package.isolation_report.status,
            "security_status": package.security_report.status,
            "recovery_status": package.recovery_report.status,
            "package_sha256": package.package_sha256,
        }

    def get_metrics(self) -> Dict[str, Any]:
        """GET /architecture/database/metrics"""
        return {
            "framework": "Part 2F - Database Architecture Verifier",
            "supported_engines": ["PostgreSQL", "SQLite"],
            "checks_enabled": [
                "schema_quality",
                "normalization_3nf",
                "orm_boundary",
                "migration_safety",
                "acid_transactions",
                "query_performance",
                "tenant_isolation",
                "security_sql_injection",
                "backup_recovery_rpo_rto",
            ],
        }
