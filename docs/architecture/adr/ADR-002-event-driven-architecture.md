# ADR-002: CloudEvents 1.0 Distributed Event-Driven Architecture

## Status
**ACCEPTED** (Date: 2026-09-18)

## Context
Asynchronous workflow steps, agent task dispatches, external webhook ingestion, and real-time observability telemetry require high-throughput, low-latency, decoupled communication across services without blocking synchronous HTTP request threads.

## Decision
We standardize on an **Event-Driven Architecture (EDA)** using the **CNCF CloudEvents 1.0** specification over an Apache Kafka / RabbitMQ event mesh. All state changes emit immutable event envelopes containing correlation IDs, tenant contexts, actor metadata, and typed payloads across 9 standardized event categories.

## Alternatives Considered
1. **Synchronous REST-Only Callbacks**: Vulnerable to cascading failures, thread pool starvation, and lost requests during network timeouts.
2. **Proprietary Internal Event Dicts**: Lacks industry standardization, making third-party webhook integrations and multi-language consumer clients difficult.

## Trade-offs
- **Pros**: Complete decoupling of producers and consumers, guaranteed at-least-once delivery, replayability, natural integration with audit vaults.
- **Cons**: Eventual consistency requires idempotent consumer handlers and compensation rollback logic for failed distributed transactions.

## Consequences
- Every message handler must be idempotent using `event_id` deduplication.
- Dead-Letter Queues (DLQs) and automated retry policies must be configured for all subscribers.
