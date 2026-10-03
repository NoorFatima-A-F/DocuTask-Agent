# Total Production Cost & Sensitivity Analysis Report (Section 8 Audit)

**Subsystem**: Production Financial Cost & Budget Protection Engine  

---

## 1. Full Production Cost Breakdown (1M Documents / Month)

| Resource Component | Unit Price | Monthly Usage | Monthly Cost ($ USD) | Percentage of Total |
|--------------------|------------|---------------|----------------------|---------------------|
| **Gemini 1.5 Flash API** | $0.000103 / doc | 1,000,000 docs | `[DERIVED]` **$103.00** | 22.8% |
| **Worker Compute (EC2/GKE)** | $0.05 / vCPU-hr | 20 vCPU (720 hrs) | `[DERIVED]` **$180.00** | 39.8% |
| **PostgreSQL RDS (DB)** | db.r6g.xlarge | 150 GB Storage | `[DERIVED]` **$95.00** | 21.0% |
| **Redis Cache / Broker** | cache.m6g.large| 16 GB Memory | `[DERIVED]` **$45.00** | 10.0% |
| **S3 Object Storage & Egress**| $0.023 / GB | 100 GB Storage | `[DERIVED]` **$15.00** | 3.3% |
| **Monitoring & Logging** | CloudWatch / Datadog | 50 GB Logs | `[DERIVED]` **$14.00** | 3.1% |
| **Total Monthly Cost** | — | **1,000,000 docs** | `[DERIVED]` **$452.00 USD** | **100.0%** |

- **Cost per Document**: `[DERIVED]` **$0.000452 USD** (All-inclusive infra + LLM cost).
