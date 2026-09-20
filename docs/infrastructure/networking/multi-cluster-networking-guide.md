# Multi-Cluster & Multi-Region Hybrid Cloud Networking Guide

## 1. Multi-Cluster Topology
DocuTask Agent clusters across AWS (us-east-1, us-west-2), GCP (us-central1), and On-Premise datacenters participate in a unified service mesh topology:

```
┌───────────────────────────┐                ┌───────────────────────────┐
│ Region A (us-east-1)      │                │ Region B (us-west-2)      │
│ Cluster Alpha             │   mTLS Mesh    │ Cluster Beta              │
│ ┌───────────────────────┐ │   Tunnel       │ ┌───────────────────────┐ │
│ │ Service Ingestion     │◄├────────────────┼►│ Service Worker (Canary) │ │
│ └───────────────────────┘ │                │ └───────────────────────┘ │
└───────────────────────────┘                └───────────────────────────┘
```

## 2. Multi-Region Dynamic Resolution
`ServiceResolver` automatically routes to healthy regional clusters and falls back to remote regions if local instances fail:
```python
from app.infrastructure.networking.discovery import ServiceResolver, ServiceDiscoveryRegistry

registry = ServiceDiscoveryRegistry()
resolver = ServiceResolver(registry)

# Resolves local us-east-1 instance; if none healthy, automatically fails over to us-west-2
target = resolver.resolve("document-ocr-worker", caller_region="us-east-1")
```

## 3. Global Control Plane Synchronization
```python
from app.infrastructure.networking.control_plane import NetworkControlPlaneManager

manager = NetworkControlPlaneManager()
manager.register_cluster("cluster-alpha", region="us-east-1", mesh_type="istio")
manager.register_cluster("cluster-beta", region="us-west-2", mesh_type="linkerd")
clusters = manager.list_clusters()
```
