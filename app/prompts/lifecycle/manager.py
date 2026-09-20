"""Prompt Lifecycle Manager (Phase 8D).

Enforces FSM transitions, state validations, and records immutable transition audits.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from app.prompts.registry.models import Prompt, PromptLifecycleState
from app.prompts.lifecycle.states import PromptLifecycleAuditEvent
from app.prompts.lifecycle.transitions import is_valid_prompt_transition
from app.prompts.registry.repository import PromptRegistryRepository


class PromptLifecycleManager:
    """Manages prompt state transitions and audit logging."""

    def __init__(self, repository: Optional[PromptRegistryRepository] = None):
        self.repository = repository
        self._audit_log: List[PromptLifecycleAuditEvent] = []

    def can_transition(
        self,
        current_state: PromptLifecycleState,
        target_state: PromptLifecycleState,
    ) -> bool:
        """Check if transition is permitted."""
        return is_valid_prompt_transition(current_state, target_state)

    def transition(
        self,
        prompt: Optional[Union[Prompt, str]] = None,
        target_state: Optional[PromptLifecycleState] = None,
        actor: str = "system",
        reason: str = "State transition",
        organization_id: str = "org_default",
        prompt_id: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[Prompt, PromptLifecycleAuditEvent]:
        """Execute validated state transition."""
        effective_target = target_state or kwargs.get("to_state") or kwargs.get("target")
        target_prompt = prompt or prompt_id or kwargs.get("prompt_id")

        if target_prompt is None or effective_target is None:
            raise ValueError("Prompt and target_state must be specified")

        if isinstance(target_prompt, str):
            pid = target_prompt
            if not self.repository:
                raise ValueError("Repository required to resolve prompt by prompt_id")
            prompt_obj = self.repository.get_prompt(pid, organization_id)
            if not prompt_obj:
                raise KeyError(f"Prompt not found: {pid}")
        else:
            prompt_obj = target_prompt
            pid = prompt_obj.prompt_id
            organization_id = prompt_obj.organization_id

        current = prompt_obj.lifecycle_state or prompt_obj.status
        if not self.can_transition(current, effective_target):
            raise ValueError(
                f"Invalid prompt lifecycle transition from '{current.value}' to '{effective_target.value}' for prompt '{pid}'"
            )

        event = PromptLifecycleAuditEvent(
            prompt_id=pid,
            organization_id=organization_id,
            from_state=current,
            to_state=effective_target,
            actor=actor,
            reason=reason,
        )
        self._audit_log.append(event)

        prompt_obj.status = effective_target
        prompt_obj.lifecycle_state = effective_target
        prompt_obj.updated_at = datetime.now(timezone.utc)

        if self.repository:
            self.repository.save_prompt(prompt_obj)

        if isinstance(target_prompt, str):
            return event
        return prompt_obj

    def get_audit_trail(self, prompt_id: str) -> List[PromptLifecycleAuditEvent]:
        """Get transition history for a prompt."""
        return [e for e in self._audit_log if e.prompt_id == prompt_id]
