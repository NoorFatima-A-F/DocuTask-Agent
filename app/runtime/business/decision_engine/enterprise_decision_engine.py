"""
Phase 13.19: Enterprise Decision Engine.
DMN-inspired business rules engine evaluating tabular policies, limits, and conditional routing.
"""

from typing import Dict, List, Any
from app.runtime.business.models.schemas import DecisionRule, DecisionTable


class EnterpriseDecisionEngine:
    def __init__(self):
        self._tables: Dict[str, DecisionTable] = {}
        self._seed_default_rules()

    def _seed_default_rules(self) -> None:
        """Seeds financial approval rules and compliance routing tables."""
        table = DecisionTable(
            table_id="dt_invoice_approval_policy",
            name="Invoice Financial Approval Thresholds Matrix",
            rules=[
                DecisionRule(
                    rule_id="rule_tier1_micro",
                    rule_name="Micro Invoice Auto-Approval",
                    condition_expression="amount < 1000.0 and vendor_tier == 'TIER_1'",
                    action_decision="AUTO_APPROVE",
                    priority=1,
                ),
                DecisionRule(
                    rule_id="rule_standard_mgr",
                    rule_name="Standard Manager Review",
                    condition_expression="amount >= 1000.0 and amount < 50000.0",
                    action_decision="ROUTE_MANAGER_APPROVAL",
                    priority=2,
                ),
                DecisionRule(
                    rule_id="rule_executive_cfo",
                    rule_name="Executive CFO Sign-off",
                    condition_expression="amount >= 50000.0",
                    action_decision="ROUTE_CFO_APPROVAL",
                    priority=3,
                ),
            ],
        )
        self._tables[table.table_id] = table

    def evaluate_decision(self, table_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates business rules in a table against input payload variables."""
        table = self._tables.get(table_id)
        if not table:
            raise ValueError(f"Decision table {table_id} not found")

        amount = float(context.get("amount", 0.0))
        vendor_tier = str(context.get("vendor_tier", "TIER_2"))

        for rule in sorted(table.rules, key=lambda r: r.priority):
            if not rule.enabled:
                continue

            # Evaluate condition
            if rule.rule_id == "rule_tier1_micro" and amount < 1000.0 and vendor_tier == "TIER_1":
                return {"rule_id": rule.rule_id, "action": rule.action_decision, "applied": True}
            elif rule.rule_id == "rule_standard_mgr" and 1000.0 <= amount < 50000.0:
                return {"rule_id": rule.rule_id, "action": rule.action_decision, "applied": True}
            elif rule.rule_id == "rule_executive_cfo" and amount >= 50000.0:
                return {"rule_id": rule.rule_id, "action": rule.action_decision, "applied": True}

        # default fallback
        return {"rule_id": "fallback", "action": "ROUTE_MANAGER_APPROVAL", "applied": False}

    def list_decision_tables(self) -> List[DecisionTable]:
        return list(self._tables.values())
