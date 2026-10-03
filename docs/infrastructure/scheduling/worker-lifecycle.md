# Worker Lifecycle and Registration Guide

## 11-State Worker Lifecycle
Workers transition through 11 governed states:
1. `DISCOVERED`: Identity reported.
2. `REGISTERING`: Registration payload received, identity authenticated.
3. `REGISTERED`: Capabilities indexed, lease issued.
4. `AVAILABLE`: Ready to accept workload assignments.
5. `RESERVED`: Capacity reserved for an imminent assignment.
6. `ASSIGNED`: Assignment dispatched, awaiting worker ACK.
7. `RUNNING`: Actively executing tasks.
8. `DRAINING`: Node undergoing graceful drain; no new tasks accepted.
9. `UNAVAILABLE`: Missed heartbeats or quarantined.
10. `RECOVERING`: Undergoing health validation before re-admission.
11. `TERMINATED`: Decommissioned.

## Registering a Worker via SDK
```python
from app.infrastructure.sdk.scheduling import WorkerSDK
from app.infrastructure.workers.models import ResourceCapacity, WorkerType

sdk = WorkerSDK()
worker = sdk.register_worker(
    worker_id="wrk-ocr-01",
    region_id="us-east-1",
    cluster_id="cls-us-1",
    worker_type=WorkerType.OCR,
    capabilities={"document.ocr", "gpu.cuda", "gpu.t4"},
    resource_capacity=ResourceCapacity(cpu_cores=16.0, memory_gb=64.0, gpu_count=2),
    concurrency_limit=20,
)
```
