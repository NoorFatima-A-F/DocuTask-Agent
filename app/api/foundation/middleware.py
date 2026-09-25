"""
Platform API Middleware & Exception Handlers.
"""

from typing import Any, Dict
from .request_context import RequestContext
from ...core.errors.exceptions import PlatformException
from ...core.errors.problem_details import ProblemDetails
from ...infrastructure.logging.logger import (
    ctx_org_id,
    ctx_request_id,
    ctx_trace_id,
)


class RequestContextExtractor:
    """Extracts standard RequestContext from raw headers."""

    @staticmethod
    def extract_from_headers(headers: Dict[str, str]) -> RequestContext:
        req_id = headers.get("x-request-id") or headers.get("X-Request-ID")
        corr_id = headers.get("x-correlation-id") or headers.get("X-Correlation-ID")
        org_id = headers.get("x-organization-id") or headers.get("X-Organization-ID")
        workspace_id = headers.get("x-workspace-id") or headers.get("X-Workspace-ID")
        env_id = headers.get("x-environment-id") or headers.get("X-Environment-ID") or "production"

        ctx = RequestContext(
            request_id=req_id,
            correlation_id=corr_id,
            organization_id=org_id,
            workspace_id=workspace_id,
            environment_id=env_id,
        )

        # Set logging context variables
        ctx_request_id.set(ctx.request_id)
        ctx_trace_id.set(ctx.correlation_id)
        ctx_org_id.set(ctx.organization_id)

        return ctx


class APIExceptionHandler:
    """Handles exceptions and formats responses as RFC 9457 Problem Details."""

    @staticmethod
    def handle_exception(exc: Exception) -> tuple[int, Dict[str, Any]]:
        if isinstance(exc, PlatformException):
            problem = exc.to_problem_details()
            return exc.http_status, problem.to_dict()

        problem = ProblemDetails(
            type="https://api.docutask.ai/errors/internal-server-error",
            title="Internal Server Error",
            status=500,
            detail=str(exc),
        )
        return 500, problem.to_dict()
