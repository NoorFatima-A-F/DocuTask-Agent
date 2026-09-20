# Runbook: Object Storage Outage Recovery

## 1. Symptoms & Detection
* **Alert Trigger**: `ObjectStorageErrorRateHigh` (s3_request_errors_total > 5%).
* **Symptoms**: Document preview failures, OCR extraction worker payload read errors.

## 2. Triage & Failover
```bash
# Verify S3 bucket accessibility
aws s3 ls s3://docutask-dr-vault-primary/
# Check cross-region replica synchronization state
aws s3api head-bucket --bucket docutask-dr-vault-secondary
```

## 3. Recovery Procedure
1. **Switch Read/Write Endpoint to Secondary Region (us-west-2)**:
   ```bash
   kubectl set env deployment/docutask-api S3_BUCKET_NAME="docutask-dr-vault-secondary"
   ```
2. **Re-sync from Immutable WORM Archive**:
   ```bash
   aws s3 sync s3://docutask-dr-worm-vault/ s3://docutask-dr-vault-primary/ --exact-timestamps
   ```

## 4. Hash Parity Verification
```bash
python -m app.platform_verification.document_storage_verification.cli
```
