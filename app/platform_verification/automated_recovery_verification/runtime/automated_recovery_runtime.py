"""
Phase 3H.12: Runtime Orchestrator for Enterprise Automated Recovery & Self-Healing Verification
"""
from typing import Dict, Any
from ..domain.models import (
    RecoveryArchitectureReport,
    RecoveryPolicyReport,
    ServiceRestartReport,
    DatabaseRecoveryReport,
    QueueRecoveryReport,
    WorkerRecoveryReport,
    AIRecoveryReport,
    CircuitBreakerReport,
    RecoveryValidationReport,
    ReliabilityMetricsReport,
    RecoverySafetyReport,
    RecoveryAuditReport,
    RecoveryCertificationReport,
)
from ..verifiers.recovery_architecture_verifier import RecoveryArchitectureVerifier
from ..verifiers.recovery_policy_verifier import RecoveryPolicyVerifier
from ..verifiers.service_restart_verifier import ServiceRestartVerifier
from ..verifiers.database_recovery_verifier import DatabaseRecoveryVerifier
from ..verifiers.queue_recovery_verifier import QueueRecoveryVerifier
from ..verifiers.worker_self_healing_verifier import WorkerSelfHealingVerifier
from ..verifiers.ai_fallback_recovery_verifier import AIFallbackRecoveryVerifier
from ..verifiers.circuit_breaker_verifier import CircuitBreakerVerifier
from ..verifiers.recovery_validation_engine_verifier import RecoveryValidationEngineVerifier
from ..verifiers.reliability_metrics_verifier import ReliabilityMetricsVerifier
from ..verifiers.recovery_safety_verifier import RecoverySafetyVerifier
from ..verifiers.recovery_audit_verifier import RecoveryAuditVerifier
from ..scoring.automated_recovery_scorer import AutomatedRecoveryScorer
from ..exporter.automated_recovery_exporter import AutomatedRecoveryExporter


class AutomatedRecoveryRuntime:
    """
    Coordinates all recovery verification routines, computes 6-pillar score, and exports manifests.
    """

    def __init__(self):
        self.arch_verifier = RecoveryArchitectureVerifier()
        self.policy_verifier = RecoveryPolicyVerifier()
        self.restart_verifier = ServiceRestartVerifier()
        self.db_verifier = DatabaseRecoveryVerifier()
        self.queue_verifier = QueueRecoveryVerifier()
        self.worker_verifier = WorkerSelfHealingVerifier()
        self.ai_verifier = AIFallbackRecoveryVerifier()
        self.circuit_verifier = CircuitBreakerVerifier()
        self.validation_verifier = RecoveryValidationEngineVerifier()
        self.metrics_verifier = ReliabilityMetricsVerifier()
        self.safety_verifier = RecoverySafetyVerifier()
        self.audit_verifier = RecoveryAuditVerifier()
        self.scorer = AutomatedRecoveryScorer()
        self.exporter = AutomatedRecoveryExporter()

    def run_full_verification(self, export_dir: str = "automated_recovery_verification") -> Dict[str, Any]:
        arch_report: RecoveryArchitectureReport = self.arch_verifier.verify_recovery_architecture()
        policy_report: RecoveryPolicyReport = self.policy_verifier.verify_recovery_policies()
        restart_report: ServiceRestartReport = self.restart_verifier.verify_service_restart()
        db_report: DatabaseRecoveryReport = self.db_verifier.verify_database_recovery()
        queue_report: QueueRecoveryReport = self.queue_verifier.verify_queue_recovery()
        worker_report: WorkerRecoveryReport = self.worker_verifier.verify_worker_self_healing()
        ai_report: AIRecoveryReport = self.ai_verifier.verify_ai_recovery()
        circuit_report: CircuitBreakerReport = self.circuit_verifier.verify_circuit_breaker()
        validation_report: RecoveryValidationReport = self.validation_verifier.verify_validation_engine()
        metrics_report: ReliabilityMetricsReport = self.metrics_verifier.verify_reliability_metrics()
        safety_report: RecoverySafetyReport = self.safety_verifier.verify_recovery_safety()
        audit_report: RecoveryAuditReport = self.audit_verifier.verify_recovery_audit()

        certification_report: RecoveryCertificationReport = self.scorer.calculate_certification_score(
            arch_report=arch_report,
            policy_report=policy_report,
            restart_report=restart_report,
            db_report=db_report,
            queue_report=queue_report,
            worker_report=worker_report,
            ai_report=ai_report,
            circuit_report=circuit_report,
            validation_report=validation_report,
            metrics_report=metrics_report,
            safety_report=safety_report,
            audit_report=audit_report,
        )

        metadata = self.exporter.export_all_reports(
            output_dir=export_dir,
            arch_report=arch_report,
            policy_report=policy_report,
            restart_report=restart_report,
            db_report=db_report,
            queue_report=queue_report,
            worker_report=worker_report,
            ai_report=ai_report,
            circuit_report=circuit_report,
            validation_report=validation_report,
            metrics_report=metrics_report,
            safety_report=safety_report,
            audit_report=audit_report,
            certification_report=certification_report,
        )

        return {
            "arch_report": arch_report,
            "policy_report": policy_report,
            "restart_report": restart_report,
            "db_report": db_report,
            "queue_report": queue_report,
            "worker_report": worker_report,
            "ai_report": ai_report,
            "circuit_report": circuit_report,
            "validation_report": validation_report,
            "metrics_report": metrics_report,
            "safety_report": safety_report,
            "audit_report": audit_report,
            "certification_report": certification_report,
            "metadata": metadata,
        }
