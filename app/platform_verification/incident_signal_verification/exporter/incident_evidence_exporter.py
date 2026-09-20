"""Incident Evidence Exporter (3H.4.7.13).

Exports 13 deterministic JSON evidence manifests to incident_signal_verification/ directory.
"""

from dataclasses import asdict
from datetime import datetime, timezone
import json
import os
from typing import Dict, Any

from ..domain.models import (
    IncidentArchitectureReport,
    AlertMappingReport,
    PayloadQualityReport,
    DependencyAnalysisReport,
    ImpactReport,
    PriorityReport,
    IncidentCorrelationReport,
    TimelineReport,
    RunbookReport,
    IncidentSecurityReport,
    IncidentAutomationReport,
    IncidentQualityScorecard,
)
from ..domain.interfaces import IIncidentEvidenceExporter


class IncidentEvidenceExporter(IIncidentEvidenceExporter):
    """Exports structured SRE compliance evidence for Incident Signal Verification."""

    def __init__(self, output_dir: str = "incident_signal_verification"):
        self.output_dir = output_dir

    def export_all(
        self,
        arch_rep: IncidentArchitectureReport,
        map_rep: AlertMappingReport,
        payload_rep: PayloadQualityReport,
        dep_rep: DependencyAnalysisReport,
        impact_rep: ImpactReport,
        prio_rep: PriorityReport,
        corr_rep: IncidentCorrelationReport,
        time_rep: TimelineReport,
        runbook_rep: RunbookReport,
        sec_rep: IncidentSecurityReport,
        auto_rep: IncidentAutomationReport,
        scorecard: IncidentQualityScorecard,
    ) -> Dict[str, str]:
        os.makedirs(self.output_dir, exist_ok=True)
        exported_files: Dict[str, str] = {}

        # 1. incident_architecture_report.json
        exported_files["incident_architecture_report.json"] = self._write_json(
            "incident_architecture_report.json", asdict(arch_rep)
        )

        # 2. alert_mapping_report.json
        exported_files["alert_mapping_report.json"] = self._write_json(
            "alert_mapping_report.json", asdict(map_rep)
        )

        # 3. payload_quality_report.json
        exported_files["payload_quality_report.json"] = self._write_json(
            "payload_quality_report.json", asdict(payload_rep)
        )

        # 4. dependency_analysis_report.json
        exported_files["dependency_analysis_report.json"] = self._write_json(
            "dependency_analysis_report.json", asdict(dep_rep)
        )

        # 5. impact_report.json
        exported_files["impact_report.json"] = self._write_json(
            "impact_report.json", asdict(impact_rep)
        )

        # 6. priority_report.json
        exported_files["priority_report.json"] = self._write_json(
            "priority_report.json", asdict(prio_rep)
        )

        # 7. correlation_report.json
        exported_files["correlation_report.json"] = self._write_json(
            "correlation_report.json", asdict(corr_rep)
        )

        # 8. timeline_report.json
        exported_files["timeline_report.json"] = self._write_json(
            "timeline_report.json", asdict(time_rep)
        )

        # 9. runbook_report.json
        exported_files["runbook_report.json"] = self._write_json(
            "runbook_report.json", asdict(runbook_rep)
        )

        # 10. security_report.json
        exported_files["security_report.json"] = self._write_json(
            "security_report.json", asdict(sec_rep)
        )

        # 11. automation_report.json
        exported_files["automation_report.json"] = self._write_json(
            "automation_report.json", asdict(auto_rep)
        )

        # 12. certification_report.json
        exported_files["certification_report.json"] = self._write_json(
            "certification_report.json", asdict(scorecard)
        )

        # 13. metadata.json
        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.4.7",
            "overall_score": scorecard.overall_score,
            "certification_tier": scorecard.certification_tier.value,
            "passed": scorecard.passed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "manifest_count": 13,
            "files": list(exported_files.keys()),
        }
        exported_files["metadata.json"] = self._write_json("metadata.json", metadata)

        return exported_files

    def _write_json(self, filename: str, data: Any) -> str:
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        return filepath
