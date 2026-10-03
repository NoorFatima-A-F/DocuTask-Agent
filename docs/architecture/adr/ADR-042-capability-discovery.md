# ADR-042: Technology-Independent Capability Discovery

## Status
Accepted

## Context
When workflows or autonomous agents need to send a message or upload a document, specifying concrete vendors (e.g. `gmail.send` or `slack.post`) tightly couples business logic to specific providers and breaks dynamic failover if a vendor experiences an outage.

## Decision
We implement a `CapabilityRegistry` that indexes high-level, technology-independent capabilities (`email.send`, `message.send`, `storage.upload`, `crm.contact.create`). When an execution requests a capability, the runtime dynamically resolves the optimal provider connector based on tenant preference, regional compliance, cost, and live health status.

## Consequences
- Business workflows become vendor-agnostic and resilient to provider outages.
- Agents can switch communication channels or storage providers dynamically without reprogramming.
- Enables seamless fallback to alternative providers (e.g. SMTP if SendGrid is degraded).
