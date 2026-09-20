# Certificate Authority & X.509 Lifecycle Guide

## 1. Trust Hierarchy & Trust Domain
- **Root CA**: Issues intermediate CA certificates and establishes cryptographic root of trust for the cluster domain (`docutask.internal`).
- **Workload Certificates**: Issued per service with short validity periods (default: 30 days) and SAN SPIFFE extensions.

## 2. Automated Certificate Rotation
```python
from app.infrastructure.networking.security import CertificateAuthorityManager

ca_mgr = CertificateAuthorityManager(trust_domain="docutask.internal")

# Issue workload certificate
cert = ca_mgr.issue_workload_certificate(
    service_name="document-ocr-worker",
    namespace="default",
    validity_days=30
)

# Rotate certificate
new_cert = ca_mgr.rotate_certificate(cert.serial_number)
```

## 3. Mutual TLS Peer Verification
```python
from app.infrastructure.networking.security import MTLSEngine

mtls = MTLSEngine(ca_mgr)
validation = mtls.validate_connection(client_cert, server_cert)
assert validation.is_valid is True
```
