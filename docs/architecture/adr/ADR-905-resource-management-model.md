# ADR-905: Resource Management Model

## Context
Platform workloads consume diverse resource categories including compute (containers, VMs, serverless), storage (databases, object buckets, caches, volumes), and networking (load balancers, service mesh endpoints).

## Decision
Introduce `ResourceManager` managing resource specifications through a 7-stage lifecycle state machine (`REQUESTED` -> `ALLOCATING` -> `READY` -> `ACTIVE` -> `DRAINING` -> `RELEASED` -> `FAILED`). Resources are decoupled from underlying cloud provider implementation details.

## Status
Accepted

## Consequences
- Unified provisioning, lifecycle management, and graceful draining across all infrastructure resources.
- Complete inventory visibility across cloud environments.
