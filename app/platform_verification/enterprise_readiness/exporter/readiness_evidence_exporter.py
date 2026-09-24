"""Readiness Evidence Exporter (3H.3.12).

Exports 11 structured JSON manifests into health_verification/:
1. readiness_contract_report.json
2. dependency_readiness_report.json
3. database_readiness_report.json
4. queue_readiness_report.json
5. worker_readiness_report.json
6. ai_provider_readiness_report.json
7. startup_readiness_report.json
8. failure_simulation_report.json
9. orchestration_report.json
10. metrics_report.json
11. metadata.json
"""

import os
import json
from dataclasses import asdict
from typing import Dict
from ..domain.models import (
    ReadinessContractReport,
    DependencyReadinessReport,
    DatabaseReadinessReport,
    QueueReadinessReport,
    WorkerReadinessReport,
    AIProviderReadinessReport,
    StartupReadinessReport,
    FailureSimulationReport,
    OrchestrationReport,
    ReadinessMetricsReport,
    ReadinessCertificationScorecard,
)
from ..domain.interfaces import IReadinessEvidenceExporter


class ReadinessEvidenceExporter(IReadinessEvidenceExporter):
    """Exports readiness verification evidence to structured JSON files."""

    def __init__(self, export_dir: str = "health_verification"):
        self.export_dir = export_dir

    def export_all(
        self,
        contract_rep: ReadinessContractReport,
        dep_rep: DependencyReadinessReport,
        db_rep: DatabaseReadinessReport,
        queue_rep: QueueReadinessReport,
        worker_rep: WorkerReadinessReport,
        ai_rep: AIProviderReadinessReport,
        startup_rep: StartupReadinessReport,
        sim_rep: FailureSimulationReport,
        orch_rep: OrchestrationReport,
        obs_rep: ReadinessMetricsReport,
        scorecard: ReadinessCertificationScorecard,
    ) -> Dict[str, str]:
        os.makedirs(self.export_dir, exist_ok=True)
        manifests: Dict[str, str] = {}

        # 1. readiness_contract_report.json
        p1 = os.path.join(self.export_dir, "readiness_contract_report.json")
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(asdict(contract_rep), f, indent=2)
        manifests["readiness_contract_report.json"] = p1

        # 2. dependency_readiness_report.json
        p2 = os.path.join(self.export_dir, "dependency_readiness_report.json")
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(asdict(dep_rep), f, indent=2)
        manifests["dependency_readiness_report.json"] = p2

        # 3. database_readiness_report.json
        p3 = os.path.join(self.export_dir, "database_readiness_report.json")
        with open(p3, "w", encoding="utf-8") as f:
            json.dump(asdict(db_rep), f, indent=2)
        manifests["database_readiness_report.json"] = p3

        # 4. queue_readiness_report.json
        p4 = os.path.join(self.export_dir, "queue_readiness_report.json")
        with open(p4, "w", encoding="utf-8") as f:
            json.dump(asdict(queue_rep), f, indent=2)
        manifests["queue_readiness_report.json"] = p4

        # 5. worker_readiness_report.json
        p5 = os.path.join(self.export_dir, "worker_readiness_report.json")
        with open(p5, "w", encoding="utf-8") as f:
            json.dump(asdict(worker_rep), f, indent=2)
        manifests["worker_readiness_report.json"] = p5

        # 6. ai_provider_readiness_report.json
        p6 = os.path.join(self.export_dir, "ai_provider_readiness_report.json")
        with open(p6, "w", encoding="utf-8") as f:
            json.dump(asdict(ai_rep), f, indent=2)
        manifests["ai_provider_readiness_report.json"] = p6

        # 7. startup_readiness_report.json
        p7 = os.path.join(self.export_dir, "startup_readiness_report.json")
        with open(p7, "w", encoding="utf-8") as f:
            json.dump(asdict(startup_rep), f, indent=2)
        manifests["startup_readiness_report.json"] = p7

        # 8. failure_simulation_report.json
        p8 = os.path.join(self.export_dir, "failure_simulation_report.json")
        with open(p8, "w", encoding="utf-8") as f:
            json.dump(asdict(sim_rep), f, indent=2)
        manifests["failure_simulation_report.json"] = p8

        # 9. orchestration_report.json
        p9 = os.path.join(self.export_dir, "orchestration_report.json")
        with open(p9, "w", encoding="utf-8") as f:
            json.dump(asdict(orch_rep), f, indent=2)
        manifests["orchestration_report.json"] = p9

        # 10. metrics_report.json
        p10 = os.path.join(self.export_dir, "metrics_report.json")
        with open(p10, "w", encoding="utf-8") as f:
            json.dump(asdict(obs_rep), f, indent=2)
        manifests["metrics_report.json"] = p10

        # 11. metadata.json
        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.3",
            "commit": "HEAD",
            "timestamp": scorecard.timestamp,
            "environment": "production",
            "scorecard": asdict(scorecard),
            "manifest_files": list(manifests.keys()),
            "status": "CERTIFIED" if scorecard.passed else "FAILED",
        }
        p11 = os.path.join(self.export_dir, "metadata.json")
        with open(p11, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        manifests["metadata.json"] = p11

        return manifests
