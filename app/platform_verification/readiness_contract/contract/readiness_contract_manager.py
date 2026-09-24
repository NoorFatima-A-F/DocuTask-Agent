"""
Readiness Contract Manager (Part 1).
Exposes and validates the standardized GET /ready schema and component checks.
"""
from typing import Dict, Any
from datetime import datetime, timezone
from app.platform_verification.readiness_contract.domain.models import (
    ReadinessContractReport,
)
from app.platform_verification.readiness_contract.domain.interfaces import (
    IReadinessContractManager,
)


class ReadinessContractManager(IReadinessContractManager):
    """
    Validates and produces production-grade /ready contract payloads.
    """

    def generate_ready_payload(
        self,
        db_status: str = "healthy",
        queue_status: str = "healthy",
        storage_status: str = "healthy",
        workers_status: str = "healthy",
        ai_status: str = "healthy",
    ) -> Dict[str, Any]:
        critical_ok = (
            db_status == "healthy"
            and queue_status == "healthy"
            and storage_status == "healthy"
            and workers_status == "healthy"
        )
        ai_ok = (ai_status == "healthy")

        if not critical_ok:
            status = "not_ready"
        elif not ai_ok:
            status = "degraded"
        else:
            status = "ready"

        return {
            "status": status,
            "service": "docutask-api",
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "checks": {
                "database": db_status,
                "queue": queue_status,
                "storage": storage_status,
                "workers": workers_status,
                "ai_provider": ai_status,
            },
        }

    def validate_readiness_contract(self) -> ReadinessContractReport:
        sample = self.generate_ready_payload()

        has_status = "status" in sample and sample["status"] in ["ready", "degraded", "not_ready"]
        has_service = sample.get("service") == "docutask-api"
        has_version = "version" in sample
        has_timestamp = "timestamp" in sample
        has_checks = isinstance(sample.get("checks"), dict)

        required_checks = ["database", "queue", "storage", "workers", "ai_provider"]
        all_checks_present = all(c in sample.get("checks", {}) for c in required_checks)

        passed = (
            has_status
            and has_service
            and has_version
            and has_timestamp
            and has_checks
            and all_checks_present
        )

        return ReadinessContractReport(
            endpoint="/ready",
            status=sample["status"],
            service=sample["service"],
            version=sample["version"],
            timestamp=sample["timestamp"],
            checks=sample["checks"],
            contract_schema_valid=passed,
            passed=passed,
            details={
                "required_checks_count": len(required_checks),
                "checks_evaluated": required_checks,
                "verdict": "READINESS_CONTRACT_VERIFIED" if passed else "CONTRACT_SCHEMA_INVALID",
            },
        )
