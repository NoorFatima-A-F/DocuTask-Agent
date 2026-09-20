"""Enterprise Governance API Gateway Middleware.

Intercepts incoming requests, validates tenant isolation boundaries, tracks execution
timings, handles security scopes, and routes audit events to the governance platform.
"""

from datetime import datetime, timezone
import logging
import time
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from .authentication import APIRequestContext, AuthenticationManager
from .rate_limit import RateLimiter

logger = logging.getLogger(__name__)


class GatewayTelemetryEvent(BaseModel):
    """Telemetry recorded for every processed API request."""

    request_id: str
    tenant_id: str
    client_id: str
    user_id: Optional[str] = None
    endpoint: str
    method: str
    status_code: int
    duration_ms: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error_code: Optional[str] = None


class GatewayMiddleware:
    """Enterprise API Gateway Pipeline Middleware."""

    def __init__(
        self,
        auth_manager: AuthenticationManager,
        rate_limiter: RateLimiter,
    ) -> None:
        self.auth_manager = auth_manager
        self.rate_limiter = rate_limiter
        self.telemetry_history: List[GatewayTelemetryEvent] = []

    def process_request(
        self,
        method: str,
        path: str,
        headers: Dict[str, str],
        handler: Callable[[APIRequestContext], Dict[str, Any]],
        required_scope: Optional[str] = None,
        tenant_override: Optional[str] = None,
        cost: int = 1,
    ) -> Dict[str, Any]:
        """Execute request pipeline through auth, rate limiting, handler, and telemetry."""
        start_time = time.time()
        request_id = headers.get("X-Request-ID")

        try:
            # 1. Identity & Auth
            auth_header = headers.get("Authorization")
            api_key_header = headers.get("X-API-Key")
            client_ip = headers.get("X-Forwarded-For", "127.0.0.1")

            ctx = self.auth_manager.authenticate_request(
                authorization_header=auth_header,
                api_key_header=api_key_header,
                client_ip=client_ip,
            )
            if request_id:
                ctx.request_id = request_id

            # 2. Tenant isolation verification
            if tenant_override and tenant_override != ctx.tenant_id and not ctx.has_scope("governance:admin"):
                raise PermissionError(f"Cross-tenant access denied. Cannot access tenant {tenant_override}.")

            # 3. Scope validation
            if required_scope and not ctx.has_scope(required_scope):
                raise PermissionError(f"Missing required permission scope: {required_scope}")

            # 4. Rate limiting check
            allowed, rate_info = self.rate_limiter.check_rate_limit(
                tenant_id=ctx.tenant_id,
                client_id=ctx.client_id,
                user_id=ctx.user_id,
                endpoint=path,
                cost=cost,
            )
            if not allowed:
                duration_ms = (time.time() - start_time) * 1000.0
                self.telemetry_history.append(
                    GatewayTelemetryEvent(
                        request_id=ctx.request_id,
                        tenant_id=ctx.tenant_id,
                        client_id=ctx.client_id,
                        user_id=ctx.user_id,
                        endpoint=path,
                        method=method,
                        status_code=429,
                        duration_ms=duration_ms,
                        error_code="RATE_LIMIT_EXCEEDED",
                    )
                )
                return {
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": f"Rate limit exceeded on {rate_info.get('dimension')}.",
                        "request_id": ctx.request_id,
                    }
                }

            # 5. Handler Execution
            result = handler(ctx)
            duration_ms = (time.time() - start_time) * 1000.0

            self.telemetry_history.append(
                GatewayTelemetryEvent(
                    request_id=ctx.request_id,
                    tenant_id=ctx.tenant_id,
                    client_id=ctx.client_id,
                    user_id=ctx.user_id,
                    endpoint=path,
                    method=method,
                    status_code=200,
                    duration_ms=duration_ms,
                )
            )
            return result

        except PermissionError as pe:
            duration_ms = (time.time() - start_time) * 1000.0
            req_id = request_id or "req_unknown"
            self.telemetry_history.append(
                GatewayTelemetryEvent(
                    request_id=req_id,
                    tenant_id="unknown",
                    client_id="unknown",
                    endpoint=path,
                    method=method,
                    status_code=403,
                    duration_ms=duration_ms,
                    error_code="FORBIDDEN",
                )
            )
            return {
                "error": {
                    "code": "FORBIDDEN",
                    "message": str(pe),
                    "request_id": req_id,
                }
            }
        except Exception as ex:
            duration_ms = (time.time() - start_time) * 1000.0
            req_id = request_id or "req_unknown"
            logger.exception("Internal Gateway Error: %s", ex)
            self.telemetry_history.append(
                GatewayTelemetryEvent(
                    request_id=req_id,
                    tenant_id="unknown",
                    client_id="unknown",
                    endpoint=path,
                    method=method,
                    status_code=500,
                    duration_ms=duration_ms,
                    error_code="INTERNAL_ERROR",
                )
            )
            return {
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(ex),
                    "request_id": req_id,
                }
            }
