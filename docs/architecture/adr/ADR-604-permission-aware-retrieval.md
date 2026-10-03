# ADR-604: Zero-Trust Permission-Aware Retrieval Architecture

## Status
Accepted

## Context
Standard RAG systems index documents globally and return matches to any requesting user, risking catastrophic cross-tenant data leaks and unauthorized access to confidential HR or executive materials.

## Decision
We enforce strict **Permission-Aware Zero-Trust Retrieval**:
1. Every search request requires a validated `UserSecurityContext` containing user ID, tenant org ID, workspace ID, department, roles, and clearance level.
2. The `KnowledgeGovernanceEngine` applies multi-tiered security checks (tenant boundary, clearance rank vs document classification, user ACLs, department allowlists) to filter out unauthorized knowledge chunks *prior* to context synthesis.

## Consequences
- Guaranteed multi-tenant and role-based data isolation during all AI generation workflows.
- Eliminates the possibility of unauthorized document content leaking into AI prompt contexts.
