"""Prompt Rollback Service (Phase 8D).

Enables instant, deterministic reversion to previous validated prompt releases.
"""

from __future__ import annotations

from app.prompts.registry.models import Prompt
from app.prompts.registry.repository import PromptRegistryRepository


class PromptRollbackService:
    """Safely restores prior production prompt versions in case of regressions."""

    def __init__(self, repository: PromptRegistryRepository):
        self.repository = repository

    def rollback(
        self,
        prompt_id: str,
        target_version_id: str,
        organization_id: str,
        actor: str = "system",
        reason: str = "Rollback triggered",
    ) -> Prompt:
        """Rolls back prompt's active release to target_version_id."""
        prompt = self.repository.get_prompt(prompt_id, organization_id)
        if not prompt:
            raise KeyError(f"Prompt not found: {prompt_id}")

        target_version = self.repository.get_version(prompt_id, target_version_id, organization_id)
        if not target_version:
            raise KeyError(f"Target version not found: {target_version_id}")

        prompt.active_version_id = target_version.version_id
        prompt.current_version = target_version.version_number
        prompt.metadata["last_rollback"] = {
            "to_version_id": target_version_id,
            "actor": actor,
            "reason": reason,
        }

        self.repository.save_prompt(prompt)
        return prompt
