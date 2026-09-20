# North-South API Gateway Security Guide

## 1. Gateway Security Architecture
All external incoming traffic passes through the North-South API Gateway filter chain:
1. **IP Allow / Deny Filtering**: Fast drop of blacklisted CIDR ranges or hostile ASNs.
2. **Token Bucket Rate Limiting**: Client IP / API Key request rate limiting.
3. **WAF Inspection**: Deep payload inspection for SQL injection, Cross-Site Scripting, and Directory Traversal.
4. **Client Authentication**: Multi-protocol authentication (API Keys, OAuth2/JWT tokens, HMAC request signatures).

## 2. Configuring Gateway Security
```python
from app.infrastructure.networking.gateway import APIGatewaySecurityManager

gw = APIGatewaySecurityManager()
gw.register_api_key("secret-api-key-cust-01", {"tenant_id": "cust-01", "tier": "enterprise"})

result = gw.inspect_request(
    client_ip="192.168.1.50",
    path="/api/v1/documents/upload",
    headers={"x-api-key": "secret-api-key-cust-01"},
    body='{"filename": "contract.pdf"}'
)
if not result.passed:
    # Reject request
    return result.status_code, result.error_message
```
