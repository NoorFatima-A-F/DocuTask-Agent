"""
Readiness Evidence Exporter (Part 12).
Exports JSON verification evidence artifacts to the readiness_verification/ directory.
"""
import os
import json
from datetime import datetime, timezone
from dataclasses import asdict
from typing import Dict, Any
from app.platform_verification.readiness_contract.domain.models import (
    ReadinessContractReport,
    StateMachineReport,
    DependencyPolicyReport,
    StartupValidationReport,
    FailureTransitionReport,
    OrchestrationReport,
    ReadinessScorecard,
)


class ReadinessEvidenceExporter:
    """
    Persists structured audit artifacts for readiness contract verification.
    """

    def __init__(self, output_dir: str = "readiness_verification"):
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
        contract_report: ReadinessContractReport,
        state_report: StateMachineReport,
        policy_report: DependencyPolicyReport,
        startup_report: StartupValidationReport,
        failure_report: FailureTransitionReport,
        orch_report: OrchestrationReport,
        scorecard: ReadinessScorecard,
    ) -> Dict[str, str]:
        exported = {}

        # 1. readiness_contract_report.json
        exported["readiness_contract_report.json"] = self._write_json(
            "readiness_contract_report.json",
            asdict(contract_report),
        )

        # 2. state_machine_report.json
        exported["state_machine_report.json"] = self._write_json(
            "state_machine_report.json",
            asdict(state_report),
        )

        # 3. dependency_policy_report.json
        exported["dependency_policy_report.json"] = self._write_json(
            "dependency_policy_report.json",
            asdict(policy_report),
        )

        # 4. startup_validation_report.json
        exported["startup_validation_report.json"] = self._write_json(
            "startup_validation_report.json",
            asdict(startup_report),
        )

        # 5. failure_transition_report.json
        exported["failure_transition_report.json"] = self._write_json(
            "failure_transition_report.json",
            asdict(failure_report),
        )

        # 6. orchestration_report.json
        exported["orchestration_report.json"] = self._write_json(
            "orchestration_report.json",
            asdict(orch_report),
        )

        # 7. certification.json
        exported["certification.json"] = self._write_json(
            "certification.json",
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "phase": "3H.3.1",
                "component": "Readiness Contract",
                "status": "PASS" if scorecard.passed else "FAIL",
                "score": scorecard.overall_readiness_score,
                "tier": scorecard.certification_tier.value,
                "verdict": scorecard.certification_verdict,
                "scorecard": asdict(scorecard),
            },
        )

        # 8. metadata.json
        exported["metadata.json"] = self._write_json(
            "metadata.json",
            {
                "phase": "3H.3.1",
                "component": "Readiness Contract",
                "status": "PASS" if scorecard.passed else "FAIL",
                "score": scorecard.overall_readiness_score,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "total_artifacts": 8,
            },
        )

        return exported
