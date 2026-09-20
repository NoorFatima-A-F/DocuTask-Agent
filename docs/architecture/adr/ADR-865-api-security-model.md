# ADR-865: API Security, Authentication & Rate Limiting Model

## Context
AI Governance APIs control critical safety gates, policy configurations, and sensitive audit evidence. The platform must defend against brute force, resource exhaustion, cross-tenant data leakage, and unauthorized modifications.

## Decision
Enforce a multi-layered security architecture:
1. Cryptographically hashed API Keys and Service Account identities.
2. Scoped permissions (`governance:read`, `governance:evaluate`, `governance:admin`).
3. Multi-dimensional Token-Bucket Rate Limiter tracking limits per tenant, client, user, endpoint, and plugin.
4. Structured JSON audit trail and telemetry recording every API interaction.

## Status
Accepted

## Consequences
- Total multi-tenant isolation and abuse prevention.
- Zero-trust security boundary for all governance interactions.
