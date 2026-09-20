"""Prompt Governance Execution Decorators (Phase 8D).

Provides declarative python decorators allowing autonomous agents and workflow tasks
to resolve and execute approved prompts seamlessly.
"""

from __future__ import annotations

import functools
import inspect
from typing import Any, Callable, Dict, Optional
from app.prompts.sdk.client import PromptGovernanceSDK


def governed_prompt(
    prompt_id: str,
    sdk: Optional[PromptGovernanceSDK] = None,
    organization_id: str = "org_default",
    model_id: str = "gpt-4o",
):
    """Decorator wrapping model invocation functions with governed prompt resolution."""
    def decorator(fn: Callable[..., Any]):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            nonlocal sdk
            if sdk is None:
                sdk = PromptGovernanceSDK()

            variables = kwargs.get("variables", kwargs)

            def executor(rendered: str):
                sig = inspect.signature(fn)
                # If function only takes 1 argument (the rendered prompt)
                if len(sig.parameters) == 1:
                    return fn(rendered)
                return fn(rendered, *args, **kwargs)

            return sdk.execute_governed_prompt(
                prompt_id=prompt_id,
                organization_id=organization_id,
                variables=variables,
                model_executor=executor,
                model_id=model_id,
            )
        return wrapper
    return decorator
