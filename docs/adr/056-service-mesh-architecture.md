# ADR-056 / ADR-951: Vendor-Neutral Service Mesh Abstraction Layer

## Status
Accepted

## Context
DocuTask Agent operates across varied deployment targets: managed Kubernetes clusters (EKS, GKE, AKS), on-premise clusters, and standalone edge compute nodes. Hardcoding mesh-specific logic (Istio EnvoyFilters, Linkerd annotations, Consul intentions) creates platform lock-in and impedes portability.

## Decision
We implement a vendor-neutral service mesh abstraction anchored by `IServiceMeshAdapter`. Concrete adapters for Istio (`IstioMeshAdapter`), Linkerd (`LinkerdMeshAdapter`), Consul Connect (`ConsulMeshAdapter`), and a built-in Native mesh translate platform routing, traffic split, and mTLS security policies into provider-specific Custom Resource Definitions (CRDs).

## Consequences
- Zero vendor lock-in: application code interacts strictly with the platform `NetworkSDK`.
- Seamless portability across Istio, Linkerd, Consul, and cloud-native environments.
- Automated manifest generation for GitOps workflows and dynamic control plane reconciliation.
