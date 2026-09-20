# Architecture Decision Record: ADR-006

## Title
Workflow Engine Architecture: Declarative DAG Orchestration, Durable State Machines, and Distributed Saga Compensations

## Status
**ACCEPTED** (2026-03-24)

## Context
DocuTask Agent executes mission-critical business workflows that coordinate document ingestion, optical character recognition (OCR), AI extraction, cross-document reconciliation, human review approvals, and transactional synchronization with external enterprise systems (SAP, Salesforce, Workday).

Document workflows in enterprise environments have unique operational characteristics:
1. **Long-Running Durability**: Workflows may span milliseconds (instant API document classification) or weeks (human-in-the-loop review, multi-party compliance approvals). State must survive worker crashes, deployments, and infrastructure restarts.
2. **Distributed Transactions & Failures**: A workflow may successfully create an invoice record in an ERP system but fail during payment gateway scheduling. Standard database ACID transactions cannot span heterogeneous third-party SaaS APIs.
3. **Complex Control Flows**: Enterprise processes require parallel fan-out/fan-in, conditional branching, dynamic sub-workflows, deterministic retries, timeouts, and human escalation gates.
4. **Declarative Transparency**: Enterprise business analysts and auditors need human-readable, auditable workflow definitions (YAML/JSON) rather than opaque, imperative hardcoded scripts.

DocuTask Agent requires a durable, deterministic, and declarative workflow engine supporting distributed Saga compensations.

---

## Decision

We adopt a **Declarative DAG Workflow Engine with Durable Event-Sourced State Machines and Distributed Saga Compensations**:

### 1. Declarative Workflow Specification (DocuTask Workflow DSL)
Workflows are defined as versioned declarative YAML/JSON artifacts structured into 5 hierarchical levels:
```
Pipeline -> Phase -> Step -> Task -> Action
```
Each step specifies:
- `id` and `type` (`agent_task`, `connector_action`, `human_review`, `conditional_switch`, `parallel_fork`, `sub_pipeline`)
- Input/Output data mapping using JSONPath expressions
- Pre-conditions and post-conditions
- Retry policies (`max_attempts`, `backoff_coefficient`, `retryable_errors`)
- Timeout deadlines
- **Compensation Action** (for transactional rollback).

### 2. Durable State Machine & Checkpointing
- Every state transition in a workflow execution is recorded as an immutable, append-only event in the PostgreSQL event log (`workflow_state_events`).
- Before executing any external side-effect (API call, email, agent dispatch), the engine commits a durable checkpoint.
- If a worker node crashes mid-execution, an idle standby worker resumes the workflow from the exact last acknowledged checkpoint without re-running completed idempotent side-effects.

### 3. Distributed Saga Orchestration & Automatic Rollback
To maintain distributed consistency across external enterprise systems without two-phase commit (2PC):
- Every forward mutating step (e.g., `create_erp_vendor_bill`) defines a paired compensation step (e.g., `cancel_erp_vendor_bill`).
- If an unrecoverable failure occurs at step $N$, the workflow engine initiates a **Saga Rollback**, executing compensations in reverse order ($N-1 \rightarrow N-2 \rightarrow \dots \rightarrow 1$).
- Rollback progress, compensation errors, and escalation alerts are tracked durably with full audit traceability.

### 4. Native Human-in-the-Loop (HITL) Suspensions
- When a workflow encounters an ambiguous document or low confidence score below workspace thresholds, it transitions into a `SUSPENDED_WAITING_FOR_HUMAN` state.
- System resources (threads/connections) are fully released.
- Upon human resolution via the Review UI or email callback, a resume event re-hydrates the workflow state and continues DAG execution.

---

## Consequences

### Positive
- **Fault-Tolerant Reliability**: Zero workflow state loss across infrastructure crashes, database failovers, or rolling platform upgrades.
- **Distributed Consistency**: Automatic Saga compensation ensures external systems are never left in inconsistent, half-processed states.
- **Auditable Compliance**: Complete visual, step-by-step audit logs satisfying SOC 2 and ISO 9001 quality management auditing.
- **Developer & User Ergonomics**: Declarative YAML workflows enable low-code visual workflow authoring, automated linting, and CI/CD version control.

### Negative / Trade-Offs
- **Storage Amplification**: Fine-grained event-sourced checkpointing increases database I/O and storage growth; managed retention policies and automated state compression are required for historical executions.
- **Compensation Authoring Discipline**: Developers and integration authors must implement and test idempotent compensation handlers for all state-mutating actions.

---

## Alternatives Considered

1. **Imperative In-Memory Execution (Celery / Asyncio Tasks)**: Rejected due to inability to survive worker restarts during long-running human review suspensions, and lack of deterministic rollback mechanisms.
2. **Third-Party External Engines (Temporal.io / Camunda)**: Evaluated; while robust, external orchestration engines introduce significant deployment footprints, complex proprietary clustering dependencies, and impedance mismatches with our 7-tier tenant PostgreSQL RLS security model. A lightweight, embedded native state machine on PostgreSQL + Redis delivers superior tenant-scoped isolation.
