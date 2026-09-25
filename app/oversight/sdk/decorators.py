"""Human Oversight Function Decorators."""

import functools
import inspect
from typing import Callable, Optional

from ..core.context import OversightContext
from ..core.exceptions import ApprovalPolicyViolationError
from ..core.engine import HumanOversightEngine


def require_oversight(
    action_type: str = "EXECUTE",
    resource_type: str = "WORKFLOW",
    business_impact: str = "MEDIUM",
    tenant_id: str = "default_tenant",
    engine: Optional[HumanOversightEngine] = None,
):
    """
    Decorator that checks human oversight policies before executing a sensitive function.
    If policies mandate human review, it generates a review request and raises ApprovalPolicyViolationError
    or returns a review payload if configured.
    """
    active_engine = engine or HumanOversightEngine()

    def decorator(func: Callable):
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                ctx = kwargs.get("oversight_context")
                if not ctx or not isinstance(ctx, OversightContext):
                    ctx = OversightContext(
                        tenant_id=tenant_id,
                        action_type=action_type,
                        resource_type=resource_type,
                        business_impact=business_impact,
                    )

                requires_approval, policy, reason = active_engine.evaluate_context(ctx)
                if requires_approval:
                    review, _ = active_engine.create_review_request(
                        context=ctx,
                        title=f"Oversight Gate: {func.__name__}",
                        description=reason,
                    )
                    raise ApprovalPolicyViolationError(
                        f"Execution halted by Human Oversight Policy '{policy.name}': {reason}. Review ID: {review.review_id}"
                    )

                return await func(*args, **kwargs)
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                ctx = kwargs.get("oversight_context")
                if not ctx or not isinstance(ctx, OversightContext):
                    ctx = OversightContext(
                        tenant_id=tenant_id,
                        action_type=action_type,
                        resource_type=resource_type,
                        business_impact=business_impact,
                    )

                requires_approval, policy, reason = active_engine.evaluate_context(ctx)
                if requires_approval:
                    review, _ = active_engine.create_review_request(
                        context=ctx,
                        title=f"Oversight Gate: {func.__name__}",
                        description=reason,
                    )
                    raise ApprovalPolicyViolationError(
                        f"Execution halted by Human Oversight Policy '{policy.name}': {reason}. Review ID: {review.review_id}"
                    )

                return func(*args, **kwargs)
            return sync_wrapper

    return decorator
