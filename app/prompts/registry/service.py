"""Prompt Registry Service (Phase 8D).

Provides unified interface for prompt asset creation, metadata lookup, version snapshotting,
and governed prompt discovery.
"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from app.prompts.registry.models import (
    Prompt,
    PromptCategory,
    PromptLifecycleState,
    PromptVersion,
    RiskLevel,
)
from app.prompts.registry.repository import PromptRegistryRepository


class PromptRegistryService:
    """Enterprise Prompt Registry management service."""

    def __init__(self, repository: Optional[PromptRegistryRepository] = None):
        self.repository = repository or PromptRegistryRepository()

    def create_prompt(
        self,
        prompt_id: str,
        name: str,
        organization_id: str,
        owner: str,
        category: PromptCategory = PromptCategory.TASK_PROMPT,
        description: str = "",
        purpose: str = "",
        department: str = "AI Engineering",
        risk_level: RiskLevel = RiskLevel.MEDIUM,
        initial_template: str = "",
        variables: Optional[List[str]] = None,
        tags: Optional[Set[str]] = None,
        allowed_models: Optional[List[str]] = None,
    ) -> tuple[Prompt, PromptVersion]:
        """Create new prompt definition and initial 1.0.0 draft version."""
        prompt = Prompt(
            prompt_id=prompt_id,
            name=name,
            description=description,
            purpose=purpose,
            category=category,
            organization_id=organization_id,
            owner=owner,
            department=department,
            risk_level=risk_level,
            status=PromptLifecycleState.DRAFT,
            lifecycle_state=PromptLifecycleState.DRAFT,
            current_version="1.0.0",
            tags=tags or set(),
            allowed_models=allowed_models or ["*"],
        )

        content_hash = hashlib.sha256(initial_template.encode("utf-8")).hexdigest()
        version_id = f"v_1_0_0_{uuid.uuid4().hex[:6]}"
        version = PromptVersion(
            version_id=version_id,
            prompt_id=prompt_id,
            version_number="1.0.0",
            content_hash=content_hash,
            prompt_template=initial_template,
            variables=variables or [],
            change_reason="Initial creation",
            created_by=owner,
        )

        prompt.active_version_id = version_id

        self.repository.save_prompt(prompt)
        self.repository.save_version(organization_id, version)
        return prompt, version

    def get_prompt(self, prompt_id: str, organization_id: str) -> Optional[Prompt]:
        """Retrieve prompt by ID."""
        return self.repository.get_prompt(prompt_id, organization_id)

    def list_prompts(
        self,
        organization_id: str,
        category: Optional[PromptCategory] = None,
        state: Optional[PromptLifecycleState] = None,
        tag: Optional[str] = None,
    ) -> List[Prompt]:
        """List prompts matching criteria."""
        return self.repository.list_prompts(
            organization_id=organization_id,
            category=category,
            state=state,
            tag=tag,
        )

    def create_version(
        self,
        prompt_id: str,
        organization_id: str,
        prompt_template: str,
        version_number: str,
        created_by: str,
        change_reason: str,
        variables: Optional[List[str]] = None,
        expected_output_schema: Optional[Dict[str, Any]] = None,
    ) -> PromptVersion:
        """Create a new immutable version for an existing prompt."""
        prompt = self.repository.get_prompt(prompt_id, organization_id)
        if not prompt:
            raise KeyError(f"Prompt not found: {prompt_id}")

        content_hash = hashlib.sha256(prompt_template.encode("utf-8")).hexdigest()
        version_id = f"v_{version_number.replace('.', '_')}_{uuid.uuid4().hex[:6]}"

        version = PromptVersion(
            version_id=version_id,
            prompt_id=prompt_id,
            version_number=version_number,
            content_hash=content_hash,
            prompt_template=prompt_template,
            variables=variables or [],
            expected_output_schema=expected_output_schema,
            change_reason=change_reason,
            created_by=created_by,
        )

        prompt.current_version = version_number
        prompt.updated_at = datetime.now(timezone.utc)
        self.repository.save_prompt(prompt)
        self.repository.save_version(organization_id, version)
        return version

    def get_version(
        self,
        prompt_id: str,
        version_id: str,
        organization_id: str,
    ) -> Optional[PromptVersion]:
        """Retrieve a specific version of a prompt."""
        return self.repository.get_version(prompt_id, version_id, organization_id)

    def list_versions(self, prompt_id: str, organization_id: str) -> List[PromptVersion]:
        """List all version history for a prompt."""
        return self.repository.list_versions(prompt_id, organization_id)
