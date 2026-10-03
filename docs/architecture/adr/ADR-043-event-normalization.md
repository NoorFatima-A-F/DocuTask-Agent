# ADR-043: Canonical Event Normalization Architecture

## Status
Accepted

## Context
External systems emit webhooks and event notifications in incompatible formats (e.g. GitHub JSON, Stripe JSON, Salesforce XML, custom headers). Downstream event listeners, workflow triggers, and agent reflection engines cannot handle hundreds of ad-hoc event schemas.

## Decision
We introduce the `EventNormalizer` and standard `NormalizedEvent` schema. All incoming webhook payloads and polling results are parsed, enriched with tenant metadata, classified into canonical event taxonomy (e.g. `communication.email.received`, `storage.file.uploaded`), and tagged with distributed correlation IDs.

## Consequences
- Single unified event contract consumed by Workflow Triggers, Agent Event Bus, and Analytics.
- Standardized tracing and correlation across distributed multi-system asynchronous workflows.
