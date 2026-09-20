"""Model Lifecycle Manager (Phase 8C).

Enforces 9-state lifecycle finite state machine:
REGISTERED -> EVALUATING -> REVIEW -> APPROVED -> ACTIVE -> RESTRICTED -> DEPRECATED -> RETIRED -> ARCHIVED
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Union
from app.model_governance.registry.models import Model, ModelLifecycleState
from app.model_governance.lifecycle.states import ModelLifecycleAuditEvent
from app.model_governance.registry.repository import ModelRegistryRepository


class ModelLifecycleManager:
    """Manages AI model lifecycle state transitions and audit logging."""

    VALID_TRANSITIONS: Dict[ModelLifecycleState, Set[ModelLifecycleState]] = {
        ModelLifecycleState.REGISTERED: {ModelLifecycleState.EVALUATING, ModelLifecycleState.ARCHIVED},
        ModelLifecycleState.EVALUATING: {ModelLifecycleState.REVIEW, ModelLifecycleState.REGISTERED, ModelLifecycleState.ARCHIVED},
        ModelLifecycleState.REVIEW: {ModelLifecycleState.APPROVED, ModelLifecycleState.EVALUATING, ModelLifecycleState.ARCHIVED},
        ModelLifecycleState.APPROVED: {ModelLifecycleState.ACTIVE, ModelLifecycleState.ARCHIVED},
        ModelLifecycleState.ACTIVE: {ModelLifecycleState.RESTRICTED, ModelLifecycleState.DEPRECATED, ModelLifecycleState.RETIRED, ModelLifecycleState.ARCHIVED},
        ModelLifecycleState.RESTRICTED: {ModelLifecycleState.ACTIVE, ModelLifecycleState.DEPRECATED, ModelLifecycleState.RETIRED, ModelLifecycleState.ARCHIVED},
        ModelLifecycleState.DEPRECATED: {ModelLifecycleState.RETIRED, ModelLifecycleState.ARCHIVED},
        ModelLifecycleState.RETIRED: {ModelLifecycleState.ARCHIVED},
        ModelLifecycleState.ARCHIVED: set(),  # Terminal state
    }

    def __init__(self, repository: Optional[ModelRegistryRepository] = None):
        self.repository = repository
        self._audit_log: List[ModelLifecycleAuditEvent] = []

    def can_transition(self, current: ModelLifecycleState, target: ModelLifecycleState) -> bool:
        """Check if lifecycle transition is valid."""
        return target in self.VALID_TRANSITIONS.get(current, set())

    def transition(
        self,
        model: Optional[Union[Model, str]] = None,
        target_state: Optional[ModelLifecycleState] = None,
        actor: Optional[str] = None,
        actor_id: Optional[str] = None,
        reason: str = "State transition",
        organization_id: str = "org_default",
        model_id: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[Model, ModelLifecycleAuditEvent]:
        """Execute state transition with validation and audit logging."""
        effective_actor = actor or actor_id or kwargs.get("actor") or "system"
        effective_target = target_state or kwargs.get("to_state") or kwargs.get("target")

        target_model = model or model_id or kwargs.get("model_id")
        if target_model is None:
            raise ValueError("model or model_id must be provided")

        if isinstance(target_model, str):
            mid = target_model
            if not self.repository:
                raise ValueError("Repository required to resolve model by model_id")
            model_obj = self.repository.get_model(mid, organization_id)
            if not model_obj:
                raise KeyError(f"Model not found: {mid}")
        else:
            model_obj = target_model
            mid = model_obj.model_id
            organization_id = model_obj.organization_id

        curr_state = model_obj.status or model_obj.lifecycle_state
        if not self.can_transition(curr_state, effective_target):
            raise ValueError(
                f"Invalid lifecycle state transition from '{curr_state.value}' to '{effective_target.value}' for model '{mid}'"
            )

        event = ModelLifecycleAuditEvent(
            model_id=mid,
            organization_id=organization_id,
            from_state=curr_state,
            to_state=effective_target,
            actor_id=effective_actor,
            reason=reason,
        )
        self._audit_log.append(event)

        model_obj.status = effective_target
        model_obj.lifecycle_state = effective_target
        model_obj.updated_at = datetime.now(timezone.utc)

        if self.repository:
            self.repository.save_model(model_obj)

        if isinstance(target_model, str):
            return event
        return model_obj

    def get_audit_trail(self, model_id: str) -> List[ModelLifecycleAuditEvent]:
        """Get lifecycle transition audit history for a model."""
        return [e for e in self._audit_log if e.model_id == model_id]
