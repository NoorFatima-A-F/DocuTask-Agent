# ADR-916: Multi-Tenant Pinned Regional Isolation and Compliance Boundaries

## Status
Accepted

## Context
High-security tenants require dedicated pinning to specific regions or clusters with exclusive isolation rules and disallowed fallback regions.

## Decision
Implement `TenantAffinityManager` and `TenantAffinityRule` enforcing pinned regions, allowed regions, and disallowed fallback boundaries at routing time.

## Consequences
- Guaranteed strict multi-tenant isolation.
- Prevents cross-jurisdiction leakage of sensitive corporate documents.
