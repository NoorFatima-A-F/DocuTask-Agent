# Multi-Tenant Regional Isolation Guide

## Tenant Affinity & Boundaries
DocuTask Agent enforces strict tenant isolation policies across global regions and dedicated clusters.

```python
from app.infrastructure.sdk.clusters import ClusterSDK
from app.infrastructure.regions.affinity import TenantAffinityRule

sdk = ClusterSDK()

# Restrict healthcare tenant strictly to US regions with exclusive isolation
sdk.set_tenant_affinity(
    TenantAffinityRule(
        tenant_id="healthcare-corp",
        allowed_region_ids=["us-east-1", "us-west-2"],
        pinned_region_id="us-east-1",
        exclusive=True,
        required_jurisdiction="US",
    )
)
```
