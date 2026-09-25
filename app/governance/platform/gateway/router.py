"""Enterprise Governance API Gateway Router.

Central routing orchestrator that maps public and internal URL routes to their
respective governance services while enforcing authentication, tenant isolation,
scopes, and rate limits.
"""

from typing import Any, Callable, Dict, List, Optional
from .authentication import APIRequestContext, AuthenticationManager
from .middleware import GatewayMiddleware
from .rate_limit import RateLimiter


class RouteDefinition:
    """Definition of a registered route."""

    def __init__(
        self,
        method: str,
        path: str,
        handler: Callable[..., Any],
        required_scope: Optional[str] = None,
        description: str = "",
        tags: Optional[List[str]] = None,
    ) -> None:
        self.method = method.upper()
        self.path = path
        self.handler = handler
        self.required_scope = required_scope
        self.description = description
        self.tags = tags or ["Governance"]


class GatewayRouter:
    """Central API Gateway Router for the Governance Developer Platform."""

    def __init__(
        self,
        auth_manager: Optional[AuthenticationManager] = None,
        rate_limiter: Optional[RateLimiter] = None,
    ) -> None:
        self.auth_manager = auth_manager or AuthenticationManager()
        self.rate_limiter = rate_limiter or RateLimiter()
        self.middleware = GatewayMiddleware(self.auth_manager, self.rate_limiter)
        self._routes: Dict[str, RouteDefinition] = {}

    def add_route(
        self,
        method: str,
        path: str,
        handler: Callable[..., Any],
        required_scope: Optional[str] = None,
        description: str = "",
        tags: Optional[List[str]] = None,
    ) -> None:
        """Register a route with the gateway."""
        key = f"{method.upper()}:{path}"
        self._routes[key] = RouteDefinition(
            method=method,
            path=path,
            handler=handler,
            required_scope=required_scope,
            description=description,
            tags=tags,
        )

    def dispatch(
        self,
        method: str,
        path: str,
        headers: Dict[str, str],
        body: Optional[Dict[str, Any]] = None,
        path_params: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Dispatch an incoming HTTP-like call through gateway middleware to route handler."""
        key = f"{method.upper()}:{path}"
        route = self._routes.get(key)

        if not route:
            # Check dynamic parameter matches (e.g. /policies/{id})
            matched_route = None
            extracted_params: Dict[str, str] = {}
            for r_key, r_def in self._routes.items():
                r_method, r_path = r_key.split(":", 1)
                if r_method != method.upper():
                    continue
                p_parts = r_path.strip("/").split("/")
                req_parts = path.strip("/").split("/")
                if len(p_parts) == len(req_parts):
                    match = True
                    cur_extracted = {}
                    for p_part, req_part in zip(p_parts, req_parts):
                        if p_part.startswith("{") and p_part.endswith("}"):
                            param_name = p_part[1:-1]
                            cur_extracted[param_name] = req_part
                        elif p_part != req_part:
                            match = False
                            break
                    if match:
                        matched_route = r_def
                        extracted_params = cur_extracted
                        break

            if matched_route:
                route = matched_route
                if path_params:
                    path_params.update(extracted_params)
                else:
                    path_params = extracted_params
            else:
                return {
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f"Endpoint not found: {method.upper()} {path}",
                        "request_id": headers.get("X-Request-ID", "req_unknown"),
                    }
                }

        def wrapped_handler(ctx: APIRequestContext) -> Dict[str, Any]:
            kwargs: Dict[str, Any] = {"ctx": ctx}
            if body is not None:
                kwargs["body"] = body
            if path_params:
                kwargs["path_params"] = path_params
            if query_params:
                kwargs["query_params"] = query_params
            return route.handler(**kwargs)

        return self.middleware.process_request(
            method=method,
            path=path,
            headers=headers,
            handler=wrapped_handler,
            required_scope=route.required_scope,
        )

    def generate_openapi_spec(self, version: str = "1.0.0") -> Dict[str, Any]:
        """Generate dynamic OpenAPI 3.0.0 specification schema."""
        paths: Dict[str, Any] = {}
        for key, route in self._routes.items():
            method, path = key.split(":", 1)
            method_lower = method.lower()
            if path not in paths:
                paths[path] = {}
            paths[path][method_lower] = {
                "summary": route.description or f"{method} {path}",
                "tags": route.tags,
                "security": [{"BearerAuth": []}],
                "responses": {
                    "200": {"description": "Successful operation"},
                    "401": {"description": "Unauthorized credentials"},
                    "403": {"description": "Forbidden scope or cross-tenant violation"},
                    "429": {"description": "Rate limit exceeded"},
                },
            }

        return {
            "openapi": "3.0.0",
            "info": {
                "title": "DocuTask Enterprise Governance Platform API",
                "version": version,
                "description": "Production-grade Governance Extensibility and Developer Platform API",
            },
            "paths": paths,
            "components": {
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "APIKey",
                    }
                }
            },
        }
