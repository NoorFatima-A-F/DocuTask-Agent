# ADR-944: Centralized Structured Logging & Inverted Search Strategy

## Status
Accepted

## Context
Unstructured text logs are difficult to parse, search, aggregate, and correlate with distributed traces. High log volumes in production systems can overwhelm disk I/O, expose sensitive compliance data, or make querying slow during active incident response.

## Decision
We implement a JSON-structured logging subsystem centered around `LogRecord` and `LogIngestionPipeline` featuring:
1. Standardized log severity hierarchy (8 levels: `TRACE`, `DEBUG`, `INFO`, `NOTICE`, `WARN`, `ERROR`, `CRITICAL`, `FATAL`).
2. Automatic data masking for credentials, tokens, PII, and financial identifiers.
3. In-memory inverted search index (`LogIndex`) enabling sub-millisecond filtering across tenant ID, service, trace ID, log level, time range, and tokenized keywords.
4. Policy-driven retention management (`LogRetentionManager`) with legal hold freeze capabilities for regulatory compliance.

## Consequences
- Guaranteed structured JSON output for all logs.
- Direct correlation between log entries and tracing spans via `trace_id` and `span_id`.
- Granular retention rules per environment and severity tier, with legal hold protections.
