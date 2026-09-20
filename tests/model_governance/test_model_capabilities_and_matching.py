"""Tests for Model Capabilities and Capability Matching Engine (Phase 8C)."""

import pytest
from app.model_governance.capabilities.registry import ModelCapability
from app.model_governance.capabilities.discovery import CapabilityMatchingEngine
from app.model_governance.registry.models import Model, ModelCategory, ModelProvider


def test_capability_matching_perfect_and_partial():
    matcher = CapabilityMatchingEngine()

    model_a = Model(
        model_id="gpt-4o",
        model_name="GPT-4o",
        organization_id="org_default",
        family_id="gpt-4o",
        version="2024-08-06",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.OPENAI,
        capabilities={
            ModelCapability.TEXT_GENERATION.value,
            ModelCapability.STRUCTURED_OUTPUT.value,
            ModelCapability.VISION.value,
            ModelCapability.FUNCTION_CALLING.value,
        },
    )

    model_b = Model(
        model_id="text-embedding-3-large",
        model_name="Embedding v3",
        organization_id="org_default",
        family_id="embed-3",
        version="1.0.0",
        category=ModelCategory.EMBEDDING,
        provider=ModelProvider.OPENAI,
        capabilities={ModelCapability.EMBEDDING.value},
    )

    # Search for vision + structured_output
    required = {ModelCapability.VISION.value, ModelCapability.STRUCTURED_OUTPUT.value}
    matches = matcher.filter_models_by_capabilities([model_a, model_b], required)
    assert len(matches) == 1
    assert matches[0].model_id == "gpt-4o"

    # Match score
    score_a = matcher.calculate_match_score(model_a, required)
    assert score_a == 1.0

    score_b = matcher.calculate_match_score(model_b, required)
    assert score_b == 0.0
