# Governance Plugin Development Guide

DocuTask Governance supports dynamic, sandboxed plugins to extend policy rules, risk models, and analytics hooks.

---

## Plugin Contract

All plugins must implement the `GovernancePlugin` abstract class:

```python
from typing import Any, Dict
from app.governance.platform.plugins.sandbox import GovernancePlugin

class CustomDataLossPreventionPlugin(GovernancePlugin):
    def __init__(self):
        super().__init__(name="DLP_Scanner", version="1.0.0", description="Scans payload for SSN and credit cards")

    def initialize(self, config: Dict[str, Any]) -> None:
        self.strict_mode = config.get("strict", True)

    def validate(self) -> bool:
        # Pre-flight security & integrity check
        return True

    def execute(self, hook_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if hook_name == "before_model_invoke":
            text = payload.get("prompt", "")
            if "SSN" in text:
                return {"violation": True, "action": "BLOCK", "reason": "SSN detected"}
        return {"violation": False}

    def shutdown(self) -> None:
        pass
```

---

## Plugin Lifecycle
1. `REGISTERED`: Metadata and capability permissions recorded.
2. `VALIDATED`: Self-validation passed in sandbox.
3. `APPROVED`: Platform administrator approves deployment.
4. `ACTIVE`: Initialized and actively handling hooks.
5. `DISABLED`: Temporarily paused without deleting state.
6. `REMOVED`: Shut down and uninstalled.
