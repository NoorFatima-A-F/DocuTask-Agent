# Worker Isolation Architecture & Container Migration Analysis (Section 2 Audit)

**Subsystem**: Worker Process Lifecycle & Container Isolation Subsystem  

---

## 1. Lifecycle Coupling Evaluation

```
[ Current Lifespan Worker ]
FastAPI App Lifespan ──► Instantiates Worker Engine ──► Single Process Space (FastAPI + Worker)

[ Recommended Standalone Worker Container ]
FastAPI Ingestion Container ──(Redis Streams)──► Standalone Worker Container (Isolated Process)
```

- **Evaluation Verdict**: Currently `app/main.py` starts background workers via lifespan context. For production Kubernetes deployments, background workers should be decoupled into a standalone container entrypoint (`python -m app.jobs.runner`) for independent horizontal scaling.
- **Migration Status**: `CONFIRMED - ACCEPTED RISK` (Lifespan worker mode supported for single-container dev/workstation; standalone CLI worker supported for Kubernetes).
