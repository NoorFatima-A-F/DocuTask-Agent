# ADR-955: Declarative Network Policy & Multi-Tenant Segmentation

## Status
Accepted

## Context
Multi-tenant compliance requirements (SOC2, ISO 27001, HIPAA) mandate strict network segmentation to ensure tenant data isolation, namespace boundaries, and egress restrictions to external third-party services.

## Decision
We implement a declarative network policy framework:
1. `NetworkPolicy` and `NetworkPolicyRule` models defining ingress and egress filtering across namespaces, CIDR IP ranges, ports, and protocols.
2. `IngressPolicyManager` generating isolated virtual networks for each tenant namespace.
3. `EgressPolicyManager` enforcing allowlisting on all outbound external API calls (e.g. OpenAI, Anthropic, Gemini, S3/GCS).

## Consequences
- Guaranteed tenant isolation at the networking layer.
- Protection against SSRF (Server-Side Request Forgery) and data exfiltration by blocking unapproved egress destinations.
- Declarative policy distribution to underlying Kubernetes NetworkPolicies or cloud security groups.
