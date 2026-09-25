"""Incident Evidence Exporter (Part 3H.3.6L).

Exports all 10 required audit JSON manifests to incident_response_verification/ directory.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from app.platform_verification.incident_response_automation.domain.models import (
    CICDPipelineReport,
    IncidentArchitectureReport,
    IncidentAutomationTier,
    IncidentClassificationReport,
    IncidentCorrelationReport,
    IncidentDetectionReport,
    IncidentKnowledgeReport,
    IncidentQualityScorecard,
    IncidentSecurityReport,
    PostmortemReport,
    RecoveryPolicyReport,
    RunbookExecutionReport,
    SelfHealingReport,
)


class IncidentEvidenceExporter:
    """Exports structured audit manifests for Phase 3H.3.6."""

    def __init__(self, output_dir: Optional[Path | str] = None) -> None:
        self.output_dir = Path(output_dir or "incident_response_verification")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_all(
        self,
        arch_report: IncidentArchitectureReport,
        detect_report: IncidentDetectionReport,
        class_report: IncidentClassificationReport,
        runbook_report: RunbookExecutionReport,
        healing_report: SelfHealingReport,
        policy_report: RecoveryPolicyReport,
        correlation_report: IncidentCorrelationReport,
        knowledge_report: IncidentKnowledgeReport,
        postmortem_report: PostmortemReport,
        security_report: IncidentSecurityReport,
        cicd_report: CICDPipelineReport,
        scorecard: IncidentQualityScorecard,
        additional_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Path]:
        """Persists all 10 manifests to disk."""
        exported: Dict[str, Path] = {}

        # 1. architecture_report.json
        arch_path = self.output_dir / "architecture_report.json"
        with open(arch_path, "w", encoding="utf-8") as f:
            json.dump(asdict(arch_report), f, indent=2, default=str)
        exported["architecture_report"] = arch_path

        # 2. detection_report.json
        det_path = self.output_dir / "detection_report.json"
        with open(det_path, "w", encoding="utf-8") as f:
            json.dump(asdict(detect_report), f, indent=2, default=str)
        exported["detection_report"] = det_path

        # 3. classification_report.json
        class_path = self.output_dir / "classification_report.json"
        with open(class_path, "w", encoding="utf-8") as f:
            json.dump(asdict(class_report), f, indent=2, default=str)
        exported["classification_report"] = class_path

        # 4. runbook_report.json
        rb_path = self.output_dir / "runbook_report.json"
        with open(rb_path, "w", encoding="utf-8") as f:
            json.dump(asdict(runbook_report), f, indent=2, default=str)
        exported["runbook_report"] = rb_path

        # 5. self_healing_report.json
        heal_path = self.output_dir / "self_healing_report.json"
        with open(heal_path, "w", encoding="utf-8") as f:
            json.dump(asdict(healing_report), f, indent=2, default=str)
        exported["self_healing_report"] = heal_path

        # 6. recovery_policy_report.json
        pol_path = self.output_dir / "recovery_policy_report.json"
        with open(pol_path, "w", encoding="utf-8") as f:
            json.dump(asdict(policy_report), f, indent=2, default=str)
        exported["recovery_policy_report"] = pol_path

        # 7. correlation_report.json
        corr_path = self.output_dir / "correlation_report.json"
        with open(corr_path, "w", encoding="utf-8") as f:
            json.dump(asdict(correlation_report), f, indent=2, default=str)
        exported["correlation_report"] = corr_path

        # 8. postmortem_report.json
        pm_path = self.output_dir / "postmortem_report.json"
        with open(pm_path, "w", encoding="utf-8") as f:
            json.dump(asdict(postmortem_report), f, indent=2, default=str)
        exported["postmortem_report"] = pm_path

        # 9. security_report.json
        sec_path = self.output_dir / "security_report.json"
        with open(sec_path, "w", encoding="utf-8") as f:
            json.dump(asdict(security_report), f, indent=2, default=str)
        exported["security_report"] = sec_path

        # 10. metadata.json
        meta_path = self.output_dir / "metadata.json"
        meta_payload = {
            "system": "DocuTask Agent",
            "phase": "3H.3.6",
            "framework": "Enterprise Incident Response Automation & Self-Healing Verification Framework",
            "status": scorecard.certification_verdict,
            "overall_score": scorecard.overall_score,
            "tier": scorecard.certification_tier.value if isinstance(scorecard.certification_tier, IncidentAutomationTier) else str(scorecard.certification_tier),
            "passed": scorecard.passed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": "production-simulation",
            "dimension_scores": {
                "detection_accuracy": scorecard.detection_accuracy_score,
                "recovery_automation": scorecard.recovery_automation_score,
                "safety_controls": scorecard.safety_controls_score,
                "incident_diagnosis": scorecard.incident_diagnosis_score,
                "operational_learning": scorecard.operational_learning_score,
                "security": scorecard.security_score,
            },
            "manifest_files": [
                "architecture_report.json",
                "detection_report.json",
                "classification_report.json",
                "runbook_report.json",
                "self_healing_report.json",
                "recovery_policy_report.json",
                "correlation_report.json",
                "postmortem_report.json",
                "security_report.json",
                "metadata.json",
            ],
            "custom_metadata": additional_metadata or {},
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_payload, f, indent=2, default=str)
        exported["metadata"] = meta_path

        return exported
