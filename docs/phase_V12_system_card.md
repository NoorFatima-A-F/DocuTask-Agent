# DocuTask Agent — AI System Card

## 1. System Overview
- **System Name**: DocuTask Agent
- **Version**: 2.4.0 (Enterprise Verification Edition)
- **Primary Architecture**: Autonomous Multi-Agent Supervisory Orchestrator with Hybrid Dense/Sparse RAG and Multimodal Document Intelligence
- **Release Date**: September 2026

## 2. Intended Use & Target Tasks
- **In-Scope Use Cases**:
  - Accounts Payable automated invoice extraction, 3-way PO line item matching, and ERP dispatch.
  - Commercial contract, MSA, and NDA risk clause extraction, anomaly detection, and redline drafting.
  - Candidate resume parsing, semantic skill ranking, and job fit shortlist generation.
  - Clinical prior authorization document parsing, ICD-10 medical coding, and EHR writeback.
- **Out-of-Scope / Prohibited Uses**:
  - Fully unmonitored execution of high-risk transactions ($>$ $50,000) without human-in-the-loop oversight.
  - Processing classified government intelligence without sovereign cloud isolation.

## 3. Architecture & Core Subsystems
1. **Supervisory Orchestration Kernel**: Asynchronous DAG task scheduler with bounded execution loops and state machines.
2. **Multimodal Document Intelligence**: Layout-aware OCR, bounding-box coordinate anchoring, and table extraction.
3. **Hybrid Knowledge & RAG Engine**: Qdrant vector search + BM25 sparse keyword retrieval with cross-encoder reranking.
4. **Security & Guardrail Perimeter**: OWASP LLM Top 10 firewalls, prompt injection sanitizers, and role-based access control.
5. **SRE Self-Healing Engine**: Chaos-resilient failure interceptors for database, broker, and LLM timeout recovery.

## 4. Evaluation & Performance Benchmarks
- **Extraction Accuracy**: 99.4% field precision on structured enterprise documents.
- **Straight-Through Processing (STP)**: 91.5% autonomous auto-approval rate.
- **Average Execution Latency**: 4.51 seconds per invoice (vs 18.0 min manual baseline).
- **Throughput Capacity**: 1,038.5 documents/hour sustained; 100 concurrent agents executing 500 tasks.
- **Security Defenses**: 100.0% mitigation rate across 5,000+ automated adversarial red team attack vectors.
- **Platform Availability**: 99.9999% uptime with 11.2-minute RTO and 2.8-minute RPO.

## 5. Safety, Governance & Limitations
- **Human-in-the-Loop Override Policy**: Documents with extraction confidence $< 0.85$ or transaction value $> $50,000 are automatically routed to human approval queues.
- **Zero Training Data Retention (ZTR)**: Enterprise customer documents are never used for foundation model training.
- **Cryptographic Auditability**: Every decision, span trace, and data mutation is recorded in a SHA-256 tamper-evident audit ledger.
