"""
Enterprise Liveness Verification Runtime Coordinator.
Orchestrates all 16 parts of the Enterprise Liveness Verification Framework.
"""
from typing import Dict, Any
from app.platform_verification.liveness.contract.liveness_contract_manager import (
    LivenessContractManager,
)
from app.platform_verification.liveness.process.process_verifier import (
    ProcessVerifier,
)
from app.platform_verification.liveness.event_loop.event_loop_monitor import (
    EventLoopMonitor,
)
from app.platform_verification.liveness.deadlock.deadlock_detector import (
    DeadlockDetector,
)
from app.platform_verification.liveness.worker.worker_heartbeat_manager import (
    WorkerHeartbeatManager,
)
from app.platform_verification.liveness.scheduler.scheduler_liveness_monitor import (
    SchedulerLivenessMonitor,
)
from app.platform_verification.liveness.resources.resource_monitor import (
    ResourceMonitor,
)
from app.platform_verification.liveness.failure_injection.liveness_failure_injector import (
    LivenessFailureInjector,
)
from app.platform_verification.liveness.recovery.automated_recovery_verifier import (
    AutomatedRecoveryVerifier,
)
from app.platform_verification.liveness.security.liveness_security_verifier import (
    LivenessSecurityVerifier,
)
from app.platform_verification.liveness.observability.liveness_metrics_exporter import (
    LivenessMetricsExporter,
)
from app.platform_verification.liveness.scoring.liveness_score_engine import (
    LivenessScoreEngine,
)
from app.platform_verification.liveness.exporter.liveness_evidence_exporter import (
    LivenessEvidenceExporter,
)


class LivenessVerificationRuntime:
    """
    Master Runtime Coordinator for Part 3H.2 Enterprise Liveness Verification Framework.
    """

    def __init__(self, output_dir: str = "health_verification", contract_path: str = "liveness_contract.yaml"):
        self.contract_manager = LivenessContractManager(contract_path=contract_path)
        self.process_verifier = ProcessVerifier()
        self.event_loop_monitor = EventLoopMonitor()
        self.deadlock_detector = DeadlockDetector()
        self.worker_heartbeat_manager = WorkerHeartbeatManager()
        self.scheduler_monitor = SchedulerLivenessMonitor()
        self.resource_monitor = ResourceMonitor()
        self.failure_injector = LivenessFailureInjector()
        self.recovery_verifier = AutomatedRecoveryVerifier()
        self.security_verifier = LivenessSecurityVerifier()
        self.metrics_exporter = LivenessMetricsExporter()
        self.score_engine = LivenessScoreEngine()
        self.exporter = LivenessEvidenceExporter(output_dir=output_dir)

    def run_full_verification(self, export: bool = True) -> Dict[str, Any]:
        # Part 1: Contract Design
        contract_rep = self.contract_manager.verify_liveness_contracts()

        # Part 2: Process Existence & State Monitoring
        process_rep = self.process_verifier.verify_processes()

        # Part 3: Event Loop Responsiveness
        loop_rep = self.event_loop_monitor.monitor_event_loop()

        # Part 4: Deadlock Detection & Watchdog
        deadlock_rep = self.deadlock_detector.detect_deadlocks()

        # Parts 5 & 8: Thread/Task & Worker Liveness
        worker_rep = self.worker_heartbeat_manager.evaluate_worker_heartbeats()

        # Part 9: Scheduler Liveness
        scheduler_rep = self.scheduler_monitor.check_scheduler_liveness()

        # Parts 6 & 7: Memory & CPU Resource Health
        resource_rep = self.resource_monitor.check_resource_health()

        # Part 11: Failure Simulation Testing
        failure_rep = self.failure_injector.execute_failure_simulations()

        # Parts 10 & 12: Container Runtime & Automated Recovery (MTTR)
        recovery_rep = self.recovery_verifier.verify_recovery()

        # Part 13: Security & Zero Information Leakage
        security_rep = self.security_verifier.verify_security()

        # Part 14: Observability
        metrics_summary = self.metrics_exporter.get_metrics_summary()

        # Part 16: Scoring Engine (Exact 6 categories)
        scorecard = self.score_engine.compute_scorecard(
            contract_report=contract_rep,
            process_report=process_rep,
            loop_report=loop_rep,
            deadlock_report=deadlock_rep,
            worker_report=worker_rep,
            scheduler_report=scheduler_rep,
            resource_report=resource_rep,
            failure_report=failure_rep,
            recovery_report=recovery_rep,
            security_report=security_rep,
        )

        # Part 15: Evidence Persistence
        exported_files = {}
        if export:
            exported_files = self.exporter.export_all(
                contract_report=contract_rep,
                process_report=process_rep,
                loop_report=loop_rep,
                deadlock_report=deadlock_rep,
                worker_report=worker_rep,
                scheduler_report=scheduler_rep,
                resource_report=resource_rep,
                failure_report=failure_rep,
                recovery_report=recovery_rep,
                security_report=security_rep,
                scorecard=scorecard,
            )

        return {
            "contract_report": contract_rep,
            "process_report": process_rep,
            "loop_report": loop_rep,
            "deadlock_report": deadlock_rep,
            "worker_report": worker_rep,
            "scheduler_report": scheduler_rep,
            "resource_report": resource_rep,
            "failure_report": failure_rep,
            "recovery_report": recovery_rep,
            "security_report": security_rep,
            "metrics_summary": metrics_summary,
            "scorecard": scorecard,
            "exported_files": exported_files,
            "success": scorecard.passed,
        }
