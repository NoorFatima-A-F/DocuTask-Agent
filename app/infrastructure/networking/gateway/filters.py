"""API Gateway Security Filters, JWT/OAuth2 Validation, WAF, and Rate Limiting."""

from dataclasses import dataclass, field
import hashlib
import hmac
import re
import time
from typing import Any, Dict, Optional, Set
import threading


@dataclass
class GatewayFilterResult:
    """Outcome of an API gateway security filter check."""
    passed: bool
    status_code: int = 200
    error_message: Optional[str] = None
    claims: Dict[str, Any] = field(default_factory=dict)
    filter_name: str = ""


class TokenBucketRateLimiter:
    """Thread-safe token-bucket rate limiter per client IP or API key."""

    def __init__(self, capacity: int = 100, refill_rate_per_sec: float = 20.0) -> None:
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self._tokens: Dict[str, float] = {}
        self._last_refill: Dict[str, float] = {}
        self._lock = threading.Lock()

    def allow_request(self, client_key: str, cost: float = 1.0) -> bool:
        """Evaluate if request is within rate limit."""
        now = time.time()
        with self._lock:
            last = self._last_refill.get(client_key, now)
            current_tokens = self._tokens.get(client_key, float(self.capacity))

            # Refill tokens
            elapsed = now - last
            current_tokens = min(float(self.capacity), current_tokens + elapsed * self.refill_rate)
            self._last_refill[client_key] = now

            if current_tokens >= cost:
                self._tokens[client_key] = current_tokens - cost
                return True
            else:
                self._tokens[client_key] = current_tokens
                return False


class IPFilter:
    """IP allow/deny list filter."""

    def __init__(self, allow_list: Optional[Set[str]] = None, deny_list: Optional[Set[str]] = None) -> None:
        self.allow_list = allow_list or set()
        self.deny_list = deny_list or set()

    def check_ip(self, client_ip: str) -> bool:
        """Check if client IP is permitted."""
        if client_ip in self.deny_list:
            return False
        if self.allow_list and client_ip not in self.allow_list:
            return False
        return True


class WAFInspector:
    """Web Application Firewall (WAF) filter detecting SQLi, XSS, and path traversal."""

    SQLI_PATTERNS = [
        r"(\bUNION\b\s+\bSELECT\b)",
        r"(\bDROP\b\s+\bTABLE\b)",
        r"(--|\bOR\b\s+1\s*=\s*1)",
        r"(';\s*--)",
    ]
    XSS_PATTERNS = [
        r"(<script.*?>.*?</script>)",
        r"(javascript\s*:)",
        r"(onerror\s*=)",
        r"(onload\s*=)",
    ]
    TRAVERSAL_PATTERNS = [
        r"(\.\./\.\.)",
        r"(%2e%2e%2f)",
        r"(/etc/passwd)",
    ]

    def inspect(self, path: str, headers: Dict[str, str], body: Optional[str] = None) -> GatewayFilterResult:
        """Scan request components for malicious patterns."""
        combined = f"{path} {' '.join(headers.values())} {body or ''}"

        for p in self.SQLI_PATTERNS:
            if re.search(p, combined, re.IGNORECASE):
                return GatewayFilterResult(
                    passed=False,
                    status_code=403,
                    error_message="WAF block: Potential SQL injection attack detected",
                    filter_name="WAFInspector",
                )

        for p in self.XSS_PATTERNS:
            if re.search(p, combined, re.IGNORECASE):
                return GatewayFilterResult(
                    passed=False,
                    status_code=403,
                    error_message="WAF block: Potential XSS attack detected",
                    filter_name="WAFInspector",
                )

        for p in self.TRAVERSAL_PATTERNS:
            if re.search(p, combined, re.IGNORECASE):
                return GatewayFilterResult(
                    passed=False,
                    status_code=403,
                    error_message="WAF block: Directory traversal attack detected",
                    filter_name="WAFInspector",
                )

        return GatewayFilterResult(passed=True, filter_name="WAFInspector")


class HMACSignatureValidator:
    """Verifies HMAC SHA-256 request signatures for webhooks and machine APIs."""

    def __init__(self, secret: str = "secret-gateway-hmac-key") -> None:
        self.secret = secret.encode("utf-8")

    def sign_request(self, timestamp: str, method: str, path: str, body: str = "") -> str:
        """Compute HMAC SHA256 signature."""
        msg = f"{timestamp}:{method.upper()}:{path}:{body}".encode("utf-8")
        return hmac.new(self.secret, msg, hashlib.sha256).hexdigest()

    def verify_signature(self, signature: str, timestamp: str, method: str, path: str, body: str = "") -> GatewayFilterResult:
        """Verify signature match."""
        expected = self.sign_request(timestamp, method, path, body)
        if not hmac.compare_digest(signature, expected):
            return GatewayFilterResult(
                passed=False,
                status_code=401,
                error_message="Invalid HMAC request signature",
                filter_name="HMACSignatureValidator",
            )
        return GatewayFilterResult(passed=True, filter_name="HMACSignatureValidator")
