# ADR 076: Network Communication Policies & Namespace Isolation

## Status
Accepted

## Context
Multi-tenant compliance requires strict boundary enforcement between system namespaces, worker tiers, database connectors, and AI execution sandboxes.

## Decision
Deploy a prioritized Network Policy Engine (`NetworkPolicyEngine`) that evaluates ingress and egress rules per namespace and service. Rules support wildcard matching, HTTP method constraints, path-level filters, and explicit ALLOW/DENY/AUDIT actions.

## Consequences
- **Positive**: Hard isolation between untrusted worker executions and sensitive database/key management layers.
- **Negative**: Misconfigured rules could drop legitimate traffic if not audited first in permissive mode.
