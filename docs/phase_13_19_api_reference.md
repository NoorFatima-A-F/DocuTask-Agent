# Phase 13.19: SaaS Platform REST API Reference

Mounted at: `/api/v1/saas`

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/saas/overview` | Platform executive overview (MRR, active tenants, usage, system health) |
| `GET` | `/api/v1/saas/tenants` | List all provisioned tenants |
| `POST` | `/api/v1/saas/tenants` | Provision a new enterprise tenant |
| `GET` | `/api/v1/saas/tenants/{tenant_id}` | Get tenant details, limits, and configuration |
| `GET` | `/api/v1/saas/organizations` | Get multi-tier organization tree |
| `POST` | `/api/v1/saas/organizations` | Create an organization / subsidiary node |
| `GET` | `/api/v1/saas/workspaces` | List isolated workspaces |
| `POST` | `/api/v1/saas/workspaces` | Provision an isolated workspace |
| `GET` | `/api/v1/saas/subscriptions` | List subscriptions and plan tiers |
| `POST` | `/api/v1/saas/subscriptions` | Upgrade / create a subscription |
| `GET` | `/api/v1/saas/usage` | Query metered usage records |
| `GET` | `/api/v1/saas/billing/invoices` | List billing invoices |
| `GET` | `/api/v1/saas/licenses` | List and verify cryptographic license keys |
| `GET` | `/api/v1/saas/marketplace` | Browse AI Marketplace assets |
| `POST` | `/api/v1/saas/marketplace/publish` | Publish verified asset to marketplace |
| `GET` | `/api/v1/saas/integrations` | List integration hub connectors |
| `POST` | `/api/v1/saas/integrations/authorize` | Authorize enterprise connector |
| `GET` | `/api/v1/saas/policies` | List tenant security & ABAC policies |
| `GET` | `/api/v1/saas/audit` | Query immutable audit ledger |
| `GET` | `/api/v1/saas/branding/{tenant_id}` | Get tenant white-label branding |
| `POST` | `/api/v1/saas/branding/{tenant_id}` | Update white-label branding |
| `POST` | `/api/v1/saas/orchestration/cycle` | Execute master SaaS orchestration cycle |
