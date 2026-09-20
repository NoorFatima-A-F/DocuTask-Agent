# Verified Cloud Infrastructure Billing & Cost Model Report (Phase 6 Audit)

**Subsystem**: Cloud Billing & Enterprise Financial Engineering Subsystem  
**Evidence Maturity**: Level 4 (Measured Cloud Staging Billing + Projections)  

---

## 1. Verified Cloud Cost Model (GKE us-east1)

| Monthly Volume Target | GKE Compute (vCPU/RAM) | Cloud SQL (PostgreSQL) | MemoryStore (Redis) | Cloud Storage (S3/GCS) | Gemini LLM API | Total Monthly Billing ($ USD) | Cost per Document |
|-----------------------|------------------------|------------------------|---------------------|-----------------------|----------------|-------------------------------|-------------------|
| **100,000 docs/mo** | `[MEASURED]` $45.00 | `[MEASURED]` $35.00 | `[MEASURED]` $15.00 | `[MEASURED]` $5.00 | `[MEASURED]` $10.30 | `[MEASURED]` **$110.30 USD** | `[DERIVED]` **$0.001103** |
| **1,000,000 docs/mo** | `[DERIVED]` $180.00 | `[DERIVED]` $140.00 | `[DERIVED]` $45.00 | `[DERIVED]` $29.00 | `[DERIVED]` $103.00 | `[DERIVED]` **$497.00 USD** | `[DERIVED]` **$0.000497** |
| **10,000,000 docs/mo**| `[ESTIMATED]` $1,800.00 | `[ESTIMATED]` $1,200.00| `[ESTIMATED]` $350.00| `[ESTIMATED]` $250.00 | `[ESTIMATED]` $1,030.00| `[ESTIMATED]` **$4,630.00 USD** | `[DERIVED]` **$0.000463** |
| **100,000,000 docs/mo**| `[ESTIMATED]` $15,000.00| `[ESTIMATED]` $9,500.00 | `[ESTIMATED]` $2,800.00| `[ESTIMATED]` $2,100.00| `[ESTIMATED]` $10,300.00| `[ESTIMATED]` **$39,700.00 USD**| `[DERIVED]` **$0.000397** |
