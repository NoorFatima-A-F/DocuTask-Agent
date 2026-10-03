# ADR-041: Multi-Tenant Credential Isolation & Secret Management

## Status
Accepted

## Context
In a multi-tenant enterprise automation platform, storing credentials directly in workflows, task variables, prompts, or execution traces creates critical data breach risks and violates SOC2/ISO-27001 compliance requirements.

## Decision
We enforce a strict 5-tier isolation hierarchy:
$$\text{Organization} \longrightarrow \text{Workspace} \longrightarrow \text{Connector} \longrightarrow \text{Credential} \longrightarrow \text{SecretProvider}$$
Raw secrets are stored exclusively in dedicated KMS/Vault backends (`SecretProvider`), while the platform only stores non-sensitive metadata (`CredentialMetadata`). Plaintext credentials are only resolved just-in-time within the runtime sandbox for the duration of a network call.

## Consequences
- Workflows, prompts, and audit logs never contain plaintext keys or tokens.
- Complete tenant boundary isolation prevents cross-tenant credential access.
- Pluggable support for HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, and Azure Key Vault.
