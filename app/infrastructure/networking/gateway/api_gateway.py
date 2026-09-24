"""North-South API Gateway Security Manager."""

from typing import Any, Dict, Optional
from .filters import (
    GatewayFilterResult,
    TokenBucketRateLimiter,
    IPFilter,
    WAFInspector,
    HMACSignatureValidator,
)


class APIGatewaySecurityManager:
    """Orchestrates North-South traffic security verification."""

    def __init__(
        self,
        rate_limiter: Optional[TokenBucketRateLimiter] = None,
        ip_filter: Optional[IPFilter] = None,
        waf: Optional[WAFInspector] = None,
        hmac_validator: Optional[HMACSignatureValidator] = None,
    ) -> None:
        self.rate_limiter = rate_limiter or TokenBucketRateLimiter()
        self.ip_filter = ip_filter or IPFilter()
        self.waf = waf or WAFInspector()
        self.hmac_validator = hmac_validator or HMACSignatureValidator()
        self._valid_api_keys: Dict[str, Dict[str, Any]] = {
            "test-api-key-enterprise": {"tenant_id": "tenant-01", "role": "admin"},
            "test-api-key-standard": {"tenant_id": "tenant-02", "role": "user"},
        }

    def register_api_key(self, api_key: str, metadata: Dict[str, Any]) -> None:
        """Register valid API key."""
        self._valid_api_keys[api_key] = metadata

    def authenticate_api_key(self, api_key: Optional[str]) -> GatewayFilterResult:
        """Verify API key."""
        if not api_key:
            return GatewayFilterResult(
                passed=False,
                status_code=401,
                error_message="Missing X-API-Key header",
                filter_name="APIKeyAuth",
            )
        info = self._valid_api_keys.get(api_key)
        if not info:
            return GatewayFilterResult(
                passed=False,
                status_code=401,
                error_message="Invalid or revoked API key",
                filter_name="APIKeyAuth",
            )
        return GatewayFilterResult(passed=True, claims=info, filter_name="APIKeyAuth")

    def inspect_request(
        self,
        client_ip: str,
        path: str,
        headers: Dict[str, str],
        body: Optional[str] = None,
        require_api_key: bool = True,
    ) -> GatewayFilterResult:
        """Execute full North-South security filter chain."""
        # 1. IP Filter
        if not self.ip_filter.check_ip(client_ip):
            return GatewayFilterResult(
                passed=False,
                status_code=403,
                error_message=f"Client IP {client_ip} is blocked",
                filter_name="IPFilter",
            )

        # 2. Rate Limiting
        client_key = headers.get("x-api-key", client_ip)
        if not self.rate_limiter.allow_request(client_key):
            return GatewayFilterResult(
                passed=False,
                status_code=429,
                error_message="Rate limit exceeded. Please retry later.",
                filter_name="RateLimiter",
            )

        # 3. WAF Inspection
        waf_res = self.waf.inspect(path, headers, body)
        if not waf_res.passed:
            return waf_res

        # 4. API Key Check if required
        if require_api_key:
            api_key = headers.get("x-api-key") or headers.get("X-API-Key")
            auth_res = self.authenticate_api_key(api_key)
            if not auth_res.passed:
                return auth_res
            return auth_res

        return GatewayFilterResult(passed=True, filter_name="APIGatewaySecurityManager")
