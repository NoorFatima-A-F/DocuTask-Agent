# Operational Runbook: Security Incident & Unauthorized Access Response

## 1. Problem Description
Detection of unauthorized API access attempts, leaked credentials, brute-force token generation, or malicious payload injection into the document parsing pipeline.

## 2. Detection
- **Alert**: `ALT-SEC-005: Unauthorized IAM Access Attempt` ($>3$ unauthorized calls in 1 min).
- **SIEM / Audit Log**: Multiple 401/403 responses from unrecognized foreign IP addresses.
- **WAF / IDS**: Malformed PDF header containing executable exploit shellcode.

## 3. Impact
- Risk of unauthorized document access or tenant data exfiltration.
- Integrity violation of operational audit trails.
- Severity: **SEV1** (Critical).

## 4. Diagnosis
1. Inspect audit trail for unauthorized actor operations:
   ```bash
   curl -s http://localhost:8000/api/v1/operations/audit | jq '.entries[] | select(.status != "SUCCESS")'
   ```
2. Trace origin IP addresses and request headers:
   ```bash
   docker logs --tail 500 docutask-api | grep -i "401\|403\|unauthorized"
   ```
3. Check API key and JWT token revocation lists.

## 5. Resolution & Remediation
1. Immediately revoke compromised API keys and rotate JWT signing secret:
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/revoke-tokens -H "Authorization: Bearer $SEC_ADMIN_KEY"
   ```
2. Block offending IP addresses at WAF / firewall layer:
   ```bash
   iptables -A INPUT -s <OFFENDING_IP> -j DROP
   ```
3. Isolate affected worker pods to prevent lateral movement.
4. Notify Data Protection Officer (DPO) and initiate regulatory incident timeline.

## 6. Validation
- Verify revoked tokens fail with 401 Unauthorized:
  ```bash
  curl -i http://localhost:8000/api/v1/documents -H "Authorization: Bearer <REVOKED_TOKEN>"
  ```
- Confirm SIEM dashboard reports zero unauthorized ingress attempts.
