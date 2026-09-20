"""Master Synchronous Runtime Orchestrator for Phase 5 Autonomous Workflows."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from ..domain.interfaces import IAutonomousWorkflowVerificationRuntime
from ..domain.models import (
    AutonomousWorkflowQualityReport,
    VerificationStatus,
)
from ..exporter.workflow_quality_exporter import AutonomousWorkflowQualityExporter
from ..scoring.workflow_quality_scorer import AutonomousWorkflowQualityScorer
from ..verifiers import (
    AuditTrailValidationVerifier,
    AutonomousRecoveryVerifier,
    BusinessKPIVerifier,
    BusinessRuleEnforcementVerifier,
    BusinessValueVerifier,
    CompleteWorkflowExecutionVerifier,
    ComplianceValidationVerifier,
    CostValidationVerifier,
    DecisionQualityVerifier,
    EnterpriseDatasetVerifier,
    ExceptionWorkflowVerifier,
    ExecutiveReadinessVerifier,
    ExplainabilityValidationVerifier,
    HumanInTheLoopVerifier,
    LongRunningWorkflowVerifier,
    MultiAgentBusinessCollaborationVerifier,
    OrganizationalWorkflowVerifier,
    ScenarioLibraryVerifier,
    WorkflowOptimizationVerifier,
    WorkflowScalabilityVerifier,
)


class AutonomousWorkflowVerificationRuntime(IAutonomousWorkflowVerificationRuntime):
    """Executes all 20 business workflow verifiers, computes multi-pillar scores, and exports cryptographic evidence."""

    def __init__(
        self,
        scorer: Optional[AutonomousWorkflowQualityScorer] = None,
        exporter: Optional[AutonomousWorkflowQualityExporter] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.scorer = scorer or AutonomousWorkflowQualityScorer()
        self.exporter = exporter or AutonomousWorkflowQualityExporter()
        self.config = config or {}

        # 20 Verifiers
        self.verifiers = {
            "scenario_library": ScenarioLibraryVerifier(self.config),
            "complete_execution": CompleteWorkflowExecutionVerifier(self.config),
            "human_in_the_loop": HumanInTheLoopVerifier(self.config),
            "multi_agent_collaboration": MultiAgentBusinessCollaborationVerifier(self.config),
            "decision_quality": DecisionQualityVerifier(self.config),
            "business_rules": BusinessRuleEnforcementVerifier(self.config),
            "exception_workflow": ExceptionWorkflowVerifier(self.config),
            "business_kpi": BusinessKPIVerifier(self.config),
            "autonomous_recovery": AutonomousRecoveryVerifier(self.config),
            "organizational_workflow": OrganizationalWorkflowVerifier(self.config),
            "long_running": LongRunningWorkflowVerifier(self.config),
            "explainability": ExplainabilityValidationVerifier(self.config),
            "audit_trail": AuditTrailValidationVerifier(self.config),
            "compliance": ComplianceValidationVerifier(self.config),
            "cost_validation": CostValidationVerifier(self.config),
            "optimization": WorkflowOptimizationVerifier(self.config),
            "business_value": BusinessValueVerifier(self.config),
            "enterprise_dataset": EnterpriseDatasetVerifier(self.config),
            "scalability": WorkflowScalabilityVerifier(self.config),
            "executive_readiness": ExecutiveReadinessVerifier(self.config),
        }

    def execute_all(self, output_dir: Optional[str] = None) -> AutonomousWorkflowQualityReport:
        execution_id = f"EXEC-5-WF-{uuid.uuid4().hex[:8].upper()}"
        executed_reports: Dict[str, Any] = {}

        # Execute all 20 verifiers deterministically
        for key, verifier in self.verifiers.items():
            rep = verifier.verify()
            executed_reports[key] = rep

        # Calculate multi-pillar score
        score = self.scorer.calculate_score(executed_reports)

        overall_report = AutonomousWorkflowQualityReport(
            project_name="DocuTask Agent",
            phase="Phase 5 - Enterprise End-to-End Autonomous Workflow & Business Process Validation",
            execution_id=execution_id,
            status=score.verification_status,
            score=score,
            reports=executed_reports,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        # Export artifacts and generate summary
        self.exporter.export(overall_report, output_dir=output_dir)

        return overall_report
