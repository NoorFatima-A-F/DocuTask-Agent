"""
Phase 3H.5: Evidence Exporter for Enterprise Health Intelligence
"""
import os
import json
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any
from ..domain.models import (
    HealthEventArchitectureReport,
    FailureClassificationReport,
    EventCorrelationReport,
    RCAReport,
    RemediationDecisionReport,
    RecoveryExecutionReport,
    SelfHealingValidationReport,
    ChaosHealthReport,
    HealthIntelligenceScorecard,
)


class HealthIntelligenceExporter:
    def export_evidence_manifests(
        self,
        output_dir: str,
        event_report: HealthEventArchitectureReport,
        class_report: FailureClassificationReport,
        corr_report: EventCorrelationReport,
        rca_report: RCAReport,
        remed_report: RemediationDecisionReport,
        recov_report: RecoveryExecutionReport,
        self_heal_report: SelfHealingValidationReport,
        chaos_report: ChaosHealthReport,
        scorecard: HealthIntelligenceScorecard,
    ) -> List[str]:
        os.makedirs(output_dir, exist_ok=True)
        exported_files: List[str] = []

        manifest_map: Dict[str, Any] = {
            "event_architecture_report.json": event_report.model_dump(),
            "failure_classification_report.json": class_report.model_dump(),
            "correlation_report.json": corr_report.model_dump(),
            "rca_report.json": rca_report.model_dump(),
            "remediation_report.json": remed_report.model_dump(),
            "recovery_report.json": recov_report.model_dump(),
            "self_healing_report.json": self_heal_report.model_dump(),
            "chaos_report.json": chaos_report.model_dump(),
            "certification_report.json": scorecard.model_dump(),
        }

        # Calculate integrity hashes
        file_hashes = {}
        for filename, data in manifest_map.items():
            filepath = os.path.join(output_dir, filename)
            content_str = json.dumps(data, indent=2, default=str)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content_str)
            exported_files.append(filepath)
            sha = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
            file_hashes[filename] = sha

        # Metadata manifest
        now_iso = datetime.now(timezone.utc).isoformat()
        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.5",
            "capability": "Health Intelligence, Diagnosis & Automated Remediation",
            "environment": "production_verification",
            "timestamp": now_iso,
            "composite_score": scorecard.composite_score,
            "tier": scorecard.tier.value,
            "certified_enterprise_ready": scorecard.certified_enterprise_ready,
            "manifest_hashes": file_hashes,
        }

        meta_filepath = os.path.join(output_dir, "metadata.json")
        with open(meta_filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        exported_files.append(meta_filepath)

        return exported_files
