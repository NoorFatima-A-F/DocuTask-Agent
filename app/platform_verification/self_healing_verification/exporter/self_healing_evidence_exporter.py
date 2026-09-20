"""
Phase 3H.5.5: Self-Healing Evidence Exporter
"""
import os
import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from ..domain.interfaces import ISelfHealingEvidenceExporter
from ..domain.models import RecoveryValidationReport, SelfHealingScorecard


class SelfHealingEvidenceExporter(ISelfHealingEvidenceExporter):
    def export_evidence_manifests(
        self,
        output_dir: str,
        validation_report: RecoveryValidationReport,
        scorecard: SelfHealingScorecard,
    ) -> List[str]:
        safe_dir = os.path.abspath(output_dir)
        os.makedirs(safe_dir, exist_ok=True)
        files_written = []

        now_str = datetime.now(timezone.utc).isoformat()

        manifests: Dict[str, Any] = {
            "recovery_validation_report.json": validation_report.model_dump(),
            "health_recovery_report.json": validation_report.layer1_health.model_dump(),
            "dependency_restore_report.json": validation_report.layer2_dependency.model_dump(),
            "workflow_validation_report.json": validation_report.layer3_workflow.model_dump(),
            "performance_recovery_report.json": validation_report.layer4_performance.model_dump(),
            "stability_window_report.json": validation_report.layer5_stability.model_dump(),
            "certification_report.json": scorecard.model_dump(),
            "metadata.json": {
                "project": "DocuTask-Agent",
                "phase": "3H.5.5",
                "title": "Enterprise Health Self-Healing & Automated Recovery Verification Framework",
                "timestamp": now_str,
                "composite_score": scorecard.composite_score,
                "tier": scorecard.tier.value,
                "certified_autonomous_recovery_ready": scorecard.certified_enterprise_ready,
            },
        }

        for fname, data in manifests.items():
            clean_name = os.path.basename(fname)
            path = os.path.abspath(os.path.join(safe_dir, clean_name))
            if not path.startswith(safe_dir):
                raise ValueError(f"Path traversal detected: {fname}")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            files_written.append(path)

        return files_written
