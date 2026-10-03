# ADR-902: Provider Abstraction Strategy

## Context
Directly embedding cloud provider SDKs (boto3, google-cloud, azure-sdk, kubernetes client) in application or agent code creates strong vendor lock-in, complicates testing, and prevents deployment in air-gapped or on-premises environments.

## Decision
Create provider-neutral abstraction interfaces (`ComputeProvider`, `StorageProvider`, `NetworkProvider`, `SecretProvider`) implemented by specialized adapters (`Kubernetes`, `AWS`, `GCP`, `Azure`, `Local`). Application and agent runtimes interact exclusively through these interfaces.

## Status
Accepted

## Consequences
- Total cloud portability across multi-cloud, hybrid, and air-gapped topologies.
- Easy local mocking and fast deterministic unit/integration testing.
