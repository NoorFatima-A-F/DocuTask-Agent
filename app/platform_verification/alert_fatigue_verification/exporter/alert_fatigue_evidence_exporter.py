"""Alert Fatigue Evidence Exporter (3H.4.8.12).

Exports 12 deterministic JSON evidence manifests to alert_fatigue_verification/ directory.
"""

from dataclasses import asdict
from datetime import datetime, timezone
import json
import os
from typing import Dict, Any

from ..domain.models import (
    FatigueArchitectureReport,
    DeduplicationReport,
    CorrelationReport,
    SeverityOptimizationReport,
    RoutingReport,
    SuppressionReport,
    GroupingReport,
    NoiseMetricsReport,
    AlertStormReport,
    MachinePrioritizationReport,
    AlertFatigueScorecard,
)
from ..domain.interfaces import IAlertFatigueEvidenceExporter


class AlertFatigueEvidenceExporter(IAlertFatigueEvidenceExporter):
    """Exports structured SRE compliance evidence for Alert Fatigue Prevention & Signal Optimization."""

    def __init__(self, output_dir: str = "alert_fatigue_verification"):
        self.output_dir = output_dir

    def export_all(
        self,
        arch_rep: FatigueArchitectureReport,
        dedup_rep: DeduplicationReport,
        corr_rep: CorrelationReport,
        sev_rep: SeverityOptimizationReport,
        route_rep: RoutingReport,
        supp_rep: SuppressionReport,
        group_rep: GroupingReport,
        noise_rep: NoiseMetricsReport,
        storm_rep: AlertStormReport,
        ml_rep: MachinePrioritizationReport,
        scorecard: AlertFatigueScorecard,
    ) -> Dict[str, str]:
        os.makedirs(self.output_dir, exist_ok=True)
        exported_files: Dict[str, str] = {}

        # 1. architecture_report.json
        exported_files["architecture_report.json"] = self._write_json(
            "architecture_report.json", asdict(arch_rep)
        )

        # 2. deduplication_report.json
        exported_files["deduplication_report.json"] = self._write_json(
            "deduplication_report.json", asdict(dedup_rep)
        )

        # 3. correlation_report.json
        exported_files["correlation_report.json"] = self._write_json(
            "correlation_report.json", asdict(corr_rep)
        )

        # 4. severity_report.json
        exported_files["severity_report.json"] = self._write_json(
            "severity_report.json", asdict(sev_rep)
        )

        # 5. routing_report.json
        exported_files["routing_report.json"] = self._write_json(
            "routing_report.json", asdict(route_rep)
        )

        # 6. suppression_report.json
        exported_files["suppression_report.json"] = self._write_json(
            "suppression_report.json", asdict(supp_rep)
        )

        # 7. grouping_report.json
        exported_files["grouping_report.json"] = self._write_json(
            "grouping_report.json", asdict(group_rep)
        )

        # 8. noise_metrics_report.json
        exported_files["noise_metrics_report.json"] = self._write_json(
            "noise_metrics_report.json", asdict(noise_rep)
        )

        # 9. storm_test_report.json
        exported_files["storm_test_report.json"] = self._write_json(
            "storm_test_report.json", asdict(storm_rep)
        )

        # 10. intelligence_report.json
        exported_files["intelligence_report.json"] = self._write_json(
            "intelligence_report.json", asdict(ml_rep)
        )

        # 11. certification_report.json
        exported_files["certification_report.json"] = self._write_json(
            "certification_report.json", asdict(scorecard)
        )

        # 12. metadata.json
        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.4.8",
            "overall_score": scorecard.overall_score,
            "certification_tier": scorecard.certification_tier.value,
            "passed": scorecard.passed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
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
