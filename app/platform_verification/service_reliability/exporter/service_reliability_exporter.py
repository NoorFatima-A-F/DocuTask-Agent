"""
Phase 3H.6: Service Level Objectives & Reliability Evidence Exporter
"""
import os
import json
import hashlib
from typing import Dict, Any
from datetime import datetime, timezone

from ..domain.models import (
    SLOArchitectureReport,
    SLICollectionReport,
    AvailabilitySLOReport,
    LatencySLOReport,
    ErrorBudgetReport,
    BurnRateReport,
    ReliabilityComplianceReport,
    DeploymentGateReport,
    ReliabilityDashboardReport,
    HistoricalReliabilityReport,
    AIReliabilityReport,
    ServiceReliabilityScorecard,
)


class ServiceReliabilityExporter:
    """
    Exports all 12 service reliability reports and metadata.json
    with SHA-256 cryptographic signatures into service_reliability_verification/.
    """

    def __init__(self, output_dir: str = "service_reliability_verification"):
        self.output_dir = output_dir

    def _compute_sha256(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def export_all(
        self,
        slo_report: SLOArchitectureReport,
        sli_report: SLICollectionReport,
        availability_report: AvailabilitySLOReport,
        latency_report: LatencySLOReport,
        error_budget_report: ErrorBudgetReport,
        burn_rate_report: BurnRateReport,
        compliance_report: ReliabilityComplianceReport,
        gate_report: DeploymentGateReport,
        dashboard_report: ReliabilityDashboardReport,
        historical_report: HistoricalReliabilityReport,
        ai_report: AIReliabilityReport,
        scorecard: ServiceReliabilityScorecard,
    ) -> Dict[str, str]:
        os.makedirs(self.output_dir, exist_ok=True)

        artifacts = {
            "slo_architecture_report.json": slo_report.model_dump(),
            "sli_collection_report.json": sli_report.model_dump(),
            "availability_slo_report.json": availability_report.model_dump(),
            "latency_slo_report.json": latency_report.model_dump(),
            "error_budget_report.json": error_budget_report.model_dump(),
            "burn_rate_report.json": burn_rate_report.model_dump(),
            "reliability_compliance_report.json": compliance_report.model_dump(),
            "deployment_gate_report.json": gate_report.model_dump(),
            "dashboard_report.json": dashboard_report.model_dump(),
            "historical_reliability_report.json": historical_report.model_dump(),
            "ai_reliability_report.json": ai_report.model_dump(),
            "certification_report.json": scorecard.model_dump(),
        }

        generated_files = {}
        for filename, data in artifacts.items():
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            generated_files[filename] = filepath

        # Calculate checksums for metadata.json
        checksums = {}
        for filename, filepath in generated_files.items():
            checksums[filename] = self._compute_sha256(filepath)

        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.6 — Enterprise Service Level Objectives (SLO), SLI, Error Budget & Reliability Compliance",
            "environment": "production-reliability-verification",
            "commit": "master-latest",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "reliability_framework_version": "1.0.0",
            "verification_id": scorecard.verification_id,
            "overall_score": scorecard.overall_reliability_score,
            "certification_tier": scorecard.certification_tier.value,
            "passed": scorecard.passed,
            "measured_availability_pct": scorecard.overall_availability_pct,
            "remaining_error_budget_pct": scorecard.overall_error_budget_remaining_pct,
            "deployment_decision": scorecard.deployment_gate_decision.value,
            "file_manifest": checksums,
        }

        metadata_path = os.path.join(self.output_dir, "metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        generated_files["metadata.json"] = metadata_path
        return generated_files
