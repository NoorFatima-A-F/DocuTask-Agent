# Financial Cost Model Validation & Classification Audit (Section 9 Audit)

**Subsystem**: Financial Cost Validation Subsystem  

---

## 1. Classification Tag Breakdown of Financial Items

- **Gemini 1.5 Flash API Token Costs**: `[DERIVED]` Calculated from published pricing ($0.000103 USD / doc) * token count.
- **Worker Instance Compute (GKE)**: `[DERIVED]` Calculated from cloud instance pricing ($0.05 / vCPU-hr) * worker count.
- **PostgreSQL Database Storage**: `[ESTIMATED]` Projected at 150 GB / 1M docs based on measured schema row byte sizes.
- **S3 Object Storage & Network Egress**: `[ESTIMATED]` Projected at 100 GB / 1M docs based on average document PDF size (100 KB).
