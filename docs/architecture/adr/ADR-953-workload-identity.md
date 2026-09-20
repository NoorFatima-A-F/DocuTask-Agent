# ADR-953: SPIFFE/SPIRE-Compatible Workload Identity Architecture

## Status
Accepted

## Context
Service identities based on IP addresses, DNS hostnames, or static shared API tokens are vulnerable to spoofing, DNS hijacking, and token leakage. Ephemeral container lifecycles in Kubernetes make IP-based identity management fragile.

## Decision
We adopt the CNCF SPIFFE (Secure Production Identity Framework for Everyone) standard for all workloads:
1. Workloads are identified by SPIFFE IDs formatted as `spiffe://{trust_domain}/ns/{namespace}/sa/{service_account}`.
2. `WorkloadIdentityManager` issues cryptographic Software Verifiable Identity Documents (SVIDs) containing signed claims and TTLs.
3. SAN extensions in X.509 certificates embed the workload's SPIFFE ID for mTLS peer verification.

## Consequences
- Workload identity is decoupled from ephemeral IP addresses and host physical locations.
- Cryptographically verifiable identity assertion across clusters, regions, and clouds.
- Compatibility with external SPIRE agents and service mesh identity providers.
