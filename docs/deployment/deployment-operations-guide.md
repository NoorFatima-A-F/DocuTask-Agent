# Enterprise Deployment Platform & Release Operations Guide

## 1. Overview
The DocuTask Agent Enterprise Deployment Platform provides a centralized release control plane, progressive delivery strategies, environment promotion gates, automated rollback, expand-contract database migrations, and developer tooling (`doctaskctl` & `InfrastructureSDK`).

---

## 2. Release & Deployment Lifecycle

```
[ Artifact Build ] 
       ↓ (Sign & Validate SBOM)
[ Release Creation ]
       ↓ (Publish)
[ Promotion Request ] 
       ↓ (Governance & Approval Gates)
[ Environment Pre-Flight Validation ]
       ↓
[ Progressive Rollout (Rolling / Blue-Green / Canary / Shadow) ]
       ↓
[ Automated Telemetry Sentry & Post-Deploy Verification ]
       ↓
[ Active in Production / Auto-Rollback if SLO Breached ]
```

---

## 3. CLI Usage with `doctaskctl`

### 3.1 Create and Publish a Release
```bash
doctaskctl release create --version 1.2.0 --name "Q3 Governance Engine" --commit 9a4f21e --artifacts art-001 art-002
```

### 3.2 Execute a Deployment
```bash
doctaskctl deploy --release rel-1.2.0 --env prod --strategy CANARY --replicas 5
```

### 3.3 Emergency Rollback
```bash
doctaskctl rollback --deployment dep-789 --reason "Spike in OCR extraction error rate"
```

### 3.4 Feature Flag Evaluation
```bash
doctaskctl flag eval --key enable_vision_ocr_v2 --tenant tenant-corp --env prod
```

---

## 4. Progressive Delivery Strategies

| Strategy | When to Use | Rollback Characteristic |
|---|---|---|
| **Rolling** | Standard stateless backend updates with predictable resource profiles | Sequential batch rollback |
| **Blue-Green** | Mission-critical core services requiring instantaneous zero-downtime cutover | Instantaneous traffic flip back to standby blue slot |
| **Canary** | High-risk AI inference or routing changes; stepwise traffic evaluation (5% -> 25% -> 50% -> 100%) | Automated abort & traffic drain upon error/latency threshold breach |
| **Shadow** | Dark-launching experimental pipelines by mirroring live requests with zero user impact | Zero customer impact; decommission shadow slot |

---

## 5. Zero-Downtime Expand-Contract Database Evolution
1. **Phase 1: EXPAND** — Add new nullable columns or tables. Dual-write in application.
2. **Phase 2: MIGRATE DATA** — Asynchronously backfill legacy rows.
3. **Phase 3: CONTRACT** — Update application readers to new columns; safely drop deprecated columns.
