"""
Disaster Recovery Governance Runtime Engine (Part 3G.4).
Master orchestrator that executes all governance verification subsystems,
evaluates continuous resilience metrics, calculates composite scorecard,
and triggers automatic artifact export.
"""
from dataclasses import dataclass
from typing import Dict, Any

from app.platform_verification.resilience_governance.domain.models import (
    OwnershipValidationReport,
    PolicyValidationReport,
    RecoveryChangeImpactReport,
    DocumentationDriftReport,
    ResilienceMaturityScore,
    PostmortemSectionReport,
    ContinuousResilienceMetricsReport,
    GovernanceScorecard,
)
from app.platform_verification.resilience_governance.ownership.ownership_validator import (
    OwnershipValidator,
)
from app.platform_verification.resilience_governance.policies.policy_manager import (
    PolicyManager,
)
from app.platform_verification.resilience_governance.change_impact.change_impact_analyzer import (
    ChangeImpactAnalyzer,
)
from app.platform_verification.resilience_governance.drift_detection.doc_drift_detector import (
    DocumentationDriftDetector,
)
from app.platform_verification.resilience_governance.maturity.maturity_assessment_engine import (
    MaturityAssessmentEngine,
)
from app.platform_verification.resilience_governance.incidents.incident_lifecycle_verifier import (
    IncidentLifecycleVerifier,
)
from app.platform_verification.resilience_governance.metrics.continuous_resilience_metrics import (
    ContinuousResilienceMetricsEngine,
)
from app.platform_verification.resilience_governance.risk.resilience_risk_manager import (
    ResilienceRiskManager,
    ResilienceRiskReport,
)
from app.platform_verification.resilience_governance.compliance_audit.audit_package_generator import (
    ComplianceAuditPackageGenerator,
    AuditPackageManifest,
)
from app.platform_verification.resilience_governance.review_pipeline.scheduled_review_engine import (
    ScheduledReviewEngine,
    CICDResilienceGateResult,
)
from app.platform_verification.resilience_governance.exporter.governance_exporter import (
    GovernanceExporter,
)


@dataclass
class MasterGovernanceExecutionResult:
    ownership_report: OwnershipValidationReport
    policy_report: PolicyValidationReport
    change_impact_report: RecoveryChangeImpactReport
    drift_report: DocumentationDriftReport
    postmortem_report: PostmortemSectionReport
    metrics_report: ContinuousResilienceMetricsReport
    risk_report: ResilienceRiskReport
    maturity_score: ResilienceMaturityScore
    audit_manifest: AuditPackageManifest
    cicd_gate_result: CICDResilienceGateResult
    scorecard: GovernanceScorecard
    export_result: Dict[str, Any]
    passed: bool


class GovernanceRuntime:
    """
    Master runtime for Part 3G.4 Disaster Recovery Governance & Continuous Resilience.
    """

    def __init__(
        self,
        base_dir: str = ".",
        gov_dir_name: str = "resilience_governance",
        audit_dir_name: str = "audit_package",
        cert_dir_name: str = "resilience_certification",
    ):
        self.base_dir = base_dir
        self.ownership_validator = OwnershipValidator()
        self.policy_manager = PolicyManager()
        self.change_impact_analyzer = ChangeImpactAnalyzer()
        self.drift_detector = DocumentationDriftDetector()
        self.maturity_engine = MaturityAssessmentEngine()
        self.incident_verifier = IncidentLifecycleVerifier()
        self.metrics_engine = ContinuousResilienceMetricsEngine()
        self.risk_manager = ResilienceRiskManager()
        self.audit_generator = ComplianceAuditPackageGenerator()
        self.review_engine = ScheduledReviewEngine()
        self.exporter = GovernanceExporter(
            base_dir=base_dir,
            gov_dir_name=gov_dir_name,
            audit_dir_name=audit_dir_name,
            cert_dir_name=cert_dir_name,
        )

    def execute_governance_verification(self, export_artifacts: bool = True) -> MasterGovernanceExecutionResult:
        """
        Runs the full disaster recovery governance verification lifecycle.
        """
        # 1. Ownership validation
        ownership_report = self.ownership_validator.validate_ownership()

        # 2. Policy validation
        policy_report = self.policy_manager.validate_policies()

        # 3. Change impact analysis
        change_impact_report = self.change_impact_analyzer.analyze_change_impact()

        # 4. Documentation drift detection
        drift_report = self.drift_detector.detect_documentation_drift()

        # 5. Incident lifecycle & postmortems
        postmortem_report = self.incident_verifier.verify_incident_lifecycle()

        # 6. Continuous resilience metrics
        metrics_report = self.metrics_engine.calculate_resilience_metrics()

        # 7. Risk assessment
        risk_report = self.risk_manager.assess_risk_posture()

        # 8. Maturity assessment
        maturity_score = self.maturity_engine.assess_maturity(
            ownership=ownership_report,
            policies=policy_report,
            drift=drift_report,
            postmortem=postmortem_report,
            metrics=metrics_report,
        )

        # 9. Compliance audit evaluation
        audit_manifest = self.audit_generator.evaluate_compliance()

        # 10. CI/CD Resilience Gate evaluation
        cicd_gate = self.review_engine.evaluate_cicd_resilience_gate(
            ownership_report=ownership_report,
            policy_report=policy_report,
            change_impact_report=change_impact_report,
            drift_report=drift_report,
            maturity_score=maturity_score,
            metrics_report=metrics_report,
        )

        # 11. Calculate Scorecard
        ownership_score = 100.0 if ownership_report.passed else 0.0
        policy_score = 100.0 if policy_report.passed else 0.0
        change_drift_score = 100.0 if (change_impact_report.passed and drift_report.passed) else 50.0
        maturity_pts = maturity_score.maturity_score
        incident_pts = postmortem_report.postmortem_quality_score
        audit_pts = audit_manifest.overall_compliance_pct

        # Weights: ownership 20%, policies 15%, change/drift 20%, maturity 20%, incidents 15%, audit 10%
        composite = (
            ownership_score * 0.20
            + policy_score * 0.15
            + change_drift_score * 0.20
            + maturity_pts * 0.20
            + incident_pts * 0.15
            + audit_pts * 0.10
        )
        composite = round(composite, 2)

        passed = (
            composite >= 95.0
            and ownership_report.passed
            and policy_report.passed
            and change_impact_report.passed
            and drift_report.passed
            and postmortem_report.passed
            and metrics_report.passed
            and risk_report.passed
            and maturity_score.passed
            and cicd_gate.gate_passed
        )

        cert_status = "ENTERPRISE_CERTIFIED" if passed else "CERTIFICATION_REJECTED"

        scorecard = GovernanceScorecard(
            ownership_score=ownership_score,
            policy_governance_score=policy_score,
            change_drift_score=change_drift_score,
            maturity_score=maturity_pts,
            incident_learning_score=incident_pts,
            audit_readiness_score=audit_pts,
            overall_governance_score=composite,
            certification_status=cert_status,
            ci_cd_deployment_approved=cicd_gate.deployment_approved,
            passed=passed,
            evaluation_metadata={
                "maturity_tier": maturity_score.maturity_level.value,
                "components_owned": f"{ownership_report.owned_components}/{ownership_report.total_components}",
                "policies_enforced": f"{policy_report.policies_evaluated}/{policy_report.policies_evaluated}",
                "compliance_score": f"{audit_manifest.overall_compliance_pct}%",
            },
        )

        # 12. Export Artifacts
        export_result = {}
        if export_artifacts:
            export_result = self.exporter.export_all(
                ownership_report=ownership_report,
                policy_report=policy_report,
                change_impact_report=change_impact_report,
                drift_report=drift_report,
                maturity_score=maturity_score,
                postmortem_report=postmortem_report,
                metrics_report=metrics_report,
                risk_report=risk_report,
                scorecard=scorecard,
            )

        return MasterGovernanceExecutionResult(
            ownership_report=ownership_report,
            policy_report=policy_report,
            change_impact_report=change_impact_report,
            drift_report=drift_report,
            postmortem_report=postmortem_report,
            metrics_report=metrics_report,
            risk_report=risk_report,
            maturity_score=maturity_score,
            audit_manifest=audit_manifest,
            cicd_gate_result=cicd_gate,
            scorecard=scorecard,
            export_result=export_result,
            passed=passed,
        )
