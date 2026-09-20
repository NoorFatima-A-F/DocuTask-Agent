"""Prompt Registry Repository (Phase 8D).

Tenant-isolated persistent storage for Prompt entities and immutable PromptVersion records.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set
from app.prompts.registry.models import Prompt, PromptCategory, PromptLifecycleState, PromptVersion


class PromptRegistryRepository:
    """In-memory, tenant-isolated repository for prompts and prompt version snapshots."""

    def __init__(self):
        # org_id -> (prompt_id -> Prompt)
        self._prompts: Dict[str, Dict[str, Prompt]] = {}
        # (org_id, prompt_id) -> (version_id -> PromptVersion)
        self._versions: Dict[tuple[str, str], Dict[str, PromptVersion]] = {}

    def save_prompt(self, prompt: Prompt) -> Prompt:
        """Save or update prompt definition."""
        if prompt.organization_id not in self._prompts:
            self._prompts[prompt.organization_id] = {}
        self._prompts[prompt.organization_id][prompt.prompt_id] = prompt
        return prompt

    def get_prompt(self, prompt_id: str, organization_id: str) -> Optional[Prompt]:
        """Get prompt by ID ensuring tenant boundaries."""
        return self._prompts.get(organization_id, {}).get(prompt_id)

    def list_prompts(
        self,
        organization_id: str,
        category: Optional[PromptCategory] = None,
        state: Optional[PromptLifecycleState] = None,
        tag: Optional[str] = None,
    ) -> List[Prompt]:
        """List prompts with faceted filtering."""
        prompts = list(self._prompts.get(organization_id, {}).values())
        if category:
            prompts = [p for p in prompts if p.category == category]
        if state:
            prompts = [p for p in prompts if (p.lifecycle_state or p.status) == state]
        if tag:
            prompts = [p for p in prompts if tag in p.tags]
        return prompts

    def delete_prompt(self, prompt_id: str, organization_id: str) -> bool:
        """Delete prompt from registry."""
        if organization_id in self._prompts and prompt_id in self._prompts[organization_id]:
            del self._prompts[organization_id][prompt_id]
            self._versions.pop((organization_id, prompt_id), None)
            return True
        return False

    def save_version(self, organization_id: str, version: PromptVersion) -> PromptVersion:
        """Save an immutable prompt version."""
        key = (organization_id, version.prompt_id)
        if key not in self._versions:
            self._versions[key] = {}
        self._versions[key][version.version_id] = version
        return version

    def get_version(self, prompt_id: str, version_id: str, organization_id: str) -> Optional[PromptVersion]:
        """Get specific prompt version."""
        return self._versions.get((organization_id, prompt_id), {}).get(version_id)

    def list_versions(self, prompt_id: str, organization_id: str) -> List[PromptVersion]:
        """List all versions for a prompt sorted chronologically."""
        versions = list(self._versions.get((organization_id, prompt_id), {}).values())
        return sorted(versions, key=lambda v: v.created_at)
