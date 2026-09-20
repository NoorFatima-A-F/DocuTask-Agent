# DocuTask Agent: Enterprise Service Mesh Operations Guide

## 1. Overview
The DocuTask Service Mesh (`app/networking/`) provides a vendor-neutral, zero-trust communication fabric for internal microservices, AI workers, and data governance pipelines.

---

## 2. Core Capabilities

### 2.1 Identity & mTLS 1.3
- **SPIFFE ID Standard**: `spiffe://docutask.internal/ns/{namespace}/sa/{service_name}`.
- **Mutual Authentication**: Strict TLS 1.3 cipher suite validation (`TLS_AES_256_GCM_SHA384`).
- **Auto-Rotation**: X.509 SVIDs rotated transparently before expiration.

### 2.2 Traffic Steering & Progressive Delivery
- **Canary Splits**: Weight-based distribution across service versions.
- **Shadow Mirroring**: Asynchronous non-blocking dark traffic replication.
- **Locality Routing**: Zone-aware endpoint selection with regional fallback.

### 2.3 Resilience & Chaos Engineering
- **Circuit Breakers**: Sliding window state machine (Closed, Open, Half-Open).
- **Exponential Retries**: Full jitter backoff algorithm preventing thundering herds.
- **Fault Injection**: Synthetic latency and error abort injection for chaos drills.

---

## 3. SDK Quickstart

```python
from app.networking.sdk import MeshClient

client = MeshClient(service_name="document-orchestrator", namespace="default")

response = client.call(
    target_service="ocr-engine",
    action="extract_text",
    payload={"doc_id": "doc-9941", "tier": "high"},
    timeout_ms=3000.0,
)

if response.status_code == 200:
    print("Success:", response.payload)
else:
    print("Failed:", response.error_message)
```
