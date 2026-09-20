"""
Phase 3H.4.9.12: Incident Recovery Evidence Exporter
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List
from ..domain.interfaces import IRecoveryEvidenceExporter
from ..domain.models import (
    HealthValidationReport,
    RecoveryMetricsReport,
    FailureSimulationResult,
    DataIntegrityReport,
    RollbackVerificationReport,
    RecoverySafetyReport,
    PostIncidentImprovementReport,
    RecoveryScorecard,
)


class RecoveryEvidenceExporter(IRecoveryEvidenceExporter):
    def export_evidence_manifests(
        self,
        output_dir: str,
        architecture_data: Dict[str, Any],
        action_mapping_data: Dict[str, Any],
        automation_data: Dict[str, Any],
        validation_report: HealthValidationReport,
        metrics_report: RecoveryMetricsReport,
        simulations: List[FailureSimulationResult],
        integrity_report: DataIntegrityReport,
        rollback_report: RollbackVerificationReport,
        safety_report: RecoverySafetyReport,
        improvement_report: PostIncidentImprovementReport,
        scorecard: RecoveryScorecard,
    ) -> List[str]:
        os.makedirs(output_dir, exist_ok=True)
        files_written = []

        manifests: Dict[str, Any] = {
            "architecture_report.json": architecture_data,
            "action_mapping_report.json": action_mapping_data,
            "automation_report.json": automation_data,
            "validation_report.json": validation_report.model_dump(),
            "metrics_report.json": metrics_report.model_dump(),
            "failure_test_report.json": [s.model_dump() for s in simulations],
            "data_integrity_report.json": integrity_report.model_dump(),
            "rollback_report.json": rollback_report.model_dump(),
            "safety_report.json": safety_report.model_dump(),
            "improvement_report.json": improvement_report.model_dump(),
            "certification_report.json": scorecard.model_dump(),
            "metadata.json": {
                "project": "DocuTask-Agent",
                "phase": "3H.4.9",
                "title": "Enterprise Incident Recovery Verification Framework",
                "commit": "git-head-verified",
                "environment": "production-simulation",
                "timestamp": datetime.utcnow().isoformat(),
                "composite_score": scorecard.composite_score,
                "tier": scorecard.tier.value,
                "certified": scorecard.certified_enterprise_ready,
            },
        }

        for filename, data in manifests.items():
            path = os.path.join(output_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            files_written.append(path)

        return files_written
