# ADR-032: Multi-Agent Message Bus & Communication Protocol

## Status
Accepted

## Context
Direct agent-to-agent remote procedure calls or tight object couplings create brittle architectures, prevent observation, bypass security policies, and inhibit asynchronous collaboration. Multi-agent communication must be decoupled, asynchronous, priority-aware, and fully auditable.

## Decision
We implement `AgentMessageBus` supporting 11 formal message types:
`COMMAND`, `REQUEST`, `RESPONSE`, `PROPOSAL`, `DECISION`, `EVIDENCE`, `ARTIFACT`, `ERROR`, `HEARTBEAT`, `CANCELLATION`, `APPROVAL`.

Every `AgentMessage` contains:
- Unique message ID, sender, receiver (or wildcard `*` for broadcast).
- Priority tier (`CRITICAL`, `HIGH`, `NORMAL`, `LOW`).
- Distributed `trace_id` for end-to-end telemetry.
- TTL (time-to-live) and structured payload dictionary.

Agents interact exclusively via mailboxes, topic subscriptions, and message queues on the `AgentMessageBus`.

## Consequences
- Guarantees complete observability, replayability, and isolation between collaborating agents.
- Enables seamless integration of supervisor orchestration, worker dispatch, and human approval events.
