# Runbook: Disaster Recovery Rollback & Re-pointing

## 1. Purpose
Defines safe procedures to roll back traffic from disaster recovery region back to primary once primary infrastructure is restored.

## 2. Steps
1. Pause asynchronous Celery ingestion workers.
2. Synchronize delta changes from DR database back to Primary PostgreSQL via WAL replay.
3. Switch Route53 Weighted DNS back to 100% Primary.
4. Resume workers and verify zero message drops in Redis queue.
