"""AI Monitoring Evidence Exporter (Part 3H.3.9.11).

Exports all 9 verification manifests to ai_monitoring_verification/.
"""

import os
import json
import dataclasses
from enum import Enum
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.platform_verification.ai_health_monitoring.domain.models import (
    AIObservabilityArchitectureReport,
    AIMetricsReport,
    AIDashboardReport,
    AILoggingReport,
    AITracingReport,
    AIAlertingReport,
    AISLOReport,
    AIIncidentTestReport,
    AIObservabilityScorecard,
)


class EnhancedJSONEncoder(json.JSONEncoder):
    """JSON encoder supporting dataclasses and Enum serialization."""

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)


class AIMonitoringEvidenceExporter:
    """Exports structured audit evidence reports and manifests for AI Health Monitoring verification."""

    DEFAULT_OUTPUT_DIR = "ai_monitoring_verification"

    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = output_dir or self.DEFAULT_OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def _write_json(self, filename: str, data: Any) -> str:
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, cls=EnhancedJSONEncoder)
        return filepath

    def export_all(
        self,
        arch_report: AIObservabilityArchitectureReport,
        metrics_report: AIMetricsReport,
        dashboard_report: AIDashboardReport,
        logging_report: AILoggingReport,
        tracing_report: AITracingReport,
        alerting_report: AIAlertingReport,
        slo_report: AISLOReport,
        incident_report: AIIncidentTestReport,
        scorecard: Optional[AIObservabilityScorecard] = None,
    ) -> Dict[str, str]:
        """Exports the 9 required manifests to disk."""
        exported_files = {}

        exported_files["telemetry_report.json"] = self._write_json(
            "telemetry_report.json", arch_report
        )
        exported_files["metrics_report.json"] = self._write_json(
            "metrics_report.json", metrics_report
        )
        exported_files["dashboard_report.json"] = self._write_json(
            "dashboard_report.json", dashboard_report
        )
        exported_files["logging_report.json"] = self._write_json(
            "logging_report.json", logging_report
        )
        exported_files["tracing_report.json"] = self._write_json(
            "tracing_report.json", tracing_report
        )
        exported_files["alerting_report.json"] = self._write_json(
            "alerting_report.json", alerting_report
        )
        exported_files["slo_report.json"] = self._write_json(
            "slo_report.json", slo_report
        )
        exported_files["incident_test_report.json"] = self._write_json(
            "incident_test_report.json", incident_report
        )

        metadata = {
            "platform": "DocuTask Agent Enterprise",
            "phase": "PART 3H.3.9 - AI Health Monitoring Integration Verification Framework",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "manifest_files_count": 9,
            "overall_status": "CERTIFIED" if (scorecard and scorecard.passed) else "COMPLETED",
            "scorecard_summary": dataclasses.asdict(scorecard) if scorecard else None,
        }

        exported_files["metadata.json"] = self._write_json(
            "metadata.json", metadata
        )

        return exported_files
