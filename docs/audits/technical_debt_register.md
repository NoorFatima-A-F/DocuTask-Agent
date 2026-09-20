# Zero-Trust Technical Debt Register & Effort Projections (Section 12 Audit)

**Subsystem**: Technical Debt Audit & Engineering Impact Subsystem  

---

## 1. Technical Debt Item Breakdown

| Debt ID | Category | Technical Debt Description | Engineering Effort | Business Impact | Mitigation Action |
|---------|----------|----------------------------|--------------------|-----------------|-------------------|
| **TD-01** | Architecture | PostgreSQL advisory lock ceiling at >32 worker pods | 3 Days | High at >1M docs/day | Implement Redis-based distributed locks (`Redlock`) |
| **TD-02** | Observability | Missing standalone OpenTelemetry collector deployment | 1 Day | Low | Deploy dedicated Jaeger / Grafana Tempo collector |
| **TD-03** | Operations | Manual PostgreSQL WAL backup verification script | 2 Days | Medium | Automate via Cloud SQL automated snapshot schedule |
