"""Prompt Version Control Manager (Phase 8D).

Guarantees immutability of historical prompt releases and version lineage tracking.
"""

from __future__ import annotations

import hashlib
import uuid
from typing import Any, Dict, List, Optional
from app.prompts.registry.models import Prompt, PromptVersion
from app.prompts.registry.repository import PromptRegistryRepository


class PromptVersionManager:
    """Manages creation, retrieval, and promotion of immutable prompt versions."""

    def __init__(self, repository: PromptRegistryRepository):
        self.repository = repository

    def create_version(
        self,
        prompt_id: str,
        organization_id: str,
        template_text: str,
        version_number: str,
        author: str,
        change_reason: str,
        variables: Optional[List[str]] = None,
        model_compatibility: Optional[List[str]] = None,
        expected_output_schema: Optional[Dict[str, Any]] = None,
    ) -> PromptVersion:
        """Create and store an immutable version snapshot."""
        prompt = self.repository.get_prompt(prompt_id, organization_id)
        if not prompt:
            raise KeyError(f"Prompt not found: {prompt_id}")

        content_hash = hashlib.sha256(template_text.encode("utf-8")).hexdigest()
        version_id = f"v_{version_number.replace('.', '_')}_{uuid.uuid4().hex[:6]}"

        version = PromptVersion(
            version_id=version_id,
            prompt_id=prompt_id,
            version_number=version_number,
            content_hash=content_hash,
            prompt_template=template_text,
            variables=variables or [],
            model_compatibility=model_compatibility or ["*"],
            expected_output_schema=expected_output_schema,
            change_reason=change_reason,
            created_by=author,
        )

        self.repository.save_version(organization_id, version)
        return version

    def set_active_version(
        self,
        prompt_id: str,
        version_id: str,
        organization_id: str,
    ) -> Prompt:
        """Promote a specific version to be the active runtime version."""
        prompt = self.repository.get_prompt(prompt_id, organization_id)
        if not prompt:
            raise KeyError(f"Prompt not found: {prompt_id}")

        version = self.repository.get_version(prompt_id, version_id, organization_id)
        if not version:
            raise KeyError(f"Version not found: {version_id}")

        prompt.active_version_id = version_id
        prompt.current_version = version.version_number
        self.repository.save_prompt(prompt)
        return prompt
