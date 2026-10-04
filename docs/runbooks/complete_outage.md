# Runbook: Complete Regional Cloud Outage & Bare-Metal Resurrection

## 1. Symptoms & Severity
* **Severity**: SEV-1 Critical (Total Datacenter Annihilation).
* **Detection**: Global multi-region probes failing across all microservice ingress endpoints.

## 2. Bare-Metal Recovery Procedure
1. **Provision Infrastructure in Disaster Recovery Region**:
   ```bash
   cd terraform/environments/dr-us-west-2
   terraform init && terraform apply -auto-approve
   ```
2. **Deploy Core Secrets & Kubernetes Platform**:
   ```bash
   helmfile -e dr-region apply
   ```
3. **Restore Database & Document Repositories**:
   ```bash
   python run_restore_verification.py --environment=dr-standby
   ```
4. **Deploy Application Microservices**:
   ```bash
   kubectl rollout restart deployment -n docutask
   ```

## 3. Full-Stack Operational Validation
```bash
python run_backup_certification.py
```
