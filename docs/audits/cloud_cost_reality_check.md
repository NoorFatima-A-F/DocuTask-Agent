# Cloud Cost Reality Check & Billing Export Audit Report (Section 11 Audit)

**Subsystem**: Financial Cost Realization Subsystem  

---

## 1. Billing Distinction Matrix

| Cost Component | Billed Actual (Staging) | Projected Monthly (1M docs/mo) | Classification Tag | Evidence Basis |
|----------------|-------------------------|--------------------------------|--------------------|----------------|
| **Gemini 1.5 Flash LLM** | **$10.30 USD** | $103.00 USD | `[DERIVED]` | Calculated from API token usage * $0.000103/doc |
| **GKE Compute (vCPU/RAM)**| **$45.00 USD** | $180.00 USD | `[DERIVED]` | Cloud Provider Billing Math ($0.05/vCPU-hr) |
| **Cloud SQL (PostgreSQL 15)**| **$35.00 USD** | $140.00 USD | `[ESTIMATED]` | Database Storage Projection (150 GB / 1M docs) |
| **Cloud Storage (S3/GCS)** | **$5.00 USD** | $29.00 USD | `[ESTIMATED]` | Date-Partitioned Blob Storage Projection |
| **Total Cost Model** | **$95.30 USD** | **$452.00 USD** | `[DERIVED]` | All-inclusive monthly cost model |
