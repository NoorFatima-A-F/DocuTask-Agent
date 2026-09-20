"""Prompt Lifecycle State Transition Constraints & Rules (Phase 8D).

Enforces 10-state lifecycle FSM:
DRAFT -> VALIDATION -> TESTING -> REVIEW -> APPROVED -> PUBLISHED -> ACTIVE -> EXPERIMENTAL -> DEPRECATED -> ARCHIVED
"""

from __future__ import annotations

from typing import Dict, Set
from app.prompts.registry.models import PromptLifecycleState


PROMPT_LIFECYCLE_TRANSITIONS: Dict[PromptLifecycleState, Set[PromptLifecycleState]] = {
    PromptLifecycleState.DRAFT: {
        PromptLifecycleState.VALIDATION,
        PromptLifecycleState.ARCHIVED,
    },
    PromptLifecycleState.VALIDATION: {
        PromptLifecycleState.TESTING,
        PromptLifecycleState.DRAFT,
        PromptLifecycleState.ARCHIVED,
    },
    PromptLifecycleState.TESTING: {
        PromptLifecycleState.REVIEW,
        PromptLifecycleState.VALIDATION,
        PromptLifecycleState.DRAFT,
        PromptLifecycleState.ARCHIVED,
    },
    PromptLifecycleState.REVIEW: {
        PromptLifecycleState.APPROVED,
        PromptLifecycleState.TESTING,
        PromptLifecycleState.DRAFT,
        PromptLifecycleState.ARCHIVED,
    },
    PromptLifecycleState.APPROVED: {
        PromptLifecycleState.PUBLISHED,
        PromptLifecycleState.ARCHIVED,
    },
    PromptLifecycleState.PUBLISHED: {
        PromptLifecycleState.ACTIVE,
        PromptLifecycleState.EXPERIMENTAL,
        PromptLifecycleState.DEPRECATED,
        PromptLifecycleState.ARCHIVED,
    },
    PromptLifecycleState.ACTIVE: {
        PromptLifecycleState.EXPERIMENTAL,
        PromptLifecycleState.DEPRECATED,
        PromptLifecycleState.ARCHIVED,
    },
    PromptLifecycleState.EXPERIMENTAL: {
        PromptLifecycleState.ACTIVE,
        PromptLifecycleState.DEPRECATED,
        PromptLifecycleState.ARCHIVED,
    },
    PromptLifecycleState.DEPRECATED: {
        PromptLifecycleState.ARCHIVED,
    },
    PromptLifecycleState.ARCHIVED: set(),  # Terminal state
}


def is_valid_prompt_transition(
    current_state: PromptLifecycleState,
    target_state: PromptLifecycleState,
) -> bool:
    """Validate whether state transition is permitted by lifecycle FSM."""
    allowed = PROMPT_LIFECYCLE_TRANSITIONS.get(current_state, set())
    return target_state in allowed
