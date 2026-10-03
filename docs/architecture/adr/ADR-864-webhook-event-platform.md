# ADR-864: Webhook and Event Subscription Platform

## Context
Asynchronous events such as policy violations, risk detections, and human approval requests must be dispatched to third-party enterprise tools (SIEMs, Slack, GRC platforms) reliably and securely.

## Decision
Implement a multi-tenant Webhook Dispatcher and in-process event subscription platform. Outbound webhooks sign all payloads using HMAC-SHA256 (`X-Governance-Signature`) and support automatic retry backoff and delivery attempt logging.

## Status
Accepted

## Consequences
- Real-time notification of security and compliance officers upon policy violations.
- Tamper-proof payload verification for external webhook consumers.
