# Cluster Health and Diagnostics Guide

## Heartbeat Leases and Sub-Component Health
Clusters periodically send heartbeats containing telemetry for 9 critical subsystems:
- Node
- Service
- Worker
- Queue
- Database
- Cache
- Storage
- Network
- Telemetry

If any subsystem reports `DEGRADED`, the cluster health transitions to `DEGRADED` and SRE alert events are published. If heartbeats lapse beyond the lease TTL, the cluster is automatically marked `UNREACHABLE`.

## Generating Diagnostics Snapshot
```python
from app.infrastructure.sdk.clusters import ClusterSDK

sdk = ClusterSDK()
report = sdk.get_cluster_diagnostics("cls-us-east-1a")
print("Cluster Health:", report["health_status"])
print("Capacity:", report["capacity"])
```
