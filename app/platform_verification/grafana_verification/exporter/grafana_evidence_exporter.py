"""Grafana Evidence Exporter (3H.4.4.12).

Exports 12 deterministic JSON evidence manifests to grafana_verification/ directory.
"""

from dataclasses import asdict
from datetime import datetime, timezone
import json
import os
from typing import Dict, Any

from ..domain.models import (
    ConfigurationReport,
    ProvisioningReport,
    DashboardValidationReport,
    UsabilityAuditReport,
    PerformanceBenchmarkReport,
    SecurityAuditReport,
    OperationalDashboardScorecard,
)
from ..domain.interfaces import IGrafanaEvidenceExporter


class GrafanaEvidenceExporter(IGrafanaEvidenceExporter):
    """Exports structured SRE compliance evidence for Grafana Dashboards."""

    def __init__(self, output_dir: str = "grafana_verification"):
        self.output_dir = output_dir

    def export_all(
        self,
        config_rep: ConfigurationReport,
        prov_rep: ProvisioningReport,
        system_rep: DashboardValidationReport,
        ai_rep: DashboardValidationReport,
        agent_rep: DashboardValidationReport,
        infra_rep: DashboardValidationReport,
        incident_rep: DashboardValidationReport,
        usability_rep: UsabilityAuditReport,
        perf_rep: PerformanceBenchmarkReport,
        sec_rep: SecurityAuditReport,
        scorecard: OperationalDashboardScorecard,
    ) -> Dict[str, str]:
        os.makedirs(self.output_dir, exist_ok=True)
        exported_files: Dict[str, str] = {}

        # 1. configuration_report.json
        exported_files["configuration_report.json"] = self._write_json(
            "configuration_report.json", asdict(config_rep)
        )

        # 2. provisioning_report.json
        exported_files["provisioning_report.json"] = self._write_json(
            "provisioning_report.json", asdict(prov_rep)
        )

        # 3. system_dashboard_report.json
        exported_files["system_dashboard_report.json"] = self._write_json(
            "system_dashboard_report.json", asdict(system_rep)
        )

        # 4. ai_dashboard_report.json
        exported_files["ai_dashboard_report.json"] = self._write_json(
            "ai_dashboard_report.json", asdict(ai_rep)
        )

        # 5. agent_dashboard_report.json
        exported_files["agent_dashboard_report.json"] = self._write_json(
            "agent_dashboard_report.json", asdict(agent_rep)
        )

        # 6. infrastructure_dashboard_report.json
        exported_files["infrastructure_dashboard_report.json"] = self._write_json(
            "infrastructure_dashboard_report.json", asdict(infra_rep)
        )

        # 7. incident_dashboard_report.json
        exported_files["incident_dashboard_report.json"] = self._write_json(
            "incident_dashboard_report.json", asdict(incident_rep)
        )

        # 8. usability_report.json
        exported_files["usability_report.json"] = self._write_json(
            "usability_report.json", asdict(usability_rep)
        )

        # 9. performance_report.json
        exported_files["performance_report.json"] = self._write_json(
            "performance_report.json", asdict(perf_rep)
        )

        # 10. security_report.json
        exported_files["security_report.json"] = self._write_json(
            "security_report.json", asdict(sec_rep)
        )

        # 11. certification_report.json
        exported_files["certification_report.json"] = self._write_json(
            "certification_report.json", asdict(scorecard)
        )

        # 12. metadata.json
        metadata = {
            "verification_framework": "DocuTask Agent Grafana Dashboard Verification Framework",
            "phase": "Phase 3H.4.4",
            "overall_score": scorecard.overall_score,
            "certification_tier": scorecard.certification_tier.value,
            "passed": scorecard.passed,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "manifest_count": 12,
            "files": list(exported_files.keys()),
        }
        exported_files["metadata.json"] = self._write_json("metadata.json", metadata)

        return exported_files

    def _write_json(self, filename: str, data: Any) -> str:
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        return filepath
