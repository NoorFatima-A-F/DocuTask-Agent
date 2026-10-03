# Governance Extension Guide

Extensions allow organizations to register custom rule engines, specialized risk calculators, and enterprise metric providers.

---

## Extension Capabilities
* `extension.policy_evaluator`: Implements `PolicyExtensionContract.evaluate_rule()`
* `extension.risk_scorer`: Implements `CustomRiskEvaluatorContract.calculate_risk()`
* `extension.metric_provider`: Implements `MetricProviderContract.compute_metrics()`

---

## Example Custom Risk Scorer Extension
```python
from app.governance.platform.extensions.contracts import CustomRiskEvaluatorContract

class FinancialDataRiskScorer(CustomRiskEvaluatorContract):
    def calculate_risk(self, action: str, resource: str, context: dict) -> float:
        if "financial" in resource.lower() and context.get("amount", 0) > 100_000:
            return 85.0
        return 10.0
```
