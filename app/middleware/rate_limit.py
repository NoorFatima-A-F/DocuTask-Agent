"""
Rate Limiting Middleware Module.
Implements in-memory sliding window rate limiting on sensitive authentication endpoints
to protect against brute-force and credential stuffing attacks.
Designed for drop-in Redis counter replacement in distributed environments.
"""

import time
from collections import defaultdict
from typing import Dict, List, Tuple
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.logging import logger
from app.core.security import sanitize_log_input
from app.schemas.response import APIResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware enforcing sliding window rate limits on sensitive endpoints."""

    # Default route rate limits: (max_requests, window_seconds)
    ROUTE_LIMITS: Dict[str, Tuple[int, int]] = {
        "/api/v1/auth/login": (5, 60),      # 5 requests per minute
        "/api/v1/auth/register": (10, 60),  # 10 requests per minute
        "/api/v1/auth/refresh": (20, 60),   # 20 requests per minute
    }

    def __init__(self, app):
        super().__init__(app)
        # Client request history: ip_key -> list of timestamp floats
        self._history: Dict[str, List[float]] = defaultdict(list)

    def _get_client_ip(self, request: Request) -> str:
        """Extracts client IP address considering proxy headers."""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "127.0.0.1"

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        path = request.url.path.rstrip("/")
        
        # Check if route requires rate limiting
        if request.method == "POST" and path in self.ROUTE_LIMITS:
            max_requests, window_seconds = self.ROUTE_LIMITS[path]
            client_ip = self._get_client_ip(request)
            key = f"{client_ip}:{path}"
            
            now = time.time()
            cutoff = now - window_seconds

            # Filter out timestamps outside window
            timestamps = [t for t in self._history[key] if t > cutoff]
            self._history[key] = timestamps

            if len(timestamps) >= max_requests:
                retry_after = int(window_seconds - (now - timestamps[0])) if timestamps else window_seconds
                logger.warning(
                    "Rate limit exceeded for IP '%s' on '%s': %d/%d",
                    sanitize_log_input(client_ip),
                    sanitize_log_input(path),
                    len(timestamps),
                    max_requests,
                )
                
                response_body = APIResponse.error_response(
                    message="Rate limit exceeded. Please try again later.",
                    errors={"limit": max_requests, "window_seconds": window_seconds, "retry_after_seconds": retry_after}
                ).model_dump()

                return JSONResponse(
                    status_code=429,
                    content=response_body,
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Limit": str(max_requests),
                        "X-RateLimit-Remaining": "0"
                    }
                )

            # Record current request timestamp
            self._history[key].append(now)
            remaining = max_requests - len(self._history[key])

            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(max_requests)
            response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
            return response

        return await call_next(request)
