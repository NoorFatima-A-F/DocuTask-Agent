"""Master Runtime Coordinator for Phase 3H.4.3 Autonomous Health Remediation Framework."""

from typing import Dict, Any
from ..policies.remediation_policy_engine import RemediationPolicyEngine
from ..classifier.action_classifier import ActionClassifier
from ..planner.recovery_decision_engine import RecoveryDecisionEngine
from ..safety.safety_guard import SafetyGuard
from ..executor.remediation_executor import RemediationExecutor
from ..validators.recovery_validator import RecoveryValidator
from ..rollback.rollback_manager import RollbackManager
from ..scenarios.self_healing_scenarios_verifier import SelfHealingScenariosVerifier
from ..metrics.remediation_metrics_collector import RemediationMetricsCollector
from ..security.remediation_permissions import RemediationPermissionsAuditor
from ..observability.remediation_telemetry_emitter import RemediationTelemetryEmitter
from ..scoring.remediation_quality_scorer import AutonomousRemediationScorer
from ..exporter.remediation_evidence_exporter import RemediationEvidenceExporter
from ..domain.models import FailureContext


class AutonomousRemediationRuntime:
    """Master orchestrator executing the 14-part autonomous remediation and recovery verification pipeline."""

    def __init__(self, export_dir: str = "health_remediation_verification"):
        self.policy_engine = RemediationPolicyEngine()
        self.classifier = ActionClassifier()
        self.decision_engine = RecoveryDecisionEngine(
            policy_engine=self.policy_engine,
            classifier=self.classifier,
        )
        self.safety_guard = SafetyGuard()
        self.executor = RemediationExecutor()
        self.validator = RecoveryValidator()
        self.rollback_mgr = RollbackManager()
        self.scenarios_verifier = SelfHealingScenariosVerifier()
        self.metrics_collector = RemediationMetricsCollector()
        self.security_auditor = RemediationPermissionsAuditor()
        self.telemetry_emitter = RemediationTelemetryEmitter()
        self.scorer = AutonomousRemediationScorer()
        self.exporter = RemediationEvidenceExporter(export_dir=export_dir)

    def trigger_remediation_pipeline(self, context: FailureContext) -> Dict[str, Any]:
        """Executes full autonomous self-healing lifecycle for a specific detected failure."""
        decision = self.decision_engine.make_decision(context)
        safety_result = self.safety_guard.validate_safety(decision)

        if not safety_result.safe_to_execute:
            return {
                "decision": decision,
                "safety": safety_result,
                "executed": False,
                "status": "BLOCKED_BY_SAFETY",
            }

        self.safety_guard.register_execution_attempt(decision.parameters.get("target", "system"))
        execution_entry = self.executor.execute_remediation(decision)
        val_report = self.validator.validate_recovery(execution_entry)

        return {
            "decision": decision,
            "safety": safety_result,
            "execution": execution_entry,
            "validation_report": val_report,
            "status": "COMPLETED",
        }

    def run_full_verification(self) -> Dict[str, Any]:
        """Runs full autonomous remediation verification across all 14 dimensions and exports manifests."""
        policy_rep = self.policy_engine.get_policy_report()
        exec_rep = self.executor.get_execution_report()
        val_rep = self.validator.get_validation_report()
        roll_rep = self.rollback_mgr.get_rollback_report()
        scen_rep = self.scenarios_verifier.verify_scenarios()
        metrics_rep = self.metrics_collector.collect_metrics()
        sec_rep = self.security_auditor.audit_security()

        scorecard = self.scorer.score_remediation(
            policy_rep=policy_rep,
            exec_rep=exec_rep,
            val_rep=val_rep,
            roll_rep=roll_rep,
            scen_rep=scen_rep,
            metrics_rep=metrics_rep,
            sec_rep=sec_rep,
        )

        manifests = self.exporter.export_all(
            policy_rep=policy_rep,
            exec_rep=exec_rep,
            val_rep=val_rep,
            roll_rep=roll_rep,
            scen_rep=scen_rep,
            metrics_rep=metrics_rep,
            sec_rep=sec_rep,
            scorecard=scorecard,
        )

        return {
            "policy_report": policy_rep,
            "execution_report": exec_rep,
            "validation_report": val_rep,
            "rollback_report": roll_rep,
            "scenarios_report": scen_rep,
            "metrics_report": metrics_rep,
            "security_report": sec_rep,
            "scorecard": scorecard,
            "exported_manifests": manifests,
        }
