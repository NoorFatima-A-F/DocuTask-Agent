"""AI Evidence Exporter (Part 3H.3.8.14).

Exports all 8 verification manifests to ai_health_verification/.
"""

import os
import json
import dataclasses
from enum import Enum
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from app.platform_verification.ai_provider_health.domain.models import (
    AIProviderHealthReport,
    AIAuthReport,
    AILatencyReport,
    AIQuotaReport,
    AIResponseIntegrityReport,
    AIFailureSimulationReport,
    AIFailoverReport,
    AIHealthQualityScorecard,
)


class EnhancedJSONEncoder(json.JSONEncoder):
    """JSON encoder supporting dataclasses and Enum serialization."""

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)


class AIEvidenceExporter:
    """Exports structured audit evidence reports and manifests for AI Provider Health verification."""

    DEFAULT_OUTPUT_DIR = "ai_health_verification"

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
        health_report: AIProviderHealthReport,
        auth_report: AIAuthReport,
        latency_report: AILatencyReport,
        quota_report: AIQuotaReport,
        response_quality_report: AIResponseIntegrityReport,
        failure_simulation_report: AIFailureSimulationReport,
        failover_report: AIFailoverReport,
        scorecard: Optional[AIHealthQualityScorecard] = None,
    ) -> Dict[str, str]:
        """Exports the 8 required manifests to disk."""
        exported_files = {}

        exported_files["provider_health_report.json"] = self._write_json(
            "provider_health_report.json", health_report
        )
        exported_files["authentication_report.json"] = self._write_json(
            "authentication_report.json", auth_report
        )
        exported_files["latency_report.json"] = self._write_json(
            "latency_report.json", latency_report
        )
        exported_files["quota_report.json"] = self._write_json(
            "quota_report.json", quota_report
        )
        exported_files["response_quality_report.json"] = self._write_json(
            "response_quality_report.json", response_quality_report
        )
        exported_files["failure_simulation_report.json"] = self._write_json(
            "failure_simulation_report.json", failure_simulation_report
        )
        exported_files["failover_report.json"] = self._write_json(
            "failover_report.json", failover_report
        )

        metadata = {
            "platform": "DocuTask Agent Enterprise",
            "phase": "PART 3H.3.8 - AI Provider Health Verification Framework",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "primary_provider": health_report.primary_provider,
            "primary_status": health_report.primary_status.value if isinstance(health_report.primary_status, Enum) else health_report.primary_status,
            "manifest_files_count": 8,
            "overall_status": "CERTIFIED" if (scorecard and scorecard.passed) else "COMPLETED",
            "scorecard_summary": dataclasses.asdict(scorecard) if scorecard else None,
        }

        exported_files["metadata.json"] = self._write_json(
            "metadata.json", metadata
        )

        return exported_files
