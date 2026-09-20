# ADR-008: OpenTelemetry Distributed Tracing Strategy

**Status**: **ACCEPTED**  
**Date**: 2026-08-19  

## 1. Context & Problem Statement
Trace end-to-end request flows across HTTP upload, message queue, worker pool, OCR engine, LLM provider, and database commit.

## 2. Decision Outcome
Propagate W3C trace headers (`X-Correlation-ID`, `X-Trace-ID`, `X-Span-ID`) across API middleware, broker message headers, worker contexts, and database event ledgers.

## 3. Consequences
- **Positive**: Complete end-to-end distributed trace graph visibility.
