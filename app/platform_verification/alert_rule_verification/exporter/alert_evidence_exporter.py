"""Alert Evidence Exporter (3H.4.5.15).

Exports 13 deterministic JSON evidence manifests to alert_verification/ directory.
"""

from dataclasses import asdict
from datetime import datetime, timezone
import json
import os
from typing import Dict, Any

from ..domain.models import (
    ArchitectureReport,
    TaxonomyReport,
    CriticalAlertReport,
    WarningAlertReport,
    ConditionTestReport,
    SeverityReport,
    MessageQualityReport,
    RoutingReport,
    FatigueReport,
    FailureTestReport,
    PerformanceReport,
    AlertQualityScorecard,
)
from ..domain.interfaces import IAlertEvidenceExporter


class AlertEvidenceExporter(IAlertEvidenceExporter):
    """Exports structured SRE compliance evidence for Alert Rule Verification."""

    def __init__(self, output_dir: str = "alert_verification"):
        self.output_dir = output_dir

    def export_all(
        self,
        arch_rep: ArchitectureReport,
        tax_rep: TaxonomyReport,
        crit_rep: CriticalAlertReport,
        warn_rep: WarningAlertReport,
        cond_rep: ConditionTestReport,
        sev_rep: SeverityReport,
        msg_rep: MessageQualityReport,
        route_rep: RoutingReport,
        fatigue_rep: FatigueReport,
        fail_rep: FailureTestReport,
        perf_rep: PerformanceReport,
        scorecard: AlertQualityScorecard,
    ) -> Dict[str, str]:
        os.makedirs(self.output_dir, exist_ok=True)
        exported_files: Dict[str, str] = {}

        # 1. architecture_report.json
        exported_files["architecture_report.json"] = self._write_json(
            "architecture_report.json", asdict(arch_rep)
        )

        # 2. taxonomy_report.json
        exported_files["taxonomy_report.json"] = self._write_json(
            "taxonomy_report.json", asdict(tax_rep)
        )

        # 3. critical_alert_report.json
        exported_files["critical_alert_report.json"] = self._write_json(
            "critical_alert_report.json", asdict(crit_rep)
        )

        # 4. warning_alert_report.json
        exported_files["warning_alert_report.json"] = self._write_json(
            "warning_alert_report.json", asdict(warn_rep)
        )

        # 5. condition_test_report.json
        exported_files["condition_test_report.json"] = self._write_json(
            "condition_test_report.json", asdict(cond_rep)
        )

        # 6. severity_report.json
        exported_files["severity_report.json"] = self._write_json(
            "severity_report.json", asdict(sev_rep)
        )

        # 7. message_quality_report.json
        exported_files["message_quality_report.json"] = self._write_json(
            "message_quality_report.json", asdict(msg_rep)
        )

        # 8. routing_report.json
        exported_files["routing_report.json"] = self._write_json(
            "routing_report.json", asdict(route_rep)
        )

        # 9. fatigue_report.json
        exported_files["fatigue_report.json"] = self._write_json(
            "fatigue_report.json", asdict(fatigue_rep)
        )

        # 10. failure_test_report.json
        exported_files["failure_test_report.json"] = self._write_json(
            "failure_test_report.json", asdict(fail_rep)
        )

        # 11. performance_report.json
        exported_files["performance_report.json"] = self._write_json(
            "performance_report.json", asdict(perf_rep)
        )

        # 12. certification_report.json
        exported_files["certification_report.json"] = self._write_json(
            "certification_report.json", asdict(scorecard)
        )

        # 13. metadata.json
        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.4.5",
            "alert_system": arch_rep.alert_system,
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
