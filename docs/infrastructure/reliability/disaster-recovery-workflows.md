# Disaster Recovery Workflows & Point-in-Time Restoration

## 1. Supported Disaster Recovery Playbooks
1. **Region Outage Recovery Workflow**: Shifts global ingress, revokes active regional leases, promotes secondary replicas, and verifies cross-service health.
2. **Database Corruption Recovery Workflow**: Quarantines corrupted database, fetches verified `SHA256` snapshot checkpoint, replays idempotent write-ahead logs, and validates restored records.
3. **Storage Loss Recovery Workflow**: Detaches failed storage volume, attaches cross-region replica volume, verifies file system consistency, and remounts worker storage pools.
4. **Queue Loss Recovery Workflow**: Provisions fresh broker partition, queries `ExecutionLeaseManager` for in-flight tasks, and republishes workloads with idempotency keys.
5. **AI Provider Fallback Workflow**: Trips primary AI provider circuit breaker, switches model routing weights to secondary provider, runs warmup inference tests, and verifies output contracts.

## 2. Integrity Verification
Post-restoration, the `RecoveryVerifier` validates:
- Cryptographic hash matches original snapshot (`SHA256`).
- Record count matches expected entity volumes.
- Schema version compatibility.
