# ADR-861: Governance API Platform Architecture

## Context
External applications, internal microservices, and client SDKs require a unified, secure, multi-tenant interface to interact with AI governance policies, evaluation engines, audit trails, and human-in-the-loop workflows. Direct access to internal database tables or internal modules violates zero-trust principles.

## Decision
Implement a centralized Governance API Gateway routing requests through strict authentication, tenant boundary validation, rate limiting, and audit logging before reaching domain services. All errors follow a canonical `{ "error": { "code": ..., "message": ..., "request_id": ... } }` schema.

## Status
Accepted

## Consequences
- Strict isolation between external consumers and internal governance datastores.
- Comprehensive telemetry and usage tracking per tenant, client, user, and endpoint.
