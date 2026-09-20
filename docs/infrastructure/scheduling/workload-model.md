# Workload Model and Execution Contracts

## Generic Workload Definition
All work across the platform (workflows, agents, OCR, embeddings, connectors) is modeled via `WorkloadRequest`:

```python
from app.infrastructure.executions.workload import (
    ResourceRequirements,
    WorkloadPriority,
    WorkloadRequest,
    WorkloadType,
)

req = WorkloadRequest(
    workload_id="wkl-ocr-100",
    workload_type=WorkloadType.OCR_JOB,
    tenant_id="enterprise-tenant-1",
    priority=WorkloadPriority.HIGH,
    required_capabilities={"document.ocr", "gpu.cuda"},
    resource_requirements=ResourceRequirements(cpu_cores=4.0, memory_gb=16.0, gpu_count=1),
    region_preferences=["us-east-1", "us-west-2"],
    required_jurisdiction="US",
    data_locality_uri="s3://docutask-us-east-1-data/invoice.pdf",
    idempotency_key="idem-ocr-100",
)
```
