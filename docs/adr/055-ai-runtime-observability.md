# ADR-055 / ADR-948: AI Runtime & LLM Inference Observability Standard

## Status
Accepted

## Context
AI-powered document processing introduces non-deterministic model behaviors, token consumption costs, prompt injection risks, and fluctuating inference latencies (time-to-first-token, inter-token latency) that traditional infrastructure APMs cannot monitor.

## Decision
We implement dedicated AI runtime observability within `AIMetricCollector`, `Tracer`, and `ObservabilitySDK` capturing:
1. Model inference metrics: prompt tokens, completion tokens, total tokens, latency per token, time-to-first-token (TTFT).
2. Cost tracking: token cost attribution per tenant, model tier, and pipeline stage.
3. Model failure modes: context length overflow, rate limiting (429), temperature drifting, fallback provider switching.
4. Security & safety tracing: prompt injection scan latency, safety filter interventions, and moderation flags correlated with distributed trace spans.

## Consequences
- Transparent cost allocation across multi-tenant workloads.
- Granular bottleneck detection distinguishing LLM latency from application preprocessing/postprocessing.
- Full auditability and safety telemetry for enterprise compliance.
