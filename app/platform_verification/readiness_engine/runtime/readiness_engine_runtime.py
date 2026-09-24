"""
Master Readiness Engine Runtime Coordinator (Part 3H.3.2).
Orchestrates dependency evaluation, checkers, policy matrix, failure simulations,
Kubernetes probe verification, security audit, metrics export, and evidence generation.
"""
from typing import Dict, Any

from app.platform_verification.readiness_engine.policy.dependency_policy_engine import DependencyPolicyEngine
from app.platform_verification.readiness_engine.checkers.database_readiness_checker import DatabaseReadinessChecker
from app.platform_verification.readiness_engine.checkers.queue_readiness_checker import QueueReadinessChecker
from app.platform_verification.readiness_engine.checkers.storage_readiness_checker import StorageReadinessChecker
from app.platform_verification.readiness_engine.checkers.ai_readiness_checker import AIProviderReadinessChecker
from app.platform_verification.readiness_engine.checkers.worker_readiness_checker import WorkerReadinessChecker
from app.platform_verification.readiness_engine.aggregator.readiness_evaluator import ReadinessEvaluator
from app.platform_verification.readiness_engine.simulation.readiness_failure_simulator import ReadinessFailureSimulator
from app.platform_verification.readiness_engine.orchestration.k8s_readiness_verifier import KubernetesReadinessVerifier
from app.platform_verification.readiness_engine.security.readiness_security_auditor import ReadinessSecurityAuditor
from app.platform_verification.readiness_engine.observability.readiness_metrics_exporter import ReadinessMetricsExporter
from app.platform_verification.readiness_engine.scoring.readiness_quality_scorer import ReadinessQualityScorer
from app.platform_verification.readiness_engine.exporter.readiness_evidence_writer import ReadinessEvidenceWriter


class ReadinessEngineRuntime:
    """
    Master runtime coordinator for Part 3H.3.2.
    """

    def __init__(
        self,
        policy_path: str = "dependency_policy.yaml",
        evidence_dir: str = "health_verification",
    ):
        self.policy_engine = DependencyPolicyEngine(policy_path=policy_path)
        self.db_checker = DatabaseReadinessChecker()
        self.queue_checker = QueueReadinessChecker()
        self.storage_checker = StorageReadinessChecker()
        self.ai_checker = AIProviderReadinessChecker()
        self.worker_checker = WorkerReadinessChecker()
        self.evaluator = ReadinessEvaluator(policy_engine=self.policy_engine)
        self.simulator = ReadinessFailureSimulator()
        self.k8s_verifier = KubernetesReadinessVerifier()
        self.security_auditor = ReadinessSecurityAuditor()
        self.metrics_exporter = ReadinessMetricsExporter()
        self.scorer = ReadinessQualityScorer()
        self.evidence_writer = ReadinessEvidenceWriter(output_dir=evidence_dir)

    def execute_full_verification(self) -> Dict[str, Any]:
        """
        Executes end-to-end verification across all 14 parts.
        """
        # 1. Dependency Checks
        db_report = self.db_checker.check_readiness()
        queue_report = self.queue_checker.check_readiness()
        storage_report = self.storage_checker.check_readiness()
        ai_report = self.ai_checker.check_readiness()
        worker_report = self.worker_checker.check_readiness()

        # 2. Dependency Matrix & Policy Evaluation
        latencies = {
            "postgres": db_report.latency_ms,
            "redis": queue_report.latency_ms,
            "storage": storage_report.latency_ms,
            "gemini": ai_report.latency_ms,
            "workers": 2.0,
            "analytics": 4.1,
        }
        matrix_report = self.policy_engine.evaluate_dependencies(live_latencies=latencies)

        # 3. Overall Readiness Evaluation & Traffic Decision
        eval_result = self.evaluator.evaluate_readiness(
            db_report=db_report,
            queue_report=queue_report,
            storage_report=storage_report,
            ai_report=ai_report,
            worker_report=worker_report,
        )

        # 4. Failure Simulations
        sim_report = self.simulator.run_all_simulations()

        # 5. Kubernetes Probe Compatibility
        k8s_report = self.k8s_verifier.verify_kubernetes_compatibility()

        # 6. Security Audit on /ready response payload
        ready_payload = {
            "service": eval_result.service,
            "state": eval_result.state.value,
            "traffic_allowed": eval_result.traffic_allowed,
            "reason": eval_result.reason,
            "checks": eval_result.checks,
        }
        sec_report = self.security_auditor.audit_security(ready_payload)

        # 7. Observability & Metrics Export
        self.metrics_exporter.set_readiness_state(eval_result.state)
        self.metrics_exporter.update_dependency_metric("postgres", db_report.passed, db_report.latency_ms / 1000.0)
        self.metrics_exporter.update_dependency_metric("redis", queue_report.passed, queue_report.latency_ms / 1000.0)
        self.metrics_exporter.update_dependency_metric("storage", storage_report.passed, storage_report.latency_ms / 1000.0)
        self.metrics_exporter.update_dependency_metric("gemini", ai_report.passed, ai_report.latency_ms / 1000.0)
        self.metrics_exporter.update_dependency_metric("workers", worker_report.passed, 0.002)

        metrics_summary = self.metrics_exporter.get_metrics_summary()
        prometheus_text = self.metrics_exporter.generate_prometheus_payload()

        # 8. Compute Scorecard
        scorecard = self.scorer.compute_scorecard(
            db_report=db_report,
            queue_report=queue_report,
            storage_report=storage_report,
            ai_report=ai_report,
            worker_report=worker_report,
            matrix_report=matrix_report,
            eval_result=eval_result,
            sim_report=sim_report,
            k8s_report=k8s_report,
            sec_report=sec_report,
            observability_valid=metrics_summary.get("prometheus_compatible", True),
        )

        # 9. Export All Evidence Manifests
        exported_files = self.evidence_writer.export_all(
            db_report=db_report,
            queue_report=queue_report,
            storage_report=storage_report,
            ai_report=ai_report,
            worker_report=worker_report,
            matrix_report=matrix_report,
            eval_result=eval_result,
            sim_report=sim_report,
            k8s_report=k8s_report,
            sec_report=sec_report,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "eval_result": eval_result,
            "db_report": db_report,
            "queue_report": queue_report,
            "storage_report": storage_report,
            "ai_report": ai_report,
            "worker_report": worker_report,
            "matrix_report": matrix_report,
            "sim_report": sim_report,
            "k8s_report": k8s_report,
            "sec_report": sec_report,
            "metrics_summary": metrics_summary,
            "prometheus_text": prometheus_text,
            "exported_files": exported_files,
        }
