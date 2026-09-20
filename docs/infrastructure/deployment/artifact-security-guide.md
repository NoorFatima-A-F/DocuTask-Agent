# Software Supply Chain & Artifact Security Guide

## 1. Supply Chain Security Principles
- **Immutable Digests**: Artifacts are referenced strictly by cryptographic SHA-256 digest, never mutable tags.
- **Software Bill of Materials (SBOM)**: Every build exports an SBOM detailing all direct and transitive dependencies.
- **Cryptographic Attestation**: Artifact digests and provenance are signed using `ArtifactSigner`.
- **Zero Critical Vulnerabilities**: Promotion to production fails if any CRITICAL or HIGH CVEs exist.

## 2. Registering and Signing Artifacts
```python
from app.infrastructure.deployment.artifacts import ArtifactRegistry, ArtifactType, SBOMComponent

registry = ArtifactRegistry()
sbom = [SBOMComponent(name="pydantic", version="2.7.0", purl="pkg:pypi/pydantic@2.7.0")]

artifact = registry.register_artifact(
    name="docutask-ocr",
    version="1.2.0",
    artifact_type=ArtifactType.CONTAINER_IMAGE,
    commit_sha="commit-778899",
    sbom=sbom,
    auto_sign=True,
)
```
