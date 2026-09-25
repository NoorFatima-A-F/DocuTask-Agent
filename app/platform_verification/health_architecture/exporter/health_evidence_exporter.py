"""
Health Evidence Exporter for Health Check Architecture Verification (Part 3H.1).
"""
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any
from dataclasses import asdict
from app.platform_verification.health_architecture.domain.models import (
    HealthStateModelReport,
    HealthContractReport,
    DependencyGraphReport,
    FailurePolicyReport,
    SecurityAuditReport,
    AutomationIntegrationReport,
    HealthScorecard,
)


class HealthEvidenceExporter:
    """
    Exports structured JSON evidence artifacts for the Health Check Architecture Verification
    into the designated target directory (default: health_architecture_verification/).
    """

    def __init__(self, output_dir: str = "health_architecture_verification"):
        self.output_dir = output_dir

    def _ensure_dir(self):
        os.makedirs(self.output_dir, exist_ok=True)

    def _write_json(self, filename: str, data: Dict[str, Any]) -> str:
        self._ensure_dir()
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        return file_path

    def export_all(
        self,
        model_report: HealthStateModelReport,
        contract_report: HealthContractReport,
        deps_report: DependencyGraphReport,
        policy_report: FailurePolicyReport,
        security_report: SecurityAuditReport,
        auto_report: AutomationIntegrationReport,
        scorecard: HealthScorecard,
    ) -> Dict[str, str]:
        exported_files = {}

        # 1. state_model_report.json
        exported_files["state_model_report.json"] = self._write_json(
            "state_model_report.json",
            asdict(model_report),
        )

        # 2. contract_report.json
        exported_files["contract_report.json"] = self._write_json(
            "contract_report.json",
            asdict(contract_report),
        )

        # 3. dependency_graph_report.json
        exported_files["dependency_graph_report.json"] = self._write_json(
            "dependency_graph_report.json",
            asdict(deps_report),
        )

        # 4. failure_policy_report.json
        exported_files["failure_policy_report.json"] = self._write_json(
            "failure_policy_report.json",
            asdict(policy_report),
        )

        # 5. security_report.json
        exported_files["security_report.json"] = self._write_json(
            "security_report.json",
            asdict(security_report),
        )

        # 6. automation_report.json
        exported_files["automation_report.json"] = self._write_json(
            "automation_report.json",
            asdict(auto_report),
        )

        # 7. certification.json
        exported_files["certification.json"] = self._write_json(
            "certification.json",
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "phase": "PART 3H.1 — Enterprise Health Check Architecture Design Verification",
                "scorecard": asdict(scorecard),
                "certified": scorecard.ci_cd_deployment_approved,
                "tier": scorecard.certification_tier.value,
                "verdict": scorecard.certification_verdict,
            },
        )

        # 8. metadata.json
        exported_files["metadata.json"] = self._write_json(
            "metadata.json",
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "platform": "DocuTask Agent",
                "framework": "Health Check Architecture Verification (Part 3H.1)",
                "total_artifacts": 8,
                "artifacts": list(exported_files.keys()),
                "passed": scorecard.passed,
                "score": scorecard.overall_health_score,
            },
        )

        return exported_files
