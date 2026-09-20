# 93. OCI Artifact Strategy & Referrers Model

Date: 2026-09-20

## Status
Accepted

## Context
Standardizing artifact distribution around OCI v1.1 image and distribution specifications enables vendor-neutral multi-cloud distribution across GHCR, Google Artifact Registry, Amazon ECR, Azure Container Registry, and Harbor.

## Decision
We implement `OCIRegistryAdapter` supporting OCI v1.1 referrers. Artifacts, SBOMs, signatures, and provenance attestations are distributed as OCI artifacts linked by content-addressed digests (`sha256:...`).

## Consequences
- Single unified registry protocol for container images, Helm packages, workflow packages, agent packages, and prompt bundles.
- Eliminates reliance on proprietary packaging formats.
