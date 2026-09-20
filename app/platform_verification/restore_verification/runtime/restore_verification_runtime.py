"""
Master Runtime Orchestrator for Automated Restore Verification System (Part 3G.2E).
"""
import time
from typing import Dict, Any, Optional

from app.platform_verification.restore_verification.orchestrator.restore_orchestrator import (
    RestoreOrchestrator,
)
from app.platform_verification.restore_verification.recovery_environment.recovery_environment_manager import (
    RecoveryEnvironmentManager,
)
from app.platform_verification.restore_verification.backup_connector.backup_discovery_engine import (
    BackupDiscoveryEngine,
)
from app.platform_verification.restore_verification.restore_engine.restore_execution_engine import (
    RestoreExecutionEngine,
)
from app.platform_verification.restore_verification.validation_engine.database_restore_validator import (
    DatabaseRestoreValidator,
)
from app.platform_verification.restore_verification.validation_engine.document_restore_validator import (
    DocumentRestoreValidator,
)
from app.platform_verification.restore_verification.validation_engine.config_secret_validator import (
    ConfigSecretValidator,
)
from app.platform_verification.restore_verification.validation_engine.integrity_checker import (
    IntegrityChecker,
)
from app.platform_verification.restore_verification.health_validator.service_startup_validator import (
    ServiceStartupValidator,
)
from app.platform_verification.restore_verification.functional_tests.synthetic_workflow_runner import (
    SyntheticWorkflowRunner,
)
from app.platform_verification.restore_verification.failure_handler.restore_failure_simulator import (
    RestoreFailureSimulator,
)
from app.platform_verification.restore_verification.performance.rto_rpo_benchmarking_engine import (
    RTORPOBenchmarkingEngine,
)
from app.platform_verification.restore_verification.scheduler.continuous_recovery_scheduler import (
    ContinuousRecoveryScheduler,
)
from app.platform_verification.restore_verification.scoring.restore_quality_scoring_engine import (
    RestoreQualityScoringEngine,
)
from app.platform_verification.restore_verification.evidence_generator.restore_evidence_manifest_engine import (
    RestoreEvidenceManifestEngine,
)


class RestoreVerificationRuntime:
    """
    Master orchestrator for the Part 3G.2E Automated Restore Verification System.
    Coordinates ephemeral environment provisioning, 10-tier restoration, multi-layer validation,
    failure injection, functional synthetic tests, scoring, and evidence serialization.
    """

    def __init__(
        self,
        orchestrator: Optional[RestoreOrchestrator] = None,
        env_manager: Optional[RecoveryEnvironmentManager] = None,
        backup_discovery: Optional[BackupDiscoveryEngine] = None,
        restore_engine: Optional[RestoreExecutionEngine] = None,
        db_validator: Optional[DatabaseRestoreValidator] = None,
        doc_validator: Optional[DocumentRestoreValidator] = None,
        config_secret_validator: Optional[ConfigSecretValidator] = None,
        integrity_checker: Optional[IntegrityChecker] = None,
        health_validator: Optional[ServiceStartupValidator] = None,
        workflow_runner: Optional[SyntheticWorkflowRunner] = None,
        failure_simulator: Optional[RestoreFailureSimulator] = None,
        performance_engine: Optional[RTORPOBenchmarkingEngine] = None,
        scheduler: Optional[ContinuousRecoveryScheduler] = None,
        scoring_engine: Optional[RestoreQualityScoringEngine] = None,
        evidence_engine: Optional[RestoreEvidenceManifestEngine] = None,
    ):
        self.orchestrator = orchestrator or RestoreOrchestrator()
        self.env_manager = env_manager or RecoveryEnvironmentManager()
        self.backup_discovery = backup_discovery or BackupDiscoveryEngine()
        self.restore_engine = restore_engine or RestoreExecutionEngine()
        self.db_validator = db_validator or DatabaseRestoreValidator()
        self.doc_validator = doc_validator or DocumentRestoreValidator()
        self.config_secret_validator = config_secret_validator or ConfigSecretValidator()
        self.integrity_checker = integrity_checker or IntegrityChecker()
        self.health_validator = health_validator or ServiceStartupValidator()
        self.workflow_runner = workflow_runner or SyntheticWorkflowRunner()
        self.failure_simulator = failure_simulator or RestoreFailureSimulator()
        self.performance_engine = performance_engine or RTORPOBenchmarkingEngine()
        self.scheduler = scheduler or ContinuousRecoveryScheduler()
        self.scoring_engine = scoring_engine or RestoreQualityScoringEngine()
        self.evidence_engine = evidence_engine or RestoreEvidenceManifestEngine()

    def execute_full_restore_verification(
        self, output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Runs the complete automated disaster recovery validation workflow.
        """
        start_time = time.perf_counter()

        # Step 1: Backup Discovery
        backup_catalog_report = self.backup_discovery.discover_and_catalog_backups()

        # Step 2: Restore Orchestration & Plan Construction
        plan = self.orchestrator.generate_restore_plan()

        # Step 3: Ephemeral Recovery Environment Provisioning
        env_report = self.env_manager.provision_recovery_environment()

        # Step 4: 10-Tier Dependency-Ordered Restoration Execution
        execution_report = self.restore_engine.execute_ordered_restore(plan)

        # Step 5: Database & Document Storage Validation
        db_report = self.db_validator.validate_database_restore()
        doc_report = self.doc_validator.validate_document_restore()

        # Step 6: Configuration & Secret Validation
        cfg_report, sec_report = self.config_secret_validator.validate_configuration_and_secrets()

        # Step 7: Cryptographic Triple Checksum Validation
        integrity_report = self.integrity_checker.verify_triple_checksum_integrity()

        # Step 8: Service Startup & Health Probe Evaluation
        startup_report = self.health_validator.validate_service_health_and_readiness()

        # Step 9: Synthetic Business Workflow Validation
        functional_report = self.workflow_runner.execute_synthetic_business_workflows()

        # Step 10: Injected Disaster Recovery Failure Simulations & Rollbacks
        failure_report = self.failure_simulator.simulate_failure_scenarios_and_rollbacks()

        # Step 11: RTO/RPO Performance Measurement
        rto_rpo_report = self.performance_engine.measure_rto_rpo_performance()

        # Step 12: Ephemeral Environment Teardown
        self.env_manager.teardown_recovery_environment()

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # Step 13: Scoring & Certification
        b_score = 100.0 if execution_report["passed"] and env_report.passed else 70.0
        d_score = 100.0 if (db_report.passed and doc_report.passed and integrity_report.passed) else 65.0
        s_score = 100.0 if startup_report.passed else 50.0
        f_score = 100.0 if functional_report.passed else 40.0
        sec_score = 100.0 if sec_report.passed else 60.0
        spd_score = 100.0 if rto_rpo_report.passed else 75.0

        scorecard = self.scoring_engine.compute_quality_scorecard(
            backup_recovery_success_score=b_score,
            data_integrity_score=d_score,
            service_recovery_score=s_score,
            functional_validation_score=f_score,
            security_validation_score=sec_score,
            recovery_speed_score=spd_score,
            execution_duration_ms=elapsed_ms,
        )

        verification_data = {
            "restore_execution_report": execution_report,
            "recovery_environment_report": env_report,
            "backup_catalog": backup_catalog_report,
            "database_restore_validation": db_report,
            "document_restore_validation": doc_report,
            "configuration_restore_validation": cfg_report,
            "secret_restore_validation": sec_report,
            "service_startup_report": startup_report,
            "functional_recovery_report": functional_report,
            "integrity_validation_report": integrity_report,
            "rto_rpo_report": rto_rpo_report,
            "failure_simulation_report": failure_report,
            "scorecard": scorecard,
        }

        # Step 14: Evidence Serialization
        manifest_paths = self.evidence_engine.export_all_evidence_artifacts(
            verification_data, output_dir=output_dir
        )

        verification_data["exported_manifest_paths"] = manifest_paths
        verification_data["passed"] = scorecard.passed

        return verification_data
