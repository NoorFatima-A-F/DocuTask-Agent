# ADR-957: North-South API Gateway Security & Web Application Firewall

## Status
Accepted

## Context
Edge ingress and external webhook endpoints face threats from unauthorized clients, volumetric DDoS attacks, automated bots, and web application vulnerabilities (SQL injection, Cross-Site Scripting, Path Traversal).

## Decision
We implement `APIGatewaySecurityManager` with dedicated security filters:
1. Multi-factor client authentication supporting API Keys, JWT tokens, and HMAC-SHA256 request signatures.
2. Web Application Firewall (`WAFInspector`) scanning paths, headers, and payloads for SQLi, XSS, and directory traversal signatures.
3. Token-bucket rate limiter (`TokenBucketRateLimiter`) enforcing per-client and per-IP request velocity caps.
4. IP allow/deny list filtering (`IPFilter`) for restricting administrative or sensitive ingest endpoints.

## Consequences
- Multi-layered defense-in-depth on all North-South incoming requests.
- Immediate blocking of malicious payload attacks before reaching internal application services.
- Protection against noisy neighbors and API quota exhaustion.
