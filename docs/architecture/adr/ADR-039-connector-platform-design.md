# ADR-039: Universal Connector Platform & Plugin Architecture

## Status
Accepted

## Context
Enterprise workflows and multi-agent systems must interact with hundreds of external business applications (CRMs, communication tools, ERPs, cloud storage). Directly coupling workflows or AI models to proprietary vendor SDKs leads to vendor lock-in, credential leakage, brittle spaghetti code, and maintenance nightmares.

## Decision
We implement a plugin-based **Universal Connector Platform (EIF-UCP)** where:
1. Every external integration is treated uniformly as an installable capability provider implementing the `BaseConnector` SDK contract.
2. The workflow engine and multi-agent runtime interact solely with abstract capability interfaces (`email.send`, `storage.upload`) rather than specific vendors.
3. Connector plugins run inside a secure sandbox with decoupled authentication, rate limiting, and circuit breakers.

## Consequences
- Workflows and AI agents remain completely decoupled from third-party vendor APIs.
- Adding a new external integration requires authoring an isolated plugin without changing workflow engine core code.
- Enforces strict multi-tenant credential isolation and security boundaries.
