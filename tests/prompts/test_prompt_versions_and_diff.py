"""Tests for Prompt Versioning, Immutability, and Diff Engine (Phase 8D)."""

import pytest
from app.prompts.registry.repository import PromptRegistryRepository
from app.prompts.registry.service import PromptRegistryService
from app.prompts.versions.diff import PromptDiffEngine
from app.prompts.versions.rollback import PromptRollbackService


def test_prompt_version_creation_and_diff():
    repo = PromptRegistryRepository()
    service = PromptRegistryService(repo)

    prompt, v1 = service.create_prompt(
        prompt_id="contract_analyzer",
        name="Contract Analyzer",
        organization_id="org_test",
        owner="legal_ai@enterprise.com",
        initial_template="Analyze contract text: {{ text }}.\nList all risks.",
        variables=["text"],
    )

    v2 = service.create_version(
        prompt_id="contract_analyzer",
        organization_id="org_test",
        prompt_template="Analyze contract text: {{ text }}.\nList all risks.\nFormat output as JSON: {{ format }}.",
        version_number="1.1.0",
        created_by="legal_ai@enterprise.com",
        change_reason="Added JSON format requirement",
        variables=["text", "format"],
    )

    assert v1.version_number == "1.0.0"
    assert v2.version_number == "1.1.0"
    assert v1.content_hash != v2.content_hash

    # Calculate structural and semantic diff
    diff_report = PromptDiffEngine.compare_versions(v1, v2)
    assert len(diff_report.added_lines) > 0
    assert "format" in diff_report.added_variables


def test_prompt_rollback_service():
    repo = PromptRegistryRepository()
    service = PromptRegistryService(repo)
    rollback_svc = PromptRollbackService(repo)

    prompt, v1 = service.create_prompt(
        prompt_id="po_matching",
        name="PO Matching",
        organization_id="org_test",
        owner="dev@test.com",
        initial_template="Match PO: {{ po_id }}",
    )

    v2 = service.create_version(
        prompt_id="po_matching",
        organization_id="org_test",
        prompt_template="Match PO with fuzzy logic: {{ po_id }}",
        version_number="1.2.0",
        created_by="dev@test.com",
        change_reason="Experimental fuzzy logic",
    )

    prompt.active_version_id = v2.version_id
    repo.save_prompt(prompt)
    assert prompt.active_version_id == v2.version_id

    # Rollback to v1
    rolled_back_prompt = rollback_svc.rollback(
        prompt_id="po_matching",
        target_version_id=v1.version_id,
        organization_id="org_test",
        reason="Fuzzy logic degraded precision",
    )

    assert rolled_back_prompt.active_version_id == v1.version_id
    assert rolled_back_prompt.current_version == "1.0.0"
