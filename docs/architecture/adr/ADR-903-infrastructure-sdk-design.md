# ADR-903: Infrastructure SDK Design

## Context
Developers, automation workflows, and internal services need a unified, typed Python SDK to provision resources, deploy services, check diagnostics, and fetch credentials safely.

## Decision
Provide `InfrastructureSDK` encapsulating runtime deployments, resource provisioning, health checks, and secret access. All actions automatically emit domain events and immutable audit records.

## Status
Accepted

## Consequences
- Single entrypoint for all infrastructure operations.
- Built-in audit traceability for all infrastructure provisioning and modifications.
