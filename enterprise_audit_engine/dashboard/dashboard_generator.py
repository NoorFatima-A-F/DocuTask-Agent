"""Enterprise Audit & Meta-Assurance Dashboard Generator."""

import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class DashboardSummary(BaseModel):
    """Top-level executive summary metrics."""
    target_release: str
    engine_version: str
    overall_certification_status: str  # CERTIFIED, CONDITIONALLY_CERTIFIED, REJECTED
    trust_assurance_score: float
    compliance_score: float
    mutation_defense_rate: float
    transparency_log_verified: bool
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AuditDashboard(BaseModel):
    """Consolidated enterprise assurance and audit dashboard."""
    summary: DashboardSummary
    integrity_verification: Dict[str, Any]
    baseline_comparison: Dict[str, Any]
    mutation_testing_results: Dict[str, Any]
    transparency_ledger: Dict[str, Any]
    compliance_mappings: Dict[str, Any]
    reproducibility_evidence: Dict[str, Any]


class DashboardGenerator:
    """Generates comprehensive JSON and interactive HTML dashboards for auditors and release gates."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_dashboard(
        self,
        target_release: str,
        engine_version: str,
        integrity_data: Dict[str, Any],
        baseline_data: Dict[str, Any],
        mutation_data: Dict[str, Any],
        transparency_data: Dict[str, Any],
        compliance_data: Dict[str, Any],
        reproducibility_data: Dict[str, Any],
        output_filename: str = "audit_dashboard.json",
    ) -> AuditDashboard:
        """Constructs and persists the full audit dashboard."""
        
        mutation_blocked = mutation_data.get("mutations_blocked_count", 0)
        mutation_total = mutation_data.get("total_mutations_executed", 0)
        mutation_rate = (mutation_blocked / mutation_total * 100.0) if mutation_total > 0 else 100.0

        comp_score = compliance_data.get("overall_compliance_score", 100.0)
        is_integrity_valid = integrity_data.get("is_valid", True)
        is_transparency_valid = transparency_data.get("is_valid", True)

        # Determine overall certification status
        if is_integrity_valid and is_transparency_valid and mutation_rate >= 100.0 and comp_score >= 80.0:
            cert_status = "CERTIFIED"
            trust_score = 100.0
        elif is_integrity_valid and mutation_rate >= 90.0:
            cert_status = "CONDITIONALLY_CERTIFIED"
            trust_score = 85.0
        else:
            cert_status = "REJECTED"
            trust_score = 40.0

        summary = DashboardSummary(
            target_release=target_release,
            engine_version=engine_version,
            overall_certification_status=cert_status,
            trust_assurance_score=trust_score,
            compliance_score=comp_score,
            mutation_defense_rate=mutation_rate,
            transparency_log_verified=is_transparency_valid,
        )

        dashboard = AuditDashboard(
            summary=summary,
            integrity_verification=integrity_data,
            baseline_comparison=baseline_data,
            mutation_testing_results=mutation_data,
            transparency_ledger=transparency_data,
            compliance_mappings=compliance_data,
            reproducibility_evidence=reproducibility_data,
        )

        json_path = self.output_dir / output_filename
        with open(json_path, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(dashboard.model_dump(), indent=2, sort_keys=True))

        return dashboard
