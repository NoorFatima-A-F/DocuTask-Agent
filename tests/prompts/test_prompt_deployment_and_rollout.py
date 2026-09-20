"""Tests for Prompt Deployment, Canary Rollouts, and Automated Rollback (Phase 8D)."""

import pytest
from app.prompts.registry.repository import PromptRegistryRepository
from app.prompts.registry.service import PromptRegistryService
from app.prompts.registry.models import PromptApprovalStatus
from app.prompts.deployment.publisher import DeploymentEnvironment, PromptPublisher
from app.prompts.deployment.rollout import PromptRolloutManager
from app.prompts.deployment.rollback import AutomatedRollbackManager
from app.prompts.versions.rollback import PromptRollbackService


def test_prompt_deployment_and_canary_routing():
    repo = PromptRegistryRepository()
    service = PromptRegistryService(repo)
    publisher = PromptPublisher(repo)
    rollout_mgr = PromptRolloutManager(publisher)

    prompt, v1 = service.create_prompt(
        prompt_id="sentiment_agent",
        name="Sentiment Agent",
        organization_id="org_test",
        owner="ops@test.com",
        initial_template="Analyze sentiment: {{ text }}",
    )
    v2 = service.create_version(
        prompt_id="sentiment_agent",
        organization_id="org_test",
        prompt_template="Analyze sentiment into POS/NEG/NEU: {{ text }}",
        version_number="1.1.0",
        created_by="ops@test.com",
        change_reason="Add discrete labels",
    )

    # Approve v1
    v1.approval_status = PromptApprovalStatus.APPROVED
    repo.save_version("org_test", v1)

    # Deploy v1 to Production
    dep1 = publisher.deploy_version(
        prompt_id="sentiment_agent",
        version_id=v1.version_id,
        organization_id="org_test",
        environment=DeploymentEnvironment.PRODUCTION,
        deployed_by="ops_lead@test.com",
    )
    assert dep1.environment == DeploymentEnvironment.PRODUCTION

    # Set Canary: 20% to v2, 80% to v1
    rollout_mgr.set_canary_rollout(
        prompt_id="sentiment_agent",
        baseline_version_id=v1.version_id,
        canary_version_id=v2.version_id,
        organization_id="org_test",
        canary_traffic_pct=0.20,
    )

    resolved_versions = [
        rollout_mgr.resolve_version_for_execution("sentiment_agent", "org_test")
        for _ in range(100)
    ]
    assert v1.version_id in resolved_versions
    assert v2.version_id in resolved_versions


def test_automated_rollback_on_high_error_rate():
    repo = PromptRegistryRepository()
    service = PromptRegistryService(repo)
    publisher = PromptPublisher(repo)
    rollback_svc = PromptRollbackService(repo)
    auto_rollback = AutomatedRollbackManager(publisher, rollback_svc, error_rate_threshold=0.05)

    prompt, v1 = service.create_prompt(
        prompt_id="tax_calculator",
        name="Tax Calculator",
        organization_id="org_test",
        owner="finance@test.com",
        initial_template="Compute tax: {{ amount }}",
    )
    # Approve fallback version v1
    v1.approval_status = PromptApprovalStatus.APPROVED
    repo.save_version("org_test", v1)

    v2 = service.create_version(
        prompt_id="tax_calculator",
        organization_id="org_test",
        prompt_template="Compute tax broken: {{ amount }}",
        version_number="2.0.0",
        created_by="finance@test.com",
        change_reason="v2 release",
    )

    # Trigger auto-rollback because error rate was 12% (threshold 5%)
    was_rolled_back = auto_rollback.evaluate_and_rollback_if_degraded(
        prompt_id="tax_calculator",
        current_version_id=v2.version_id,
        fallback_version_id=v1.version_id,
        organization_id="org_test",
        observed_error_rate=0.12,
    )

    assert was_rolled_back is True
    updated_prompt = repo.get_prompt("tax_calculator", "org_test")
    assert updated_prompt.active_version_id == v1.version_id
