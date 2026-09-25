"""
Phase 3H.5.5: Self-Healing Evidence Exporter
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
from app.core.security import resolve_safe_path, validate_safe_filename_segment
from ..domain.interfaces import ISelfHealingEvidenceExporter
from ..domain.models import RecoveryValidationReport, SelfHealingScorecard


class SelfHealingEvidenceExporter(ISelfHealingEvidenceExporter):
    def export_evidence_manifests(
        self,
        output_dir: str,
        validation_report: RecoveryValidationReport,
        scorecard: SelfHealingScorecard,
    ) -> List[str]:
        safe_dir = Path(output_dir) if output_dir else Path.cwd() / "self_healing_verification"
        safe_dir.mkdir(parents=True, exist_ok=True)
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
            clean_name = validate_safe_filename_segment(fname)
            path = resolve_safe_path(safe_dir, clean_name)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            files_written.append(str(path))

        return files_written
