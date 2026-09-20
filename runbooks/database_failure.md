# Runbook: PostgreSQL Database Disaster Recovery

## 1. Symptoms & Detection
* **Alert Trigger**: `PostgresClusterUnavailable` (pg_up == 0) or `PgBouncerPoolExhausted`.
* **Symptoms**: API returning 500/503 on database queries; Celery task timeouts.

## 2. Immediate Triage Commands
```bash
# Check RDS/PostgreSQL cluster status
kubectl get pods -n docutask -l app=postgres
# Check PgBouncer connection pool
psql -h pgbouncer.internal -p 6432 -U pgbouncer pgbouncer -c "SHOW POOLS;"
```

## 3. Step-by-Step Recovery Procedure
1. **Initiate Automated Multi-AZ Failover**:
   ```bash
   aws rds reboot-db-instance --db-instance-identifier docutask-prod-pg --force-failover
   ```
2. **Fallback: Point-in-Time Restore from Base Snapshot & WAL**:
   ```bash
   aws rds restore-db-instance-to-point-in-time      --source-db-instance-identifier docutask-prod-pg      --target-db-instance-identifier docutask-prod-pg-recovered      --restore-time "$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
   ```
3. **Re-route DNS / Connection String**:
   ```bash
   kubectl set env deployment/docutask-api DATABASE_URL="postgresql://user:pass@docutask-prod-pg-recovered:5432/docutask"
   ```

## 4. Post-Recovery Validation
```bash
python -m app.platform_verification.database_backup_verification.cli
```

## 5. Rollback Procedure
If restored instance exhibits schema drift, revert DNS to read-replica promoted cluster.
