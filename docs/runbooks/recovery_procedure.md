# Operational Runbook: Disaster Recovery & Multi-Region Restore Procedure

## 1. Problem Description
Complete catastrophic loss of primary infrastructure zone, unrecoverable data corruption, or total cloud region disruption requiring full business continuity activation.

## 2. Detection
- **Multi-Region Sentinel**: Primary region heartbeat fails continuously for $>60$ seconds.
- **Health Probes**: Total unavailability of API, database, and storage subsystems.
- **Disaster Declaration**: SRE on-call lead declares disaster state.

## 3. Impact
- Platform completely inaccessible in primary region.
- Activation of target RTO ($<15$ minutes) and RPO ($<5$ minutes) commitments.
- Severity: **SEV1** (Critical - Disaster State).

## 4. Diagnosis
1. Check cloud provider status dashboard and network routes.
2. Verify availability and timestamp of latest encrypted backups in secondary bucket:
   ```bash
   aws s3 ls s3://docutask-backup-secondary-region/database/
   ```
3. Test connectivity to standby replica database in secondary region.

## 5. Resolution & Disaster Recovery Workflow
1. Promote secondary read replica to primary database:
   ```bash
   docker exec -it docutask-postgres-secondary pg_ctl promote
   ```
2. Restore MinIO / S3 object storage state from immutable snapshot archive:
   ```bash
   mc mirror secondary-backup/docutask-blobs active-storage/docutask-blobs
   ```
3. Spin up standby container fleet in secondary region:
   ```bash
   docker compose -f docker-compose.dr.yml up -d
   ```
4. Update DNS Global Traffic Manager (GTM) / Route 53 to point to secondary region VIP:
   ```bash
   aws route53 change-resource-record-sets --hosted-zone-id Z12345 --change-batch file://failover-dns.json
   ```

## 6. Validation
- Run end-to-end integration workflow against failover endpoint:
  ```bash
  python -m pytest tests/platform_verification/test_enterprise_disaster_recovery.py -k test_dr_rto_rpo_verification
  ```
- Verify data consistency across restored document records.
