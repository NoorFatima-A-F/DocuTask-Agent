# Architecture Decision Record: ADR-008

## Title
Cloud-Native Production Deployment: Kubernetes Topology, Node Pool Isolation, GitOps, and Multi-Region Disaster Recovery

## Status
**ACCEPTED** (2026-03-24)

## Context
DocuTask Agent is designed to operate as a high-availability, highly resilient multi-tenant enterprise platform deployable across public cloud providers (AWS, GCP, Azure), sovereign private clouds, and on-premise air-gapped data centers.

Enterprise platform operations require:
1. **Heterogeneous Workload Characteristics**: The platform runs diverse compute workloads: low-latency web/API services (FastAPI/React), CPU-intensive document rendering/OCR engines, memory-intensive vector indexing, and GPU-accelerated local AI inference.
2. **Workload Interference & Resource Starvation**: Heavy OCR batch processing or agent reasoning loops must never starve critical customer-facing API endpoints or real-time webhooks.
3. **Disaster Recovery (DR) & Business Continuity**: Enterprise SLAs mandate RTO (Recovery Time Objective) < 15 minutes and RPO (Recovery Point Objective) < 1 minute during regional cloud outages.
4. **Automated Infrastructure Governance**: Infrastructure must be 100% declarative, auditable, and managed through GitOps (ArgoCD / Terraform) with zero manual console intervention.

DocuTask Agent requires a cloud-native deployment topology that ensures compute isolation, rapid autoscaling, continuous delivery, and robust disaster recovery.

---

## Decision

We adopt a **Cloud-Native Kubernetes Topology with Dedicated Node Pools, Helm Packaging, ArgoCD GitOps, and Multi-Region Active-Passive Disaster Recovery**:

### 1. Dedicated Kubernetes Node Pools
Compute infrastructure is segmented into four dedicated, tainted node pools:
1. **Core Services Pool (`pool-core`)**: General compute (e.g., `c6i.2xlarge`) running API Gateways, Identity Services, Web UIs, and Orchestration Controllers.
2. **AI & Agent Worker Pool (`pool-agents`)**: High-CPU/Memory compute (e.g., `c6i.4xlarge`) running autonomous agent reasoning loops, sandbox containers, and workflow state engines.
3. **Document & OCR Compute Pool (`pool-ocr`)**: Burst-optimized compute (e.g., `c6i.8xlarge`) dedicated to high-throughput PDF rasterization, image preprocessing, and OCR extraction.
4. **GPU Inference Pool (`pool-gpu`, Optional/Sovereign)**: GPU-accelerated nodes (e.g., `g5.2xlarge` / NVIDIA A10G) running local vLLM / TensorRT model inference for air-gapped deployments.

### 2. Autonomous Autoscaling & Elasticity
- **Horizontal Pod Autoscaling (HPA)**: API and Agent pods scale dynamically based on custom Prometheus metrics (e.g., `http_requests_per_second`, `agent_active_sessions`).
- **KEDA (Kubernetes Event-driven Autoscaling)**: Worker pools scale based on Redis/RabbitMQ queue depths (`workflow_task_queue_depth`, `document_ingestion_queue_depth`), scaling from 0 to 500+ workers within 45 seconds.

### 3. Declarative GitOps Delivery (ArgoCD + Helm)
- All platform infrastructure is declared as version-controlled Terraform modules.
- Application deployments, configurations, network policies, and RBAC rules are packaged as versioned Helm charts and continuously synchronized via **ArgoCD**.
- Zero direct `kubectl` write access in production environments.

### 4. Multi-Region Disaster Recovery (Active-Passive with Hot Standby)
- **Primary Region (Active)**: Handles 100% of live traffic and active workflow execution.
- **Secondary Region (Hot Standby)**:
  - Database: Asynchronous streaming replication with PostgreSQL replication slots (RPO < 12s).
  - Storage: S3 Cross-Region Replication (CRR) for document blobs and vector index snapshots.
  - Compute: Minimal standby cluster running ArgoCD sync; automated DNS failover (Route 53 / Cloudflare) triggers HPA scale-up (RTO < 8.4 minutes).

### 5. Zero-Trust Mesh & Network Policies
- Cilium / Istio Service Mesh enforces mutual TLS (mTLS) with SPIFFE/SPIRE cryptographic workload identities.
- Strict Kubernetes `NetworkPolicy` resources isolate namespaces and prevent unauthorized lateral movement between microservices.

---

## Consequences

### Positive
- **No Resource Starvation**: CPU-intensive OCR and agent processing cannot degrade API latency or UI responsiveness.
- **Sub-10-Minute Recovery**: Verified disaster recovery RTO < 8.4 minutes and RPO < 12 seconds exceeds standard enterprise Tier 1 application requirements.
- **Portability**: Kubernetes and Helm foundation enables seamless deployment across AWS EKS, GCP GKE, Azure AKS, Red Hat OpenShift, or on-premise air-gapped clusters.
- **Auditable Operations**: GitOps ensures every infrastructure change, configuration update, and deployment is immutably committed to git history.

### Negative / Trade-Offs
- **Cluster Management Complexity**: Managing multi-node-pool Kubernetes clusters and cross-region replication requires experienced platform engineering and SRE oversight.
- **Standby Infrastructure Cost**: Secondary region hot standby infrastructure incurs an estimated 25%–35% baseline infrastructure cost overhead.

---

## Alternatives Considered

1. **Serverless-Only (AWS Lambda / Google Cloud Functions)**: Rejected due to cold-start penalties on large AI/agent runtimes, execution duration limits (15 minutes), and lack of portability to private/on-premise enterprise environments.
2. **Single Shared Kubernetes Node Pool**: Rejected due to high risk of resource starvation where a surge in document uploads would exhaust CPU/memory and crash API gateways.
3. **Active-Active Multi-Region Database**: Rejected due to extreme distributed database write conflict complexity, multi-master latency overhead, and high operational fragility compared to active-passive with sub-second replication.
