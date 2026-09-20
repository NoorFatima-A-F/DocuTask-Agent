"""Tests for Intelligent Model Selection and Failover Routing (Phase 8C)."""

import pytest
from app.model_governance.registry.models import (
    Model,
    ModelCategory,
    ModelLifecycleState,
    ModelProvider,
    RiskLevel,
)
from app.model_governance.registry.repository import ModelRegistryRepository
from app.model_governance.selection.selector import (
    ModelSelectionRequest,
    ModelSelectionService,
)
from app.model_governance.selection.routing import ModelRouter
from app.model_governance.policies.enforcement import ModelPolicyEnforcer


def test_intelligent_model_selection():
    repo = ModelRegistryRepository()
    enforcer = ModelPolicyEnforcer()
    service = ModelSelectionService(repo, enforcer)

    # Register fast model
    model_fast = Model(
        model_id="gpt-4o-mini",
        model_name="GPT-4o Mini",
        organization_id="org_test",
        family_id="gpt-4o",
        version="2024-07-18",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.OPENAI,
        lifecycle_state=ModelLifecycleState.ACTIVE,
        capabilities={"text_generation", "structured_output"},
        input_token_cost_per_1k=0.00015,
        risk_level=RiskLevel.LOW,
    )
    repo.save_model(model_fast)

    # Register powerful model
    model_heavy = Model(
        model_id="gpt-4o",
        model_name="GPT-4o",
        organization_id="org_test",
        family_id="gpt-4o",
        version="2024-08-06",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.OPENAI,
        lifecycle_state=ModelLifecycleState.ACTIVE,
        capabilities={"text_generation", "structured_output", "vision", "complex_reasoning"},
        input_token_cost_per_1k=0.0025,
        risk_level=RiskLevel.LOW,
    )
    repo.save_model(model_heavy)

    # Task requiring only basic extraction -> choose cheaper model
    req_simple = ModelSelectionRequest(
        task_name="invoice_key_value_extraction",
        organization_id="org_test",
        required_capabilities={"text_generation", "structured_output"},
    )
    res_simple = service.select_model(req_simple)
    assert res_simple.selected_model.model_id == "gpt-4o-mini"

    # Task requiring complex reasoning -> choose heavier model
    req_complex = ModelSelectionRequest(
        task_name="contract_risk_analysis",
        organization_id="org_test",
        required_capabilities={"text_generation", "complex_reasoning"},
    )
    res_complex = service.select_model(req_complex)
    assert res_complex.selected_model.model_id == "gpt-4o"


def test_model_failover_routing():
    repo = ModelRegistryRepository()
    service = ModelSelectionService(repo)
    router = ModelRouter(repo, service)

    m1 = Model(
        model_id="primary-llm",
        model_name="Primary LLM",
        organization_id="org_test",
        family_id="f1",
        version="v1",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.OPENAI,
        lifecycle_state=ModelLifecycleState.ACTIVE,
        capabilities={"text_generation"},
        input_token_cost_per_1k=0.001,
    )
    m2 = Model(
        model_id="secondary-llm",
        model_name="Secondary LLM",
        organization_id="org_test",
        family_id="f2",
        version="v1",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.GOOGLE,
        lifecycle_state=ModelLifecycleState.ACTIVE,
        capabilities={"text_generation"},
        input_token_cost_per_1k=0.002,
    )
    repo.save_model(m1)
    repo.save_model(m2)

    req = ModelSelectionRequest(
        task_name="text_summarization",
        organization_id="org_test",
        required_capabilities={"text_generation"},
    )

    # Primary model simulates outage, secondary succeeds
    def mock_executor(model: Model):
        if model.model_id == "primary-llm":
            raise ConnectionError("503 Service Unavailable")
        return f"Response from {model.model_id}"

    result, record = router.execute_with_failover(req, mock_executor)
    assert result == "Response from secondary-llm"
    assert record.status == "FAILOVER"
    assert "primary-llm" in record.failover_chain
    assert "secondary-llm" in record.failover_chain
