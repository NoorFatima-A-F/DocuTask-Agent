"""Master Synchronous Runtime Orchestrator for Phase 4 Cross-System Integration."""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from ..domain.interfaces import ICrossSystemIntegrationVerificationRuntime
from ..domain.models import (
    CrossSystemIntegrationQualityReport,
)
from ..exporter.integration_quality_exporter import CrossSystemIntegrationQualityExporter
from ..scoring.integration_quality_scorer import CrossSystemIntegrationQualityScorer
from ..verifiers import (
    AgentCollaborationVerifier,
    APIChainVerifier,
    CognitiveIntegrationVerifier,
    CrossSystemPerformanceVerifier,
    DataIntegrityVerifier,
    DependencyMappingVerifier,
    DeploymentIntegrationVerifier,
    EnterpriseWorkflowsVerifier,
    EventBusVerifier,
    EvidenceGenerationVerifier,
    FailurePropagationVerifier,
    IntegrationRegressionVerifier,
    InterfaceContractVerifier,
    KnowledgeFlowVerifier,
    LifecycleIntegrationVerifier,
    MarketplaceValidationVerifier,
    MemoryInteractionVerifier,
    ObservabilityIntegrationVerifier,
    PlanningPipelineVerifier,
    SchedulerVerifier,
    SecurityBoundaryVerifier,
    StatePropagationVerifier,
)


class CrossSystemIntegrationVerificationRuntime(ICrossSystemIntegrationVerificationRuntime):
    """Executes all 22 cross-system verifiers, computes multi-pillar scores, and exports cryptographic evidence."""

    def __init__(
        self,
        scorer: Optional[CrossSystemIntegrationQualityScorer] = None,
        exporter: Optional[CrossSystemIntegrationQualityExporter] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.scorer = scorer or CrossSystemIntegrationQualityScorer()
        self.exporter = exporter or CrossSystemIntegrationQualityExporter()
        self.config = config or {}

        # 22 Verifiers
        self.verifiers = {
            "dependency_mapping": DependencyMappingVerifier(self.config),
            "interface_contract": InterfaceContractVerifier(self.config),
            "api_chain": APIChainVerifier(self.config),
            "state_propagation": StatePropagationVerifier(self.config),
            "knowledge_flow": KnowledgeFlowVerifier(self.config),
            "memory_interaction": MemoryInteractionVerifier(self.config),
            "planning_pipeline": PlanningPipelineVerifier(self.config),
            "agent_collaboration": AgentCollaborationVerifier(self.config),
            "cognitive_integration": CognitiveIntegrationVerifier(self.config),
            "security_boundary": SecurityBoundaryVerifier(self.config),
            "lifecycle_integration": LifecycleIntegrationVerifier(self.config),
            "deployment_integration": DeploymentIntegrationVerifier(self.config),
            "marketplace_validation": MarketplaceValidationVerifier(self.config),
            "event_bus": EventBusVerifier(self.config),
            "scheduler": SchedulerVerifier(self.config),
            "observability_integration": ObservabilityIntegrationVerifier(self.config),
            "data_integrity": DataIntegrityVerifier(self.config),
            "failure_propagation": FailurePropagationVerifier(self.config),
            "cross_system_performance": CrossSystemPerformanceVerifier(self.config),
            "enterprise_workflows": EnterpriseWorkflowsVerifier(self.config),
            "integration_regression": IntegrationRegressionVerifier(self.config),
            "evidence_generation": EvidenceGenerationVerifier(self.config),
        }

    def execute_all(self, output_dir: Optional[str] = None) -> CrossSystemIntegrationQualityReport:
        execution_id = f"EXEC-4-INT-{uuid.uuid4().hex[:8].upper()}"
        executed_reports: Dict[str, Any] = {}

        # Execute all 22 verifiers deterministically
        for key, verifier in self.verifiers.items():
            rep = verifier.verify()
            executed_reports[key] = rep

        # Calculate multi-pillar score
        score = self.scorer.calculate_score(executed_reports)

        overall_report = CrossSystemIntegrationQualityReport(
            project_name="DocuTask Agent",
            phase="Phase 4 - Enterprise Cross-System Integration & End-to-End Platform Validation",
            execution_id=execution_id,
            status=score.verification_status,
            score=score,
            reports=executed_reports,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        # Export artifacts and generate summary
        self.exporter.export(overall_report, output_dir=output_dir)

        return overall_report
