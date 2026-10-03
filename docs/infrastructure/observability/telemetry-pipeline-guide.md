# Telemetry Pipeline & Context Propagation Operational Guide

## 1. Context Structure & Correlated Metadata
Every execution context within DocuTask Agent maintains a `TelemetryContext` stored inside a Python `contextvar`.

```python
from app.infrastructure.observability.telemetry import TelemetryContext, get_current_context, set_current_context

ctx = TelemetryContext(
    trace_id="4bf92f3577b34da6a3ce929d0e0e4736",
    span_id="00f067aa0ba902b7",
    tenant_id="tenant-enterprise-01",
    service_name="doc-processor-worker",
    region="us-east-1",
    cluster_id="cluster-prod-alpha",
    user_id="usr_892341",
    attributes={"workflow_id": "wf_ocr_v2"}
)
token = set_current_context(ctx)
```

## 2. Sensitive Data & PII Redaction
The pipeline automatically scrubs sensitive data across logs and telemetry attributes via `mask_sensitive_data`:
- **Social Security Numbers (SSN)**: `\b\d{3}-\d{2}-\d{4}\b` -> `[REDACTED_SSN]`
- **Credit Card Numbers**: 16-digit patterns -> `[REDACTED_CC]`
- **Email Addresses**: User emails -> `[REDACTED_EMAIL]`
- **Bearer Tokens / API Keys**: Authorization headers -> `[REDACTED_TOKEN]`
- **Passwords**: `password=...` / `"password": "..."` -> `[REDACTED_PASSWORD]`

## 3. Telemetry Collector Pipeline Configuration
```python
from app.infrastructure.observability.telemetry import (
    TelemetryCollectorPipeline,
    InMemoryExporter,
    OTLPJsonExporter
)

exporter = OTLPJsonExporter(endpoint="https://otlp.collector.internal:4318/v1/traces")
pipeline = TelemetryCollectorPipeline(
    exporter=exporter,
    batch_size=1000,
    flush_interval_seconds=5.0,
    mask_pii=True
)
pipeline.start()
```
