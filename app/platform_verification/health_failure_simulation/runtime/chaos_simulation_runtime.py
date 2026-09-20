"""
Phase 3H.11: Runtime Orchestrator for Enterprise Health Failure Simulation & Chaos Verification
"""
from typing import Dict, Any
from ..domain.models import (
    ChaosArchitectureReport,
    ScenarioRegistryReport,
    DatabaseFailureReport,
    QueueFailureReport,
    WorkerFailureReport,
    AIProviderFailureReport,
    ResourceFailureReport,
    FailureDetectionMetricsReport,
    RollbackValidationReport,
    ChaosSafetyReport,
    ChaosCertificationReport,
)
from ..verifiers.chaos_architecture_verifier import ChaosArchitectureVerifier
from ..verifiers.scenario_registry_verifier import ScenarioRegistryVerifier
from ..verifiers.database_failure_verifier import DatabaseFailureVerifier
from ..verifiers.queue_failure_verifier import QueueFailureVerifier
from ..verifiers.worker_failure_verifier import WorkerFailureVerifier
from ..verifiers.ai_failure_verifier import AIProviderFailureVerifier
from ..verifiers.resource_failure_verifier import ResourceFailureVerifier
from ..verifiers.detection_metrics_verifier import FailureDetectionMetricsVerifier
from ..verifiers.rollback_verifier import RollbackValidationVerifier
from ..verifiers.safety_verifier import ChaosSafetyVerifier
from ..scoring.chaos_reliability_scorer import ChaosReliabilityScorer
from ..exporter.chaos_evidence_exporter import ChaosEvidenceExporter


class ChaosSimulationRuntime:
    """
    Executes all Phase 3H.11 chaos experiments, scores reliability across 5 pillars, and exports cryptographically signed manifests.
    """

    def __init__(self):
        self.arch_verifier = ChaosArchitectureVerifier()
        self.registry_verifier = ScenarioRegistryVerifier()
        self.db_verifier = DatabaseFailureVerifier()
        self.queue_verifier = QueueFailureVerifier()
        self.worker_verifier = WorkerFailureVerifier()
        self.ai_verifier = AIProviderFailureVerifier()
        self.resource_verifier = ResourceFailureVerifier()
        self.detection_verifier = FailureDetectionMetricsVerifier()
        self.rollback_verifier = RollbackValidationVerifier()
        self.safety_verifier = ChaosSafetyVerifier()
        self.scorer = ChaosReliabilityScorer()
        self.exporter = ChaosEvidenceExporter()

    def run_full_verification(self, export_dir: str = "health_failure_simulation") -> Dict[str, Any]:
        arch_report: ChaosArchitectureReport = self.arch_verifier.verify_chaos_architecture()
        registry_report: ScenarioRegistryReport = self.registry_verifier.verify_scenario_registry()
        db_report: DatabaseFailureReport = self.db_verifier.verify_database_failure()
        queue_report: QueueFailureReport = self.queue_verifier.verify_queue_failure()
        worker_report: WorkerFailureReport = self.worker_verifier.verify_worker_failure()
        ai_report: AIProviderFailureReport = self.ai_verifier.verify_ai_failure()
        resource_report: ResourceFailureReport = self.resource_verifier.verify_resource_failure()
        detection_report: FailureDetectionMetricsReport = self.detection_verifier.verify_detection_metrics()
        rollback_report: RollbackValidationReport = self.rollback_verifier.verify_rollback()
        safety_report: ChaosSafetyReport = self.safety_verifier.verify_safety()

        certification_report: ChaosCertificationReport = self.scorer.calculate_certification_score(
            arch_report=arch_report,
            registry_report=registry_report,
            db_report=db_report,
            queue_report=queue_report,
            worker_report=worker_report,
            ai_report=ai_report,
            resource_report=resource_report,
            detection_report=detection_report,
            rollback_report=rollback_report,
            safety_report=safety_report,
        )

        metadata = self.exporter.export_all_reports(
            output_dir=export_dir,
            arch_report=arch_report,
            registry_report=registry_report,
            db_report=db_report,
            queue_report=queue_report,
            worker_report=worker_report,
            ai_report=ai_report,
            resource_report=resource_report,
            detection_report=detection_report,
            rollback_report=rollback_report,
            safety_report=safety_report,
            certification_report=certification_report,
        )

        return {
            "arch_report": arch_report,
            "registry_report": registry_report,
            "db_report": db_report,
            "queue_report": queue_report,
            "worker_report": worker_report,
            "ai_report": ai_report,
            "resource_report": resource_report,
            "detection_report": detection_report,
            "rollback_report": rollback_report,
            "safety_report": safety_report,
            "certification_report": certification_report,
            "metadata": metadata,
        }
