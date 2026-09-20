# ADR-703: Database Isolation Model

## Status
Accepted

## Context
Multi-tenant storage requires balancing operational cost, performance, and cross-tenant data leak prevention.

## Decision
Adopt **Shared Database, Shared Schema with Row-Level Tenant Isolation** as the default storage tier, mediated by `TenantDatabaseManager` and `TenantScopedQuery`.
1. Every persistent entity must include mandatory `organization_id` and optional `workspace_id`.
2. Automatic query wrapping injects `WHERE organization_id = :current_tenant_org_id`.
3. Architecture supports future seamless migration to Schema-per-tenant or Database-per-tenant for dedicated enterprise deployments.

## Consequences
- **Positive**: High database resource utilization, simplified schema migrations, zero cross-tenant leak risk via ORM-level query wrapping.
- **Trade-off**: Requires strict developer adherence to `TenantDatabaseManager` and repository wrappers.
