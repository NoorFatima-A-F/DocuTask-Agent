# Enterprise Cluster Management Guide

## Overview
The DocuTask Agent Cluster Management Subsystem provides centralized lifecycle orchestration, capability indexing, and health lease management across multi-cloud and Kubernetes clusters.

## 12-State Cluster Lifecycle
Clusters progress through a deterministic state machine:
1. `DISCOVERED`: Cluster identity detected by discovery service.
2. `REGISTERING`: Registration payload received, identity validated.
3. `REGISTERED`: Cryptographic trust established, added to registry.
4. `VALIDATING`: Pre-flight connectivity, version, and policy verification.
5. `READY`: Validated and prepared for workload traffic.
6. `ACTIVE`: Actively serving tenant workloads and eligible for routing.
7. `DEGRADED`: One or more sub-components reporting degraded health.
8. `DRAINING`: Completing in-flight jobs without accepting new requests.
9. `MAINTENANCE`: Offline for upgrades or maintenance work.
10. `SUSPENDED`: Quarantined due to policy or security violations.
11. `OFFLINE`: Heartbeat lease expired or cluster unreachable.
12. `REMOVED`: Permanently decommissioned and deleted from active topology.

## Cluster Registration via SDK
```python
from app.infrastructure.sdk.clusters import ClusterSDK
from app.infrastructure.clusters.models import CapacityModel, ClusterType

sdk = ClusterSDK()
cluster = sdk.register_cluster(
    cluster_id="cls-us-east-1a",
    name="US East Primary Production",
    region_id="us-east-1",
    provider="kubernetes",
    cluster_type=ClusterType.PRODUCTION,
    capabilities={"gpu_a100", "nvme_ssd", "arm64"},
    capacity=CapacityModel(allocatable_cpu_cores=256.0, utilized_cpu_cores=32.0),
    labels={"tier": "high_throughput", "env": "prod"},
)
```
