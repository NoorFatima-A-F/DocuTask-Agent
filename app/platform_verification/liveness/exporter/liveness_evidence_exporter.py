"""
Liveness Evidence Exporter (Part 15).
Exports JSON verification evidence artifacts to the health_verification/ directory.
"""
import os
import json
from datetime import datetime, timezone
from dataclasses import asdict
from typing import Dict, Any
from app.platform_verification.liveness.domain.models import (
    LivenessContractReport,
    ProcessStateReport,
    EventLoopHealthReport,
    DeadlockReport,
    WorkerLivenessReport,
    SchedulerLivenessReport,
    ResourceHealthReport,
    FailureSimulationReport,
    RecoveryReport,
    SecurityReport,
    LivenessScorecard,
)


class LivenessEvidenceExporter:
    """
    Persists structured audit artifacts for liveness verification to disk.
    """

    def __init__(self, output_dir: str = "health_verification"):
        self.output_dir = output_dir

    def _ensure_dir(self):
        os.makedirs(self.output_dir, exist_ok=True)

    def _write_json(self, filename: str, data: Dict[str, Any]) -> str:
        self._ensure_dir()
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        return file_path

    def export_all(
        self,
        contract_report: LivenessContractReport,
        process_report: ProcessStateReport,
        loop_report: EventLoopHealthReport,
        deadlock_report: DeadlockReport,
        worker_report: WorkerLivenessReport,
        scheduler_report: SchedulerLivenessReport,
        resource_report: ResourceHealthReport,
        failure_report: FailureSimulationReport,
        recovery_report: RecoveryReport,
        security_report: SecurityReport,
        scorecard: LivenessScorecard,
    ) -> Dict[str, str]:
        exported = {}

        # 1. liveness_contract_report.json
        exported["liveness_contract_report.json"] = self._write_json(
            "liveness_contract_report.json",
            asdict(contract_report),
        )

        # 2. process_health_report.json
        exported["process_health_report.json"] = self._write_json(
            "process_health_report.json",
            asdict(process_report),
        )

        # 3. event_loop_report.json
        exported["event_loop_report.json"] = self._write_json(
            "event_loop_report.json",
            asdict(loop_report),
        )

        # 4. deadlock_report.json
        exported["deadlock_report.json"] = self._write_json(
            "deadlock_report.json",
            asdict(deadlock_report),
        )

        # 5. worker_liveness_report.json
        exported["worker_liveness_report.json"] = self._write_json(
            "worker_liveness_report.json",
            asdict(worker_report),
        )

        # 6. resource_health_report.json
        exported["resource_health_report.json"] = self._write_json(
            "resource_health_report.json",
            asdict(resource_report),
        )

        # 7. failure_simulation_report.json
        exported["failure_simulation_report.json"] = self._write_json(
            "failure_simulation_report.json",
            asdict(failure_report),
        )

        # 8. recovery_report.json
        exported["recovery_report.json"] = self._write_json(
            "recovery_report.json",
            asdict(recovery_report),
        )

        # 9. certification.json
        exported["certification.json"] = self._write_json(
            "certification.json",
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "phase": "PART 3H.2 — Enterprise Liveness Verification Framework",
                "scorecard": asdict(scorecard),
                "certified": scorecard.passed,
                "tier": scorecard.certification_tier.value,
                "verdict": scorecard.certification_verdict,
            },
        )

        # 10. metadata.json
        exported["metadata.json"] = self._write_json(
            "metadata.json",
            {
                "project": "DocuTask-Agent",
                "phase": "3H.2",
                "commit": "master-verified",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "environment": "production-hardened",
                "total_artifacts": 10,
                "score": scorecard.overall_liveness_score,
                "passed": scorecard.passed,
            },
        )

        return exported
