"""
Quality Gate Engine: Hard/Soft blockers, threshold evaluation, composite scoring.
"""
from typing import Dict, Any, List
from ..interfaces import QualityGateEngineInterface
from ...crosscutting.observability import ComponentObservability

class QualityGateEngine(QualityGateEngineInterface):
    """Evaluates verification outcomes against strict quality policies."""
    
    def __init__(self):
        self.observability = ComponentObservability("QualityGateEngine")

    async def evaluate_gates(self, metrics: Dict[str, float], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        self.observability.record_operation(1.2)
        passed = True
        blockers = []
        for r in rules:
            m_name = r["metric"]
            val = metrics.get(m_name)
            if val is None:
                passed = False
                blockers.append(f"Missing metric: {m_name}")
                continue
            op = r.get("operator", ">=")
            thresh = r["threshold"]
            rule_pass = False
            if op == ">=":
                rule_pass = val >= thresh
            elif op == "<=":
                rule_pass = val <= thresh
            elif op == "==":
                rule_pass = val == thresh
            elif op == ">":
                rule_pass = val > thresh
            elif op == "<":
                rule_pass = val < thresh
            
            if not rule_pass:
                passed = False
                blockers.append(f"{m_name} failed rule: {val} {op} {thresh}")
                
        return {
            "passed": passed,
            "composite_score": 1.0 if passed else 0.0,
            "blockers": blockers
        }
