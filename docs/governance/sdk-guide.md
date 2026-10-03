# DocuTask Governance SDK Developer Guide

Official developer guide for Python and TypeScript SDKs.

---

## Python SDK

### Installation
```bash
pip install doctask-governance
```

### Quickstart
```python
from app.governance.platform.sdk.python.client import GovernanceClient

# Initialize client
client = GovernanceClient(api_key="gov_live_...")

# Evaluate an AI action before execution
decision = client.evaluate(
    action="model.invoke",
    resource="gemini-1.5-pro",
    context={"prompt_tokens": 1200, "contains_pii": False},
    raise_on_deny=True
)

if decision.allowed:
    # Execute AI model
    print("Action allowed:", decision.decision_id)
```

---

## TypeScript / JavaScript SDK

### Installation
```bash
npm install @doctask/governance-sdk
```

### Quickstart
```typescript
import { GovernanceClient } from "@doctask/governance-sdk";

const client = new GovernanceClient({
  apiKey: "gov_live_...",
  baseUrl: "https://api.governance.doctask.io"
});

const decision = await client.evaluate({
  action: "agent.execute",
  resource: "invoice_agent",
  context: { risk_level: "low" }
});

if (decision.allowed) {
  console.log("Decision approved:", decision.decision_id);
}
```
