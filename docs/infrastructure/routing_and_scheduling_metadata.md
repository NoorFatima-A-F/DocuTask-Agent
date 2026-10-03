# Routing and Scheduling Metadata Guide

## Workload Routing Evaluation
Workloads demand specific runtime resources, geographic boundaries, compliance profiles, and hardware capabilities.

```python
from app.infrastructure.sdk.clusters import ClusterSDK
from app.infrastructure.routing.metadata import WorkloadRoutingRequest

sdk = ClusterSDK()
req = WorkloadRoutingRequest(
    tenant_id="enterprise-tenant-1",
    workload_type="ocr",
    required_jurisdiction="US",
    required_capabilities={"gpu_t4", "nvme_ssd"},
    min_cpu_cores=4.0,
    min_memory_gb=16.0,
    labels_selector={"env": "prod"},
)

decision = sdk.evaluate_routing(req)
if decision.is_routable:
    print(f"Routing to Cluster: {decision.selected_cluster_id} in Region: {decision.selected_region_id}")
else:
    print(f"Rejections: {decision.rejection_reasons}")
```
