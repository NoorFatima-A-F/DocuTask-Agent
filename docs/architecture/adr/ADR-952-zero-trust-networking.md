# ADR-952: Zero-Trust Architecture & Default-Deny Authorization

## Status
Accepted

## Context
Perimeter-based network security models assume that internal network traffic is trustworthy. In multi-tenant distributed environments and hybrid clouds, compromised workers or insider threats can freely perform lateral movement if internal calls are unauthenticated.

## Decision
We enforce a strict Zero-Trust model across all service-to-service communication:
1. Every internal request is untrusted by default (`DENY`).
2. Authentication requires mutual TLS (mTLS) with cryptographically verifiable SPIFFE workload identities.
3. `ZeroTrustPolicyEngine` validates caller SPIFFE, target SPIFFE, HTTP method, path prefix, and tenant boundary.
4. All denials are logged to `NetworkFlowLogger` and broadcast as security events.

## Consequences
- Guaranteed elimination of unauthenticated lateral movement.
- Mandatory tenant boundary verification on every inter-service call.
- Comprehensive audit trail of all allowed and denied network attempts.
