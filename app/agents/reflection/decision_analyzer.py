"""
Decision Analyzer.
Evaluates governance decisions, policy outcomes, rule firings, and risk metrics.
"""

from typing import Any, Dict, List
from app.agents.reflection.reflection_context import DecisionTrace


class DecisionAnalyzer:
    """Analyzes decision traces from the Decision and Governance Engine."""

    def analyze_decisions(self, decisions: List[DecisionTrace]) -> Dict[str, Any]:
        """Examines policy checks, approval gates, and risk scores."""
        total = len(decisions)
        if total == 0:
            return {
                "total_decisions": 0,
                "allowed_count": 0,
                "denied_count": 0,
                "average_risk_score": 0.0,
                "policy_compliance_rate": 1.0
            }

        allowed = sum(1 for d in decisions if d.outcome == "ALLOWED")
        denied = sum(1 for d in decisions if d.outcome != "ALLOWED")
        risks = [d.risk_score for d in decisions]
        avg_risk = sum(risks) / total if risks else 0.0

        return {
            "total_decisions": total,
            "allowed_count": allowed,
            "denied_count": denied,
            "average_risk_score": avg_risk,
            "policy_compliance_rate": allowed / total
        }
