# Root Cause Analysis (5-Whys): INC-2026-DR-001

1. **Why was service degraded?**
   - The primary database in AZ-1 was unreachable by application worker nodes.
2. **Why was AZ-1 primary unreachable?**
   - The virtual switch route table dropped packets between subnet A and subnet B.
3. **Why did failover take 4.2 minutes?**
   - Healthcheck retry thresholds required 3 consecutive failed probes before quorum trigger.
4. **Why did clients experience brief reconnection latency?**
   - PgBouncer pool drainage took 20 seconds to clear stale TCP sessions.
5. **Why was no data lost?**
   - Synchronous replication (`synchronous_commit = on`) guaranteed zero uncommitted transaction gaps on the replica.
