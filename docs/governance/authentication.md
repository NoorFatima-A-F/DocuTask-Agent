# Governance Platform Authentication & Security Model

DocuTask Governance uses a zero-trust multi-tenant authentication model.

---

## Authentication Schemes
1. **API Keys**: High-performance, cryptographically hashed API tokens with granular rate-limits and scopes.
2. **Service Accounts**: Non-human identities assigned to microservices, cron jobs, and CI/CD pipelines.
3. **OAuth2 / OIDC Tokens**: Enterprise federated identity for human reviewers and dashboard access.

---

## Permission Scopes
* `governance:read`: Read-only access to policies, decisions, and analytics.
* `governance:evaluate`: Authority to evaluate actions against governance rules.
* `governance:admin`: Full tenant administrative authority (create/publish policies, approve plugins, delete resources).
* `governance:plugin:read`: Permission to execute within the sandbox.
