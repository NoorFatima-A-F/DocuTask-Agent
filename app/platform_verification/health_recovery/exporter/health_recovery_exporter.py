"""
Phase 3H.5.12: Health Recovery Evidence Exporter
"""
import os
import json
import hashlib
from typing import Dict, Any
from datetime import datetime, timezone

from ..domain.models import (
    HealthStateTransitionReport,
    FailureDetectionReport,
    RecoveryPolicyReport,
    ComponentRecoveryReport,
    RecoverySafetyReport,
    SelfHealingReport,
    RecoveryChaosReport,
    RecoveryValidationReport,
    RecoveryObservabilityReport,
    RecoverySecurityReport,
    HealthRecoveryScorecard,
)


class HealthRecoveryExporter:
    """
    Exports all 11 health recovery verification reports and metadata.json
    with SHA-256 cryptographic signatures.
    """

    def __init__(self, output_dir: str = "health_recovery_verification"):
        self.output_dir = output_dir

    def _compute_sha256(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def export_all(
        self,
        transition_report: HealthStateTransitionReport,
        detection_report: FailureDetectionReport,
        policy_report: RecoveryPolicyReport,
        component_report: ComponentRecoveryReport,
        safety_report: RecoverySafetyReport,
        self_healing_report: SelfHealingReport,
        chaos_report: RecoveryChaosReport,
        validation_report: RecoveryValidationReport,
        observability_report: RecoveryObservabilityReport,
        security_report: RecoverySecurityReport,
        scorecard: HealthRecoveryScorecard,
    ) -> Dict[str, str]:
        os.makedirs(self.output_dir, exist_ok=True)

        artifacts = {
            "state_transition_report.json": transition_report.model_dump(),
            "failure_detection_report.json": detection_report.model_dump(),
            "recovery_policy_report.json": policy_report.model_dump(),
            "component_recovery_report.json": component_report.model_dump(),
            "safety_report.json": safety_report.model_dump(),
            "self_healing_report.json": self_healing_report.model_dump(),
            "chaos_report.json": chaos_report.model_dump(),
            "validation_report.json": validation_report.model_dump(),
            "observability_report.json": observability_report.model_dump(),
            "security_report.json": security_report.model_dump(),
            "certification_report.json": scorecard.model_dump(),
        }

        generated_files = {}
        for filename, data in artifacts.items():
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            generated_files[filename] = filepath

        # Calculate checksums for metadata.json
        checksums = {}
        for filename, filepath in generated_files.items():
            checksums[filename] = self._compute_sha256(filepath)

        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.5.12 — Automated Health Recovery Verification Framework",
            "environment": "production-recovery-verification",
            "commit": "master-latest",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "recovery_engine_version": "1.0.0",
            "overall_score": scorecard.overall_recovery_score,
            "certification_tier": scorecard.certification_tier.value,
            "passed": scorecard.passed,
            "mttr_seconds": scorecard.mttr_seconds,
            "mttd_seconds": scorecard.mttd_seconds,
            "recovery_success_rate": scorecard.recovery_success_rate,
            "file_manifest": checksums,
        }

        metadata_path = os.path.join(self.output_dir, "metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        generated_files["metadata.json"] = metadata_path
        return generated_files
