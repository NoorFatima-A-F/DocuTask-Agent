"""Tenant Context ASGI/FastAPI Middleware (ESP-MOOS)."""

from __future__ import annotations

from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from app.tenancy.context.context import set_current_tenant_context, reset_tenant_context
from app.tenancy.context.resolver import TenantContextResolver
from app.tenancy.core.exceptions import TenantNotFoundError, TenancyError


class TenantContextMiddleware(BaseHTTPMiddleware):
    """Intercepts all incoming HTTP requests to resolve and set TenantContext."""

    def __init__(self, app, resolver: TenantContextResolver | None = None):
        super().__init__(app)
        self.resolver = resolver or TenantContextResolver()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Bypass open endpoints like health checks
        if request.url.path in ["/health", "/docs", "/openapi.json", "/metrics"]:
            return await call_next(request)

        headers_dict = dict(request.headers)
        try:
            context = self.resolver.resolve_from_headers(headers_dict)
        except TenantNotFoundError:
            # If no org headers provided and path is not an exempt public route, allow downstream or return 400
            if request.url.path.startswith("/api/v1/public") or request.url.path.startswith("/auth"):
                return await call_next(request)
            return JSONResponse(
                status_code=400,
                content={"error": "TenantContextMissing", "message": "X-Organization-Id header required"},
            )
        except TenancyError as e:
            return JSONResponse(
                status_code=403,
                content={"error": e.__class__.__name__, "message": str(e)},
            )

        token = set_current_tenant_context(context)
        try:
            response = await call_next(request)
            response.headers["X-Organization-Id"] = context.organization_id
            response.headers["X-Workspace-Id"] = context.workspace_id
            if context.request_id:
                response.headers["X-Request-Id"] = context.request_id
            return response
        finally:
            reset_tenant_context(token)
