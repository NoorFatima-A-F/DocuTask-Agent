# Regional Failover Operational Runbook

## 1. Automated vs. Manual Trigger Criteria
- **Automated Failover**: Triggered when `ReliabilityCoordinator` detects region-level outage exceeding RTO max acceptable limit ($> 900s$) or simultaneous primary cluster loss.
- **Manual Failover**: Initiated via `/api/v1/infrastructure/reliability/failover/plan` and `/execute` for disaster drills or planned maintenance.

## 2. Standard Execution Sequence
```
1. Pre-Flight Validation (Capacity, Data Residency, Replication Lag)
   ↓
2. Source Region Drain (Set Route Weight = 0%, In-Flight Request Draining)
   ↓
3. Execution Lease Revocation (Revoke all active worker leases in source)
   ↓
4. Replication Sync Confirmation (Ensure target replica is caught up)
   ↓
5. Target Region Promotion (Activate primary roles on target clusters)
   ↓
6. Dynamic Traffic Cutover (Update Gateway/DNS Route Table to Target Region)
   ↓
7. End-to-End Readiness Verification (Deep Probes pass on target)
   ↓
8. Post-Failover Incident & Audit Record Finalization
```

## 3. Rollback Protocol
If target region readiness probes fail during Promotion or Traffic Cutover, `FailoverOrchestrator` automatically reverses routing weights to restore original traffic distribution if the source region remains viable.
