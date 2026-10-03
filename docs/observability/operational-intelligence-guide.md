# DocuTask Agent: Operational Intelligence & SRE Platform Guide

## 1. Overview
The DocuTask Observability Platform (`app/observability/`) provides full-stack operational intelligence, SRE automation, and reliability engineering across all platform layers.

---

## 2. Core Pillars

### 2.1 Multidimensional Telemetry Context
Every log, metric, trace span, and event includes universal execution context:
```python
from app.observability.core import ObservabilityContext, set_current_context

ctx = ObservabilityContext(
    tenant_id="tenant-acme",
    service_name="ocr-engine",
    workflow_id="wf-992",
    agent_id="agent-classifier",
)
set_current_context(ctx)
```

### 2.2 Metrics & Golden Signals
- **Infrastructure**: Node CPU, Memory, Disk, Container Health.
- **Runtime**: Worker Count, Queue Depth, Processing Rate.
- **AI Execution**: Model Latency, Token Usage, Hallucination Rate, Evaluation Scores.

### 2.3 Distributed Tracing & Continuous Profiling
- OpenTelemetry W3C `traceparent` propagation across service boundaries.
- Continuous latency profiling & flamegraph hotspot detection.

### 2.4 Incident Response & Closed-Loop Self-Healing
- Formal incident state machine (`DETECTED` -> `RESOLVED` -> `POSTMORTEM`).
- Automated self-healing actions: Worker scaling, rolling restarts, queue draining.
- Automated blameless postmortem generation with 5-Whys.

---

## 3. Developer SDK Quickstart

```python
from app.observability.sdk import ObservabilitySDK, trace, metric_counter, profile

sdk = ObservabilitySDK(service_name="document-pipeline")

@trace(operation="agent.reasoning")
@profile(block_name="ai.inference")
@metric_counter(name="agent_executions_total")
def execute_agent_step(doc_id: str):
    # Business logic here
    sdk.logger.info("Executing agent reasoning step", doc_id=doc_id)
    return {"status": "success", "doc_id": doc_id}
```
