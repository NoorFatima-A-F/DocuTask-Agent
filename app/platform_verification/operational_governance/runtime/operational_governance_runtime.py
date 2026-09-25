"""
Phase 3H.8: Enterprise Operational Governance Verification Runtime Orchestrator
"""
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from app.platform_verification.operational_governance.verifiers.change_governance_verifier import ChangeGovernanceVerifier
from app.platform_verification.operational_governance.verifiers.configuration_change_verifier import ConfigurationChangeVerifier
from app.platform_verification.operational_governance.verifiers.deployment_safety_verifier import DeploymentSafetyVerifier
from app.platform_verification.operational_governance.verifiers.database_change_verifier import DatabaseChangeVerifier
from app.platform_verification.operational_governance.verifiers.ai_model_change_verifier import AIModelChangeVerifier
from app.platform_verification.operational_governance.verifiers.approval_workflow_verifier import ApprovalWorkflowVerifier
from app.platform_verification.operational_governance.verifiers.rollback_verification_verifier import RollbackVerificationVerifier
from app.platform_verification.operational_governance.verifiers.audit_trail_verifier import AuditTrailVerifier
from app.platform_verification.operational_governance.verifiers.continuous_verification_verifier import ContinuousVerificationVerifier
from app.platform_verification.operational_governance.verifiers.governance_dashboard_verifier import GovernanceDashboardVerifier
from app.platform_verification.operational_governance.scoring.operational_governance_scorer import OperationalGovernanceScorer
from app.platform_verification.operational_governance.exporter.operational_governance_exporter import OperationalGovernanceExporter

logger = logging.getLogger("operational_governance.runtime")


class OperationalGovernanceRuntime:
    """
    Main runtime orchestrator for Phase 3H.8 Operational Governance Verification Framework.
    """

    def __init__(self, output_dir: Optional[Path] = None):
        self.change_verifier = ChangeGovernanceVerifier()
        self.config_verifier = ConfigurationChangeVerifier()
        self.deploy_verifier = DeploymentSafetyVerifier()
        self.db_verifier = DatabaseChangeVerifier()
        self.ai_verifier = AIModelChangeVerifier()
        self.approval_verifier = ApprovalWorkflowVerifier()
        self.rollback_verifier = RollbackVerificationVerifier()
        self.audit_verifier = AuditTrailVerifier()
        self.continuous_verifier = ContinuousVerificationVerifier()
        self.dashboard_verifier = GovernanceDashboardVerifier()
        self.scorer = OperationalGovernanceScorer()
        self.exporter = OperationalGovernanceExporter(output_dir=output_dir)

    def run_full_verification(self, export_evidence: bool = True) -> Dict[str, Any]:
        logger.info("Starting Phase 3H.8 Enterprise Operational Governance Verification Suite...")

        # 1. Execute all 10 Verifiers
        change_report = self.change_verifier.verify_change_governance()
        config_report = self.config_verifier.verify_configuration_changes()
        deploy_report = self.deploy_verifier.verify_deployment_safety()
        db_report = self.db_verifier.verify_database_changes()
        ai_report = self.ai_verifier.verify_ai_model_changes()
        approval_report = self.approval_verifier.verify_approval_workflows()
        rollback_report = self.rollback_verifier.verify_automated_rollbacks()
        audit_report = self.audit_verifier.verify_audit_trails()
        continuous_report = self.continuous_verifier.verify_continuous_operations()
        dashboard_report = self.dashboard_verifier.generate_governance_dashboard()

        # 2. Scorecard Calculation
        scorecard = self.scorer.calculate_scorecard(
            change_report=change_report,
            config_report=config_report,
            deploy_report=deploy_report,
            db_report=db_report,
            ai_report=ai_report,
            approval_report=approval_report,
            rollback_report=rollback_report,
            audit_report=audit_report,
            continuous_report=continuous_report,
            dashboard_report=dashboard_report,
        )

        export_metadata = None
        if export_evidence:
            export_metadata = self.exporter.export_all(
                change_report=change_report,
                config_report=config_report,
                deploy_report=deploy_report,
                db_report=db_report,
                ai_report=ai_report,
                approval_report=approval_report,
                rollback_report=rollback_report,
                audit_report=audit_report,
                continuous_report=continuous_report,
                dashboard_report=dashboard_report,
                scorecard=scorecard,
            )

        logger.info(
            f"Phase 3H.8 Verification Complete. Score: {scorecard.overall_governance_score}% "
            f"({scorecard.certification_tier.value}). Passed: {scorecard.passed}"
        )

        return {
            "scorecard": scorecard,
            "change_governance_report": change_report,
            "configuration_change_report": config_report,
            "deployment_safety_report": deploy_report,
            "database_change_report": db_report,
            "ai_model_change_report": ai_report,
            "approval_workflow_report": approval_report,
            "rollback_verification_report": rollback_report,
            "audit_trail_report": audit_report,
            "continuous_verification_report": continuous_report,
            "governance_dashboard_report": dashboard_report,
            "export_metadata": export_metadata,
        }
