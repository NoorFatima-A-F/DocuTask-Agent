# ADR 073: Zero-Trust Network & Contextual Security Model

## Status
Accepted

## Context
Perimeter-based network security is insufficient for multi-tenant AI governance platforms. Internal lateral movement and credential theft must be defended against using continuous verification of every request.

## Decision
Implement a strict Zero-Trust Evaluation Engine (`ZeroTrustEvaluator`) where:
1. Every service-to-service call requires an attested SPIFFE SVID.
2. Network policies default to DENY unless explicitly allowed by namespace/service/method/path rules.
3. Contextual risk scoring calculates dynamic threat levels based on client IP, tenant reputation, and anomalous patterns.

## Consequences
- **Positive**: Complete defense-in-depth, zero lateral movement, auditable authorization decisions.
- **Negative**: Requires strict policy authoring during onboarding of new services.
