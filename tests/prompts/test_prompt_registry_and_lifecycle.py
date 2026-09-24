"""Tests for Prompt Registry, Domain Models, and 10-State Lifecycle FSM (Phase 8D)."""

import pytest
from app.prompts.registry.models import (
    PromptCategory,
    PromptLifecycleState,
    RiskLevel,
)
from app.prompts.registry.repository import PromptRegistryRepository
from app.prompts.registry.service import PromptRegistryService
from app.prompts.lifecycle.manager import PromptLifecycleManager


def test_prompt_registration_and_retrieval():
    repo = PromptRegistryRepository()
    service = PromptRegistryService(repo)

    prompt, version = service.create_prompt(
        prompt_id="invoice_parser_v1",
        name="Enterprise Invoice Extraction Prompt",
        organization_id="org_test",
        owner="lead_ai@enterprise.com",
        category=PromptCategory.EXTRACTION_PROMPT,
        description="Extracts line items, vendor details, and amounts",
        initial_template="Extract key-value pairs from {{ document_text }}.",
        variables=["document_text"],
        risk_level=RiskLevel.MEDIUM,
    )

    assert prompt.prompt_id == "invoice_parser_v1"
    assert prompt.status == PromptLifecycleState.DRAFT
    assert prompt.active_version_id == version.version_id
    assert version.version_number == "1.0.0"

    fetched = service.get_prompt("invoice_parser_v1", "org_test")
    assert fetched is not None
    assert fetched.name == "Enterprise Invoice Extraction Prompt"


def test_tenant_isolation_in_prompts():
    repo = PromptRegistryRepository()
    service = PromptRegistryService(repo)

    service.create_prompt(
        prompt_id="doc_summary",
        name="Doc Summary A",
        organization_id="tenant_a",
        owner="dev@a.com",
        initial_template="Summarize {{ text }}",
    )

    assert service.get_prompt("doc_summary", "tenant_a") is not None
    assert service.get_prompt("doc_summary", "tenant_b") is None


def test_prompt_lifecycle_valid_and_invalid_transitions():
    repo = PromptRegistryRepository()
    service = PromptRegistryService(repo)
    lifecycle = PromptLifecycleManager(repo)

    prompt, _ = service.create_prompt(
        prompt_id="fsm_test_prompt",
        name="FSM Test Prompt",
        organization_id="org_test",
        owner="dev@test.com",
        initial_template="Hello {{ name }}",
    )

    # Valid: DRAFT -> VALIDATION -> TESTING -> REVIEW -> APPROVED -> PUBLISHED -> ACTIVE
    lifecycle.transition(prompt, target_state=PromptLifecycleState.VALIDATION)
    assert prompt.lifecycle_state == PromptLifecycleState.VALIDATION

    lifecycle.transition(prompt, target_state=PromptLifecycleState.TESTING)
    assert prompt.lifecycle_state == PromptLifecycleState.TESTING

    lifecycle.transition(prompt, target_state=PromptLifecycleState.REVIEW)
    assert prompt.lifecycle_state == PromptLifecycleState.REVIEW

    lifecycle.transition(prompt, target_state=PromptLifecycleState.APPROVED)
    assert prompt.lifecycle_state == PromptLifecycleState.APPROVED

    lifecycle.transition(prompt, target_state=PromptLifecycleState.PUBLISHED)
    assert prompt.lifecycle_state == PromptLifecycleState.PUBLISHED

    lifecycle.transition(prompt, target_state=PromptLifecycleState.ACTIVE)
    assert prompt.lifecycle_state == PromptLifecycleState.ACTIVE

    # Invalid: ACTIVE directly to DRAFT
    with pytest.raises(ValueError, match="Invalid prompt lifecycle transition"):
        lifecycle.transition(prompt, target_state=PromptLifecycleState.DRAFT)
