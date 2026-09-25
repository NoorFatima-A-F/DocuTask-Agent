"""
Request Context & Security Headers Middleware.
Attaches unique X-Request-ID UUID headers, measures request timing (latency),
sets enterprise security headers, and logs HTTP access events structuredly.
"""

import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.security import sanitize_log_input
from app.core.logging import logger


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware attaching request timing, Request-ID, and enterprise security headers."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Extract or generate unique Request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        start_time = time.perf_counter()
        
        # Log request start
        logger.info("HTTP Request Started: %s %s | RequestID=%s", request.method, sanitize_log_input(request.url.path), sanitize_log_input(request_id))

        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = int((time.perf_counter() - start_time) * 1000)
            logger.error(
                "HTTP Request Failed: %s %s | Duration=%dms | Error=%s",
                request.method,
                sanitize_log_input(request.url.path),
                duration_ms,
                sanitize_log_input(exc),
            )
            raise exc

        duration_ms = int((time.perf_counter() - start_time) * 1000)

        # Attach custom process headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{duration_ms}ms"

        # Enterprise Security Headers (OWASP Recommended Defaults)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        
        # Relax CSP on Swagger / ReDoc docs endpoints to allow Swagger UI CDN resources
        if any(request.url.path.endswith(ext) for ext in ["/docs", "/redoc", "/openapi.json"]):
            response.headers["Content-Security-Policy"] = (
                "default-src 'self' https://cdn.jsdelivr.net 'unsafe-inline' 'unsafe-eval' data:; "
                "img-src 'self' data: https://fastapi.tiangolo.com https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;"
            )
        else:
            response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"
            
        response.headers["Cache-Control"] = "no-store, max-age=0"


        logger.info(
            f"HTTP Response Completed: {request.method} {request.url.path} | Status={response.status_code} | Duration={duration_ms}ms | RequestID={request_id}"
        )

        return response
