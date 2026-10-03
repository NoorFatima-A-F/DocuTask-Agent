# ADR 072: Service Mesh Architecture & Decentralized Data Plane

## Status
Accepted

## Context
DocuTask Agent operates across distributed multi-cluster environments requiring secure, resilient, and observable service-to-service communication. Point-to-point hardcoded HTTP calls lack centralized policy enforcement, unified telemetry, identity attestation, and dynamic traffic steering.

## Decision
Adopt a centralized Mesh Control Plane (`ServiceMeshController`) paired with sidecar proxy interceptors (`DataPlaneInterceptor`, `ServiceProxy`) running alongside service workloads. The data plane intercepts all inbound and outbound traffic, applying identity verification, mTLS encryption, traffic policies, resilience retries/circuit breakers, and telemetry collection transparently.

## Consequences
- **Positive**: Decouples application logic from networking concerns, enables dynamic reconfiguration without downtime, and standardizes security/telemetry.
- **Negative**: Adds slight processing overhead per hop (mitigated by zero-allocation buffers and in-memory caches).
