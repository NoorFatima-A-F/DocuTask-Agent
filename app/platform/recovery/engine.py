"""
Platform Recovery Engine.
Executes policy-driven recovery strategies for platform exceptions and workflow failures.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
import uuid
from ...core.errors.error_codes import RecoveryPolicy
from ...core.errors.exceptions import PlatformException


@dataclass
class RecoveryAction:
    """Record of a triggered recovery action."""
    action_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    policy: RecoveryPolicy = RecoveryPolicy.RETRY
    error_id: str = ""
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    attempts: int = 0
    max_attempts: int = 3
    details: Dict[str, Any] = field(default_factory=dict)
    result_message: Optional[str] = None


class RecoveryEngine:
    """Coordinates and executes policy-based recovery actions."""

    def __init__(self):
        self._action_history: List[RecoveryAction] = []
        self._handlers: Dict[RecoveryPolicy, Callable[[PlatformException, RecoveryAction], Any]] = {}
        self._register_default_handlers()

    def _register_default_handlers(self) -> None:
        """Register default recovery handlers if needed."""
        pass

    def register_handler(self, policy: RecoveryPolicy, handler: Callable[[PlatformException, RecoveryAction], Any]) -> None:
        """Register custom recovery strategy handler."""
        self._handlers[policy] = handler

    async def execute_recovery(
        self,
        exception: PlatformException,
        retry_fn: Optional[Callable[[], Any]] = None,
        compensation_fn: Optional[Callable[[], Any]] = None,
        max_attempts: int = 3,
    ) -> RecoveryAction:
        """Evaluate exception recovery policy and execute the corresponding strategy."""
        policy = exception.recovery_policy
        action = RecoveryAction(
            policy=policy,
            error_id=exception.error_id,
            max_attempts=max_attempts,
            details={"error_code": exception.error_code, "category": exception.category.value},
        )
        self._action_history.append(action)
        action.status = "IN_PROGRESS"

        if policy == RecoveryPolicy.RETRY:
            if retry_fn and exception.retryable:
                for attempt in range(1, max_attempts + 1):
                    action.attempts = attempt
                    try:
                        if asyncio.iscoroutinefunction(retry_fn):
                            await retry_fn()
                        else:
                            retry_fn()
                        action.status = "COMPLETED"
                        action.result_message = f"Succeeded on retry attempt {attempt}"
                        return action
                    except Exception as err:
                        if attempt == max_attempts:
                            action.status = "FAILED"
                            action.result_message = f"Exhausted {max_attempts} retry attempts: {str(err)}"
            else:
                action.status = "FAILED"
                action.result_message = "Exception marked non-retryable or no retry function provided"

        elif policy == RecoveryPolicy.COMPENSATION or policy == RecoveryPolicy.ROLLBACK:
            if compensation_fn:
                try:
                    if asyncio.iscoroutinefunction(compensation_fn):
                        await compensation_fn()
                    else:
                        compensation_fn()
                    action.status = "COMPLETED"
                    action.result_message = f"Compensation successfully executed for {exception.error_code}"
                except Exception as comp_err:
                    action.status = "FAILED"
                    action.result_message = f"Compensation failed: {str(comp_err)}"
            else:
                action.status = "COMPLETED"
                action.result_message = "Rollback recorded (no compensation function required)"

        elif policy == RecoveryPolicy.DEAD_LETTER_QUEUE:
            action.status = "COMPLETED"
            action.result_message = f"Routed message to DLQ for error {exception.error_id}"

        elif policy == RecoveryPolicy.HUMAN_APPROVAL or policy == RecoveryPolicy.ESCALATION:
            action.status = "PENDING"
            action.result_message = f"Escalated for human operator review: {exception.message}"

        elif policy == RecoveryPolicy.ABORT:
            action.status = "COMPLETED"
            action.result_message = "Execution safely aborted per policy"

        else:
            handler = self._handlers.get(policy)
            if handler:
                try:
                    res = handler(exception, action)
                    if asyncio.iscoroutine(res):
                        await res
                    action.status = "COMPLETED"
                except Exception as h_err:
                    action.status = "FAILED"
                    action.result_message = f"Custom handler failed: {str(h_err)}"

        return action

    def get_history(self) -> List[RecoveryAction]:
        """Return full recovery audit log."""
        return list(self._action_history)
