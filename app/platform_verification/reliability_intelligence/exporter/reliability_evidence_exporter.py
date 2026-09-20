"""Reliability Evidence Exporter.

Part 3H.3.7M: Comprehensive SRE Evidence Artifact Generator.
Exports all 11 JSON verification manifests to reliability_intelligence_verification/.
"""

import os
import json
import dataclasses
from enum import Enum
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from app.platform_verification.reliability_intelligence.domain.models import (
    ReliabilityModelReport,
    SLOVerificationReport,
    ErrorBudgetReport,
    FailurePatternReport,
    RootCauseReport,
    ReliabilityRiskReport,
    CapacityIntelligenceReport,
    ChangeImpactReport,
    ReliabilityRecommendationReport,
    ContinuousImprovementReport,
    ReliabilitySecurityReport,
    ReliabilityMaturityScorecard,
)


class EnhancedJSONEncoder(json.JSONEncoder):
    """JSON encoder supporting dataclasses and Enum serialization."""

    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)


class ReliabilityEvidenceExporter:
    """Exports structured audit evidence reports and manifests for reliability intelligence verification."""

    DEFAULT_OUTPUT_DIR = "reliability_intelligence_verification"

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
        model_report: ReliabilityModelReport,
        slo_report: SLOVerificationReport,
        error_budget_report: ErrorBudgetReport,
        failure_pattern_report: FailurePatternReport,
        root_cause_report: RootCauseReport,
        risk_score_report: ReliabilityRiskReport,
        capacity_report: CapacityIntelligenceReport,
        change_impact_report: ChangeImpactReport,
        recommendation_report: ReliabilityRecommendationReport,
        improvement_report: ContinuousImprovementReport,
        security_report: Optional[ReliabilitySecurityReport] = None,
        scorecard: Optional[ReliabilityMaturityScorecard] = None,
    ) -> Dict[str, str]:
        """Exports all 11 audit manifests and metadata to output directory."""
        exported_files = {}

        exported_files["reliability_model_report.json"] = self._write_json(
            "reliability_model_report.json", model_report
        )
        exported_files["slo_report.json"] = self._write_json(
            "slo_report.json", slo_report
        )
        exported_files["error_budget_report.json"] = self._write_json(
            "error_budget_report.json", error_budget_report
        )
        exported_files["failure_pattern_report.json"] = self._write_json(
            "failure_pattern_report.json", failure_pattern_report
        )
        exported_files["root_cause_report.json"] = self._write_json(
            "root_cause_report.json", root_cause_report
        )
        exported_files["risk_score_report.json"] = self._write_json(
            "risk_score_report.json", risk_score_report
        )
        exported_files["capacity_report.json"] = self._write_json(
            "capacity_report.json", capacity_report
        )
        exported_files["change_impact_report.json"] = self._write_json(
            "change_impact_report.json", change_impact_report
        )
        exported_files["recommendation_report.json"] = self._write_json(
            "recommendation_report.json", recommendation_report
        )
        exported_files["improvement_report.json"] = self._write_json(
            "improvement_report.json", improvement_report
        )

        metadata = {
            "platform": "DocuTask Agent Enterprise",
            "phase": "PART 3H.3.7 - Reliability Engineering Intelligence & Continuous Improvement",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "target_slos": {
                "api_gateway": "99.5%",
                "document_pipeline": "99.0%",
                "agent_runtime": "98.0%",
                "ai_gateway": "99.0%",
            },
            "manifest_files_count": 11,
            "overall_status": "VERIFIED_MATURE" if (scorecard and scorecard.passed) else "COMPLETED",
            "scorecard_summary": dataclasses.asdict(scorecard) if scorecard else None,
            "security_summary": dataclasses.asdict(security_report) if security_report else None,
        }

        exported_files["metadata.json"] = self._write_json(
            "metadata.json", metadata
        )

        return exported_files
