"""Enterprise Model Governance Python SDK (Phase 8C).

Unified client interface for agents, workflows, and developers to register, query,
evaluate, select, and reproduce AI model invocations in compliance with enterprise governance.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Set
from app.model_governance.registry.models import (
    Model,
    ModelCategory,
    ModelLifecycleState,
    ModelProvider,
    RiskLevel,
)
from app.model_governance.registry.repository import ModelRegistryRepository
from app.model_governance.registry.service import ModelRegistryService
from app.model_governance.lifecycle.manager import ModelLifecycleManager
from app.model_governance.lifecycle.deprecation import ModelDeprecationManager, DeprecationPlan
from app.model_governance.approval.workflow import ModelApprovalWorkflowEngine
from app.model_governance.approval.approvals import StageStatus
from app.model_governance.selection.selector import (
    ModelSelectionRequest,
    ModelSelectionResult,
    ModelSelectionService,
)
from app.model_governance.selection.routing import ModelRouter, ModelInvocationRecord
from app.model_governance.evaluation.benchmarks import ModelBenchmarkDataset, ModelBenchmarkRunner
from app.model_governance.evaluation.scoring import ModelEvaluationScorer
from app.model_governance.risk.scoring import ModelRiskScorer
from app.model_governance.policies.enforcement import ModelPolicyEnforcer
from app.model_governance.reproducibility.snapshot import ReproducibilityService, ExecutionSnapshot
from app.model_governance.analytics.usage import ModelUsageTracker, UsageEvent
from app.model_governance.analytics.cost import ModelCostCalculator
from app.model_governance.analytics.performance import ModelPerformanceAnalyzer, PerformanceMetricSample


class ModelGovernanceSDK:
    """Master Developer SDK for Enterprise AI Model Governance."""

    def __init__(
        self,
        repository: Optional[ModelRegistryRepository] = None,
        policy_enforcer: Optional[ModelPolicyEnforcer] = None,
    ):
        self.repository = repository or ModelRegistryRepository()
        self.policy_enforcer = policy_enforcer or ModelPolicyEnforcer()
        self.registry = ModelRegistryService(self.repository)
        self.lifecycle = ModelLifecycleManager(self.repository)
        self.approval = ModelApprovalWorkflowEngine(self.repository, self.lifecycle)
        self.deprecation = ModelDeprecationManager(self.repository, self.lifecycle)
        self.selection = ModelSelectionService(self.repository, self.policy_enforcer)
        self.router = ModelRouter(self.repository, self.selection)
        self.eval_runner = ModelBenchmarkRunner()
        self.eval_scorer = ModelEvaluationScorer()
        self.risk_scorer = ModelRiskScorer()
        self.reproducibility = ReproducibilityService()
        self.usage = ModelUsageTracker()
        self.cost = ModelCostCalculator()
        self.performance = ModelPerformanceAnalyzer()

    # --- Model Registration & Discovery ---
    def register_model(self, model: Model) -> Model:
        res = self.registry.register_model(model)
        self.cost.register_model_pricing(model)
        return res

    def get_model(self, model_id: str, organization_id: str) -> Optional[Model]:
        return self.registry.get_model(model_id, organization_id)

    def list_models(
        self,
        organization_id: str,
        state: Optional[ModelLifecycleState] = None,
    ) -> List[Model]:
        return self.registry.list_models(organization_id=organization_id, status=state)

    # --- Lifecycle & Approvals ---
    def submit_for_approval(self, model_id: str, organization_id: str) -> Any:
        return self.approval.initiate_workflow(model_id, organization_id)

    def approve_stage(
        self,
        model_id: str,
        stage_name: str,
        reviewer: str,
        comments: Optional[str] = None,
        organization_id: str = "org_default",
    ) -> Any:
        return self.approval.review_stage(
            model_id=model_id,
            stage_name=stage_name,
            reviewer=reviewer,
            decision=StageStatus.APPROVED,
            comments=comments,
            organization_id=organization_id,
        )

    # --- Intelligent Selection & Routing ---
    def select_model(
        self,
        task_name: str,
        organization_id: str,
        required_capabilities: Optional[Set[str]] = None,
        max_input_cost_per_1k: Optional[float] = None,
        target_region: str = "us-east-1",
    ) -> ModelSelectionResult:
        req = ModelSelectionRequest(
            task_name=task_name,
            organization_id=organization_id,
            required_capabilities=required_capabilities or set(),
            max_input_cost_per_1k=max_input_cost_per_1k,
            target_region=target_region,
        )
        return self.selection.select_model(req)

    def execute_task(
        self,
        task_name: str,
        organization_id: str,
        executor_fn: Callable[[Model], Any],
        required_capabilities: Optional[Set[str]] = None,
    ) -> tuple[Any, ModelInvocationRecord]:
        req = ModelSelectionRequest(
            task_name=task_name,
            organization_id=organization_id,
            required_capabilities=required_capabilities or set(),
        )
        return self.router.execute_with_failover(req, executor_fn)

    # --- Reproducibility ---
    def capture_execution_snapshot(
        self,
        snapshot_id: str,
        organization_id: str,
        task_name: str,
        model: Model,
        prompt_text: str,
        system_prompt: str,
        input_data: Any,
        hyperparameters: Optional[Dict[str, Any]] = None,
    ) -> ExecutionSnapshot:
        return self.reproducibility.capture_snapshot(
            snapshot_id=snapshot_id,
            organization_id=organization_id,
            task_name=task_name,
            model_id=model.model_id,
            model_version=model.version,
            provider=model.provider.value if hasattr(model.provider, "value") else str(model.provider),
            prompt_text=prompt_text,
            system_prompt=system_prompt,
            input_data=input_data,
            hyperparameters=hyperparameters,
        )
