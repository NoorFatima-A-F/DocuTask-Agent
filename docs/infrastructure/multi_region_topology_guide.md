# Multi-Region Topology Guide

## Overview
DocuTask Agent supports globally distributed deployments partitioned into distinct jurisdictional regions with data residency enforcement, latency-based routing, and cross-region egress controls.

## Region Registration & Jurisdictions
Each region is defined with a sovereign data residency jurisdiction (e.g. `US`, `EU`, `APAC`, `GLOBAL`).

```python
from app.infrastructure.sdk.clusters import ClusterSDK
from app.infrastructure.regions.models import Geography

sdk = ClusterSDK()
sdk.register_region(
    region_id="eu-west-1",
    name="eu-west-1",
    display_name="Europe (Ireland)",
    provider="aws",
    data_residency_jurisdiction="EU",
    is_primary=False,
    routing_priority=20,
    geography=Geography(continent="Europe", country="IE", jurisdiction="EU"),
    failover_region_id="eu-central-1",
)
```

## Egress Controls
Data residency policy engines verify that documents classified under strict jurisdictions (such as EU GDPR) cannot egress to foreign jurisdictions unless an authorized encrypted egress gateway is present.
