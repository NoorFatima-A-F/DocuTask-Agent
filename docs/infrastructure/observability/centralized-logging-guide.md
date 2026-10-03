# Centralized Logging & Inverted Search Guide

## 1. Structured Log Model & Severity Hierarchy
Log records follow the `LogRecord` format, using 8 severity levels:
`TRACE` (0) -> `DEBUG` (1) -> `INFO` (2) -> `NOTICE` (3) -> `WARN` (4) -> `ERROR` (5) -> `CRITICAL` (6) -> `FATAL` (7).

```json
{
  "timestamp": "2026-09-19T14:30:00.123456Z",
  "level": "ERROR",
  "service": "document-pipeline-worker",
  "message": "Failed to parse OCR response from provider",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "tenant_id": "tenant-corp",
  "error_type": "ProviderTimeoutError",
  "stack_trace": "Traceback (most recent call last)...",
  "attributes": {"attempt": 3, "endpoint": "https://api.vision.internal/v1"}
}
```

## 2. Inverted Index Search
The `LogIndex` powers sub-millisecond querying without requiring full log scans:
```python
from app.infrastructure.observability.logs import LogIndex, LogLevel

index = LogIndex()
index.index_record(record)

results = index.search(
    tenant_id="tenant-corp",
    service="document-pipeline-worker",
    min_level=LogLevel.WARN,
    query="OCR timeout",
    limit=50
)
```

## 3. Retention Policies & Legal Holds
`LogRetentionManager` applies tier-based retention with legal hold immutability:
- **Hot Tier**: 7 days (in-memory & NVMe cache)
- **Warm Tier**: 30 days (distributed object storage)
- **Cold Tier**: 365 days (compressed archival)
- **Legal Hold**: Indefinite freeze preventing any log deletion during investigations.
