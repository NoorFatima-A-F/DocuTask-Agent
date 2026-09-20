# Architecture Decision Record: ADR-003

## Title
Enterprise Multi-Tenancy Architecture: 7-Tier Hierarchical Scoping, PostgreSQL Row-Level Security, and Cryptographic Secret Isolation

## Status
**ACCEPTED** (2026-03-24)

## Context
DocuTask Agent is transitioning from a single-tenant/siloed document processing tool into an enterprise-grade multi-tenant autonomous workflow platform serving Fortune 500 enterprises, regulated healthcare networks, and global financial institutions.

In multi-tenant enterprise SaaS, tenant isolation failures represent existential security and compliance risks (GDPR, HIPAA, SOC 2, ISO 27001). Traditional approaches to multi-tenancy exhibit distinct architectural trade-offs:

1. **Silo Isolation (Database-per-Tenant)**: Highest isolation, but catastrophic operational complexity and cost overhead when scaling to thousands of tenants (pool exhaustion, schema migration friction, resource fragmentation).
2. **Coarse Shared Schema (Tenant ID column in application query predicates)**: High density and low cost, but vulnerable to catastrophic developer error where an omitted `WHERE tenant_id = ?` query exposes cross-tenant data.
3. **Container-per-Tenant**: Severe infrastructure cost and cold-start latency for autonomous agent execution.

DocuTask Agent requires a multi-tenant architecture that delivers **defense-in-depth isolation**, high infrastructure resource density, strict compliance boundaries, and deterministic policy enforcement across data, execution runtimes, secrets, and AI models.

---

## Decision

We adopt a **7-Tier Hierarchical Multi-Tenancy Architecture** enforced at the kernel, database, object storage, and secret layers:

### 1. 7-Tier Hierarchy
Every operational entity in DocuTask Agent is bound to a strict hierarchical path:
1. `Platform`: Global management control plane.
2. `Enterprise`: Top-level conglomerate / parent customer entity.
3. `Organization`: Operating enterprise business entity / billing boundary.
4. `Workspace`: Business unit, department, or regional team boundary.
5. `Environment`: Lifecycle stage (`production`, `staging`, `development`, `sandbox`).
6. `Project`: Specific business initiative, workflow group, or document domain.
7. `Principal / Agent`: Human user, service account, or autonomous agent executor.

### 2. Mandatory Triple Scoping Envelope
Every database row, CloudEvent, API request context, log line, and storage key MUST carry the immutable scope triplet:
```
(organization_id, workspace_id, environment_id)
```

### 3. Database Layer: PostgreSQL Native Row-Level Security (RLS)
- We mandate PostgreSQL Row-Level Security (RLS) on all multi-tenant tables.
- RLS policies use PostgreSQL transaction session variables (`app.current_org_id`, `app.current_workspace_id`, `app.current_env_id`).
- Database connection pools use unprivileged application roles where RLS is enforced at the database kernel level, preventing SQL injection or developer query bugs from breaching tenant boundaries:
```sql
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents FORCE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_policy ON documents
  USING (
    org_id = current_setting('app.current_org_id')::uuid
    AND workspace_id = current_setting('app.current_workspace_id')::uuid
    AND env_id = current_setting('app.current_env_id')::text
  );
```

### 4. Storage and Secret Isolation
- **S3 / Blob Storage**: Object keys strictly scoped by hierarchy:
  `s3://docutask-enterprise-{org_id}/{workspace_id}/{env_id}/{resource_type}/{resource_id}`
- **Secrets Management (HashiCorp Vault / AWS Secrets Manager)**: Paths mounted per tenant:
  `/secret/docutask/orgs/{org_id}/workspaces/{workspace_id}/{env_id}/...`
- **Envelope Encryption**: Dedicated Customer-Managed Encryption Keys (CMEK) via AWS KMS / GCP KMS / Azure Key Vault per Enterprise/Organization with automated 90-day rotation.

### 5. Runtime & Agent Memory Isolation
- Agent episodic memory and vector search partitions are physically isolated using tenant-scoped collection namespaces and HNSW graph filters (`filter: { org_id: ..., workspace_id: ..., env_id: ... }`).
- Agent execution sandboxes run in ephemeral gVisor / Firecracker runtimes with network isolation policies preventing cross-tenant egress.

---

## Consequences

### Positive
- **Guaranteed Defense-in-Depth**: Impossible to leak tenant data via standard application-level SQL omissions because the database engine rejects unauthenticated queries.
- **Regulatory Compliance**: Satisfies SOC 2 Type II, HIPAA multi-tenant data segregation, and FedRAMP isolation criteria.
- **Resource Efficiency**: High data density and cost efficiency on shared PostgreSQL and Redis clusters without sacrificing strict cryptographic isolation.
- **Granular Quotas & Attribution**: Precise real-time tracking of token consumption, storage utilization, and worker compute per workspace.

### Negative / Trade-Offs
- **Connection Setup Overhead**: Every database checkout from the connection pool must execute `SET LOCAL app.current_org_id = ...` (mitigated via pooled session hooks in SQLAlchemy / asyncpg).
- **Complex Superuser / Cross-Tenant Analytics**: Global platform maintenance and cross-tenant aggregate analytics require dedicated bypass roles and hardened audit-logged analytics pipelines.
- **Schema Migrations**: Schema migrations must be tested against RLS policies to ensure migration scripts do not accidentally violate or lock RLS constraints.

---

## Alternatives Considered

1. **Database-Per-Tenant (Physical Silo)**: Rejected due to excessive infrastructure cost, connection pool starvation at >1,000 tenants, and high operational toil during global migrations.
2. **Schema-Per-Tenant**: Rejected due to PostgreSQL DDL lock contention and degraded performance when scaling beyond 500 schemas per cluster.
3. **Application-Level Only Scoping (Pure ORM Filters)**: Rejected as unacceptable enterprise risk; a single missing `.filter(tenant_id=...)` in raw SQL or ORM query would lead to catastrophic data disclosure.
