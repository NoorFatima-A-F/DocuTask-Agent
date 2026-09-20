"""Tests for Model Registry and Metadata Management (Phase 8C)."""

import pytest
from app.model_governance.registry.models import (
    ApprovalStatus,
    DeploymentType,
    Model,
    ModelCategory,
    ModelLifecycleState,
    ModelProvider,
    RiskLevel,
)
from app.model_governance.registry.repository import ModelRegistryRepository
from app.model_governance.registry.service import ModelRegistryService
from app.model_governance.metadata.schemas import (
    ComprehensiveModelMetadata,
    ModelBusinessMetadata,
    ModelGovernanceMetadata,
    ModelTechnicalMetadata,
)
from app.model_governance.metadata.validators import ModelMetadataValidator


def test_model_registration_and_retrieval():
    repo = ModelRegistryRepository()
    service = ModelRegistryService(repo)

    model = Model(
        model_id="gpt-4o-gov",
        model_name="GPT-4o Enterprise",
        organization_id="org_test",
        family_id="gpt-4o",
        version="2024-08-06",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.OPENAI,
        deployment_type=DeploymentType.MANAGED_CLOUD,
        capabilities={"text_generation", "structured_output", "vision"},
        context_window=128000,
        max_output_tokens=4096,
        input_token_cost_per_1k=0.0025,
        output_token_cost_per_1k=0.010,
        risk_level=RiskLevel.LOW,
    )

    created = service.register_model(model)
    assert created.model_id == "gpt-4o-gov"
    assert created.lifecycle_state == ModelLifecycleState.REGISTERED

    fetched = service.get_model("gpt-4o-gov", "org_test")
    assert fetched is not None
    assert fetched.model_name == "GPT-4o Enterprise"
    assert "structured_output" in fetched.capabilities


def test_tenant_isolation_in_registry():
    repo = ModelRegistryRepository()
    service = ModelRegistryService(repo)

    m1 = Model(
        model_id="claude-3-5-sonnet",
        model_name="Claude Sonnet",
        organization_id="tenant_a",
        family_id="claude-3-5",
        version="2024-10-22",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.ANTHROPIC,
    )
    service.register_model(m1)

    assert service.get_model("claude-3-5-sonnet", "tenant_a") is not None
    assert service.get_model("claude-3-5-sonnet", "tenant_b") is None


def test_metadata_validation():
    metadata = ComprehensiveModelMetadata(
        technical=ModelTechnicalMetadata(
            architecture="Transformer",
            parameter_count_billion=175.0,
            context_window_tokens=128000,
        ),
        business=ModelBusinessMetadata(
            owner_email="mlops@docutask.internal",
            business_unit="Enterprise AI",
            cost_center="CC-904",
        ),
        governance=ModelGovernanceMetadata(
            data_residency_regions=["us-east-1", "eu-west-1"],
            gdpr_compliant=True,
            eu_ai_act_tier="General Purpose AI with Systemic Risk",
        ),
    )

    is_valid, errors = ModelMetadataValidator.validate(metadata)
    assert is_valid is True
    assert len(errors) == 0


def test_metadata_validation_failure():
    metadata = ComprehensiveModelMetadata(
        technical=ModelTechnicalMetadata(
            architecture="",
            context_window_tokens=-10,
        ),
        business=ModelBusinessMetadata(
            owner_email="invalid-email",
            business_unit="",
        ),
        governance=ModelGovernanceMetadata(
            data_residency_regions=[],
        ),
    )

    is_valid, errors = ModelMetadataValidator.validate(metadata)
    assert is_valid is False
    assert len(errors) >= 3
