# Control Plane Operations Guide

## Architectural Hierarchy
1. **Global Control Plane (`GlobalControlPlane`)**: Coordinates global cluster registrations, syncs regional control planes, advances global epochs, and exposes global topology snapshots.
2. **Regional Control Plane (`RegionalControlPlane`)**: Governs local cluster admission, runs intra-region reconciliation loops, monitors heartbeat leases, and maintains regional availability during global partition events.

## Global Topology Snapshot
```python
from app.infrastructure.sdk.clusters import ClusterSDK

sdk = ClusterSDK()
topology = sdk.get_global_topology()
print("Active Regions:", topology["global_state"]["active_regions_count"])
print("Total Clusters:", topology["global_state"]["total_clusters_count"])
```
