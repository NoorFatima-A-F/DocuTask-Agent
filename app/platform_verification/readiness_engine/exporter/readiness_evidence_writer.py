"""
Readiness Evidence Writer (Part 3H.3.2.13).
Persists structured audit artifacts to health_verification/ directory.
"""
import os
import json
from datetime import datetime, timezone
from dataclasses import asdict
from typing import Dict, Any
from app.platform_verification.readiness_engine.domain.models import (
    DatabaseReadinessReport,
    QueueReadinessReport,
    StorageReadinessReport,
    AIProviderReadinessReport,
    WorkerReadinessReport,
    DependencyMatrixReport,
    ReadinessEvaluationResult,
    FailureSimulationReport,
    KubernetesCompatibilityReport,
    ReadinessSecurityReport,
    ReadinessScorecard,
)


class ReadinessEvidenceWriter:
    """
    Persists structured audit artifacts for Part 3H.3.2.
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
        db_report: DatabaseReadinessReport,
        queue_report: QueueReadinessReport,
        storage_report: StorageReadinessReport,
        ai_report: AIProviderReadinessReport,
        worker_report: WorkerReadinessReport,
        matrix_report: DependencyMatrixReport,
        eval_result: ReadinessEvaluationResult,
        sim_report: FailureSimulationReport,
        k8s_report: KubernetesCompatibilityReport,
        sec_report: ReadinessSecurityReport,
        scorecard: ReadinessScorecard,
    ) -> Dict[str, str]:
        exported = {}

        # 1. readiness_engine_report.json
        exported["readiness_engine_report.json"] = self._write_json(
            "readiness_engine_report.json",
            {
                "evaluation": asdict(eval_result),
                "scorecard": asdict(scorecard),
                "kubernetes": asdict(k8s_report),
                "security": asdict(sec_report),
            },
        )

        # 2. dependency_matrix.json
        exported["dependency_matrix.json"] = self._write_json(
            "dependency_matrix.json",
            asdict(matrix_report),
        )

        # 3. database_readiness.json
        exported["database_readiness.json"] = self._write_json(
            "database_readiness.json",
            asdict(db_report),
        )

        # 4. queue_readiness.json
        exported["queue_readiness.json"] = self._write_json(
            "queue_readiness.json",
            asdict(queue_report),
        )

        # 5. storage_readiness.json
        exported["storage_readiness.json"] = self._write_json(
            "storage_readiness.json",
            asdict(storage_report),
        )

        # 6. ai_provider_readiness.json
        exported["ai_provider_readiness.json"] = self._write_json(
            "ai_provider_readiness.json",
            asdict(ai_report),
        )

        # 7. failure_tests.json
        exported["failure_tests.json"] = self._write_json(
            "failure_tests.json",
            asdict(sim_report),
        )

        # 8. metadata.json
        exported["metadata.json"] = self._write_json(
            "metadata.json",
            {
                "phase": "3H.3.2",
                "component": "Dependency-Aware Readiness Engine",
                "status": "PASS" if scorecard.passed else "FAIL",
                "score": scorecard.overall_readiness_score,
                "tier": scorecard.certification_tier.value,
                "verdict": scorecard.certification_verdict,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "total_artifacts": 8,
            },
        )

        return exported
