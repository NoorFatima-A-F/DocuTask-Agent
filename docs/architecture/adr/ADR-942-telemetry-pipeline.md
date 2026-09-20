# ADR-942: Centralized Telemetry Pipeline & Context Management

## Status
Accepted

## Context
High-throughput services produce large volumes of telemetry data (metrics, logs, traces, profile records). Without a centralized pipeline, telemetry collection blocks critical path executions, risks leaking PII / secrets, and lacks unified context propagation.

## Decision
We implement a non-blocking `TelemetryCollectorPipeline` coupled with context variable-backed `TelemetryContext` and `TelemetrySDK`. The pipeline enforces:
1. Asynchronous batching with size and duration-based flushing.
2. Built-in PII and secret redaction (`mask_sensitive_data` covering SSNs, credit cards, emails, passwords, bearer tokens, API keys).
3. Automatic enrichment with cluster, region, host, tenant, and trace context.
4. Pluggable exporters supporting in-memory buffers and OpenTelemetry Protocol (OTLP) JSON format.

## Consequences
- Guaranteed zero PII / secret leakage in logs and telemetry payloads.
- High-efficiency batching minimizes network I/O and overhead on worker nodes.
- Thread and async-task safe contextual correlation across concurrent requests.
