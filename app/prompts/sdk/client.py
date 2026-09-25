"""Enterprise Prompt Governance SDK (Phase 8D).

Unified Python client interface for developers, autonomous agents, and workflow pipelines
to access governed, versioned, evaluated, and secured prompt assets.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Optional
from app.prompts.registry.models import (
    Prompt,
    PromptCategory,
    PromptVersion,
    RiskLevel,
)
from app.prompts.registry.repository import PromptRegistryRepository
from app.prompts.registry.service import PromptRegistryService
from app.prompts.lifecycle.manager import PromptLifecycleManager
from app.prompts.versions.versioning import PromptVersionManager
from app.prompts.versions.diff import PromptDiffEngine
from app.prompts.versions.rollback import PromptRollbackService
from app.prompts.templates.engine import PromptTemplateEngine
from app.prompts.approvals.workflow import ApprovalStageStatus, PromptApprovalWorkflowEngine
from app.prompts.evaluation.datasets import PromptEvaluationDataset
from app.prompts.evaluation.metrics import PromptEvaluationMetrics
from app.prompts.evaluation.runner import PromptEvaluationRunner
from app.prompts.testing.regression import PromptRegressionTester
from app.prompts.security.validation import PromptSecurityValidator
from app.prompts.deployment.publisher import DeploymentEnvironment, PromptDeploymentRecord, PromptPublisher
from app.prompts.deployment.rollout import PromptRolloutManager
from app.prompts.monitoring.analytics import PromptAnalyticsEngine
from app.prompts.monitoring.metrics import PromptExecutionEvent
from app.prompts.optimization.ab_testing import PromptABTestingService


class GovernedPromptExecutionResult:
    """Result container for governed prompt rendering and execution."""

    def __init__(
        self,
        prompt_id: str,
        version_id: str,
        rendered_prompt: str,
        output: Any,
        latency_ms: float,
        is_success: bool = True,
    ):
        self.prompt_id = prompt_id
        self.version_id = version_id
        self.rendered_prompt = rendered_prompt
        self.output = output
        self.latency_ms = latency_ms
        self.is_success = is_success


class PromptGovernanceSDK:
    """Master Developer SDK for Enterprise AI Prompt Governance."""

    def __init__(
        self,
        repository: Optional[PromptRegistryRepository] = None,
    ):
        self.repository = repository or PromptRegistryRepository()
        self.registry = PromptRegistryService(self.repository)
        self.lifecycle = PromptLifecycleManager(self.repository)
        self.versions = PromptVersionManager(self.repository)
        self.diff = PromptDiffEngine()
        self.rollback_service = PromptRollbackService(self.repository)
        self.template_engine = PromptTemplateEngine()
        self.approvals = PromptApprovalWorkflowEngine(self.repository, self.lifecycle)
        self.eval_runner = PromptEvaluationRunner()
        self.regression = PromptRegressionTester(self.eval_runner)
        self.security = PromptSecurityValidator()
        self.publisher = PromptPublisher(self.repository)
        self.rollout = PromptRolloutManager(self.publisher)
        self.analytics = PromptAnalyticsEngine()
        self.ab_testing = PromptABTestingService()

    # --- Prompt Registry & Management ---
    def create_prompt(
        self,
        prompt_id: str,
        name: str,
        organization_id: str,
        owner: str,
        category: PromptCategory = PromptCategory.TASK_PROMPT,
        description: str = "",
        initial_template: str = "",
        variables: Optional[List[str]] = None,
        risk_level: RiskLevel = RiskLevel.MEDIUM,
    ) -> tuple[Prompt, PromptVersion]:
        """Create new governed prompt and initial draft version."""
        # Security scan template first
        is_safe, violations = self.security.validate_security(initial_template)
        if not is_safe:
            raise ValueError(f"Prompt template contains security risks: {violations}")

        return self.registry.create_prompt(
            prompt_id=prompt_id,
            name=name,
            organization_id=organization_id,
            owner=owner,
            category=category,
            description=description,
            initial_template=initial_template,
            variables=variables,
            risk_level=risk_level,
        )

    def get_prompt(self, prompt_id: str, organization_id: str) -> Optional[Prompt]:
        """Fetch prompt definition."""
        return self.registry.get_prompt(prompt_id, organization_id)

    def create_version(
        self,
        prompt_id: str,
        organization_id: str,
        template_text: str,
        version_number: str,
        author: str,
        change_reason: str,
        variables: Optional[List[str]] = None,
    ) -> PromptVersion:
        """Create new immutable version snapshot."""
        is_safe, violations = self.security.validate_security(template_text)
        if not is_safe:
            raise ValueError(f"Prompt version template contains security risks: {violations}")

        return self.registry.create_version(
            prompt_id=prompt_id,
            organization_id=organization_id,
            prompt_template=template_text,
            version_number=version_number,
            created_by=author,
            change_reason=change_reason,
            variables=variables,
        )

    # --- Evaluation & Testing ---
    def evaluate_version(
        self,
        prompt_id: str,
        version_id: str,
        organization_id: str,
        dataset: PromptEvaluationDataset,
        inference_fn: Callable[[str], Any],
    ) -> PromptEvaluationMetrics:
        """Run benchmark evaluation on a prompt version."""
        version = self.registry.get_version(prompt_id, version_id, organization_id)
        if not version:
            raise KeyError(f"Prompt version not found: {version_id}")

        return self.eval_runner.evaluate_prompt(version, dataset, inference_fn)

    # --- Approvals & Promotion ---
    def submit_and_approve(
        self,
        prompt_id: str,
        version_id: str,
        organization_id: str,
        approver: str = "governance-lead@enterprise.com",
    ) -> Any:
        """Submit and approve all stages for a prompt version."""
        wf = self.approvals.initiate_workflow(prompt_id, version_id, organization_id)
        for stage in self.approvals.STAGE_NAMES:
            wf = self.approvals.review_stage(
                prompt_id=prompt_id,
                version_id=version_id,
                organization_id=organization_id,
                stage_name=stage,
                reviewer=approver,
                decision=ApprovalStageStatus.APPROVED,
            )
        return wf

    def deploy(
        self,
        prompt_id: str,
        version_id: str,
        organization_id: str,
        environment: DeploymentEnvironment = DeploymentEnvironment.PRODUCTION,
        deployed_by: str = "ops@enterprise.com",
    ) -> PromptDeploymentRecord:
        """Deploy approved prompt version to target environment."""
        return self.publisher.deploy_version(
            prompt_id=prompt_id,
            version_id=version_id,
            organization_id=organization_id,
            environment=environment,
            deployed_by=deployed_by,
        )

    # --- Governed Execution ---
    def render(
        self,
        prompt_id: str,
        organization_id: str,
        variables: Optional[Dict[str, Any]] = None,
        version_id: Optional[str] = None,
    ) -> str:
        """Render active or specified prompt template with dynamic variables."""
        prompt = self.registry.get_prompt(prompt_id, organization_id)
        if not prompt:
            raise KeyError(f"Prompt not found: {prompt_id}")

        target_vid = version_id or prompt.active_version_id
        if not target_vid:
            raise ValueError(f"No active version deployed for prompt {prompt_id}")

        version = self.registry.get_version(prompt_id, target_vid, organization_id)
        if not version:
            raise KeyError(f"Version not found: {target_vid}")

        return self.template_engine.render(
            template=version.prompt_template,
            variables=variables,
        )

    def execute_governed_prompt(
        self,
        prompt_id: str,
        organization_id: str,
        variables: Dict[str, Any],
        model_executor: Callable[[str], Any],
        model_id: str = "gpt-4o",
    ) -> GovernedPromptExecutionResult:
        """Render, execute via model, and record operational telemetry."""
        prompt = self.registry.get_prompt(prompt_id, organization_id)
        if not prompt:
            raise KeyError(f"Prompt not found: {prompt_id}")

        version_id = prompt.active_version_id or self.rollout.resolve_version_for_execution(prompt_id, organization_id)
        if not version_id:
            raise ValueError(f"No active version available for prompt {prompt_id}")

        rendered = self.render(
            prompt_id=prompt_id,
            organization_id=organization_id,
            variables=variables,
            version_id=version_id,
        )

        t0 = time.time()
        is_success = True
        err = None
        output = None

        try:
            output = model_executor(rendered)
        except Exception as e:
            is_success = False
            err = str(e)
            raise e
        finally:
            latency = (time.time() - t0) * 1000.0
            event = PromptExecutionEvent(
                event_id=f"evt_p_{int(time.time()*1000)}",
                prompt_id=prompt_id,
                version_id=version_id,
                organization_id=organization_id,
                model_id=model_id,
                prompt_tokens=len(rendered) // 4,
                completion_tokens=len(str(output)) // 4 if output else 0,
                latency_ms=latency,
                cost_usd=0.0001,
                is_success=is_success,
                error_type=err,
            )
            self.analytics.record_event(event)

        return GovernedPromptExecutionResult(
            prompt_id=prompt_id,
            version_id=version_id,
            rendered_prompt=rendered,
            output=output,
            latency_ms=latency,
            is_success=is_success,
        )
