"""Tests for API Gateway Security, WAF Inspection, Rate Limiting, and HMAC."""

from app.infrastructure.networking.gateway import (
    APIGatewaySecurityManager,
    TokenBucketRateLimiter,
    WAFInspector,
    HMACSignatureValidator,
)


def test_waf_inspector_attack_detection() -> None:
    waf = WAFInspector()

    # Clean request
    clean_res = waf.inspect(path="/api/v1/documents", headers={"content-type": "application/json"}, body='{"doc_id": "123"}')
    assert clean_res.passed is True

    # SQL Injection detection
    sqli_res = waf.inspect(path="/api/v1/documents", headers={}, body="SELECT * FROM users UNION SELECT null, password FROM admin")
    assert sqli_res.passed is False
    assert sqli_res.status_code == 403
    assert "SQL injection" in sqli_res.error_message

    # XSS detection
    xss_res = waf.inspect(path="/api/v1/search?q=<script>alert(1)</script>", headers={})
    assert xss_res.passed is False
    assert "XSS" in xss_res.error_message

    # Directory Traversal detection
    trav_res = waf.inspect(path="/api/v1/files/../../etc/passwd", headers={})
    assert trav_res.passed is False
    assert "traversal" in trav_res.error_message


def test_rate_limiter_and_hmac_signatures() -> None:
    # Rate limiter
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate_per_sec=0.1)
    assert limiter.allow_request("client-1") is True
    assert limiter.allow_request("client-1") is True
    assert limiter.allow_request("client-1") is False  # Capacity exceeded

    # HMAC Signature
    signer = HMACSignatureValidator(secret="test-secret")
    ts = "1726740000"
    sig = signer.sign_request(ts, "POST", "/webhook", '{"event": "test"}')

    # Valid verify
    v_res = signer.verify_signature(sig, ts, "POST", "/webhook", '{"event": "test"}')
    assert v_res.passed is True

    # Tampered body verify
    bad_v_res = signer.verify_signature(sig, ts, "POST", "/webhook", '{"event": "tampered"}')
    assert bad_v_res.passed is False


def test_api_gateway_security_manager() -> None:
    gw = APIGatewaySecurityManager()

    # Valid API Key
    res_valid = gw.inspect_request(
        client_ip="1.2.3.4",
        path="/api/v1/documents",
        headers={"x-api-key": "test-api-key-enterprise"},
    )
    assert res_valid.passed is True
    assert res_valid.claims["tenant_id"] == "tenant-01"

    # Missing API Key
    res_missing = gw.inspect_request(
        client_ip="1.2.3.4",
        path="/api/v1/documents",
        headers={},
    )
    assert res_missing.passed is False
    assert res_missing.status_code == 401
