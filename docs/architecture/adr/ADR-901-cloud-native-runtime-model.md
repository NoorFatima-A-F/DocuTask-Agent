# ADR-901: Cloud-Native Runtime Model

## Context
DocuTask Agent requires a unified runtime lifecycle engine to deploy, start, stop, restart, and monitor microservices across diverse cloud and hybrid infrastructures. Without a centralized runtime model, service processes and containers have inconsistent lifecycles and recovery behaviors.

## Decision
Introduce `InfrastructureRuntime` governed by a strict 9-state state machine (`CREATED` -> `INITIALIZING` -> `STARTING` -> `RUNNING` -> `DEGRADED` -> `STOPPING` -> `STOPPED` -> `FAILED` -> `RECOVERING`). All services report status and support automatic self-healing recovery loops.

## Status
Accepted

## Consequences
- Uniform service lifecycle and automated recovery across Kubernetes, AWS, GCP, Azure, and local runtimes.
- Deterministic state management preventing zombie or orphan processes.
