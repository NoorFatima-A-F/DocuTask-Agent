# DocuTask Governance Platform API Reference

The DocuTask Governance Platform exposes an enterprise REST API for policy management, action evaluations, audit proof verification, human approvals, and governance analytics.

---

## Base URLs
* Production: `https://api.governance.doctask.io/api/v1`
* Staging: `https://staging-api.governance.doctask.io/api/v1`

---

## Authentication
Every request must supply authentication via Bearer token or API key header:
```http
Authorization: Bearer <API_KEY>
# or
X-API-Key: <API_KEY>
```

---

## Core Endpoints

### 1. Action Evaluation
Evaluate an agent, model, or tool action against active tenant governance policies.

```http
POST /api/v1/governance/evaluate
```

**Request Body:**
```json
{
  "action": "agent.execute",
  "resource": "invoice_processing_agent",
  "context": {
    "risk_level": "medium",
    "data_classification": "PII"
  }
}
```

**Response (`200 OK`):**
```json
{
  "decision_id": "dec_8f1e29c0",
  "decision": "ALLOW",
  "allowed": true,
  "reason": "All governance policies satisfied.",
  "policies_applied": ["data_protection_policy", "model_risk_policy"],
  "risk_level": "LOW",
  "evaluation_time_ms": 1.25,
  "timestamp": "2026-09-19T12:00:00Z"
}
```

---

### 2. Policy Management

#### List Policies
```http
GET /api/v1/governance/policies?status=ACTIVE&page=1&page_size=20
```

#### Create Policy
```http
POST /api/v1/governance/policies
```
```json
{
  "name": "high_cost_model_guardrail",
  "description": "Requires human approval for models with cost > $0.05/call",
  "policy_type": "operational",
  "severity": "HIGH",
  "enforcement_action": "APPROVAL_REQUIRED",
  "rules": [
    {"field": "context.cost_per_call", "op": ">", "value": 0.05}
  ]
}
```

#### Publish Policy
```http
POST /api/v1/governance/policies/{id}/publish
```

---

### 3. Audits & Evidence

#### List Audit Trail
```http
GET /api/v1/governance/audits?event_type=GOVERNANCE_DECISION
```

#### Cryptographic Proof
```http
GET /api/v1/governance/audits/{id}/proof
```

---

### 4. Human-in-the-Loop (HITL) Approvals

#### List Pending Reviews
```http
GET /api/v1/governance/approvals?status=PENDING
```

#### Approve Request
```http
POST /api/v1/governance/approvals/{id}/approve
```

#### Reject Request
```http
POST /api/v1/governance/approvals/{id}/reject
```

---

### 5. Governance Analytics
```http
GET /api/v1/governance/analytics
GET /api/v1/governance/analytics/risk
GET /api/v1/governance/analytics/compliance
```
