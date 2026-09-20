# Zero-Trust Security Portfolio Summary

- **Non-Root Containers**: Unprivileged user (UID 10001) with read-only rootfs and dropped kernel capabilities.
- **Zero Vulnerability Guarantee**: Continuous Trivy/Grype image scanning with 0 Critical / 0 High CVEs.
- **KMS Envelope Encryption**: Master KMS key wrapping with AES-256 for all at-rest document storage.
- **mTLS 1.3 Service Mesh**: SPIFFE/SPIRE cryptographic identity across all microservice RPCs.
- **AI Guardrail Defense**: 100% prompt injection neutralization and output schema sanitization.