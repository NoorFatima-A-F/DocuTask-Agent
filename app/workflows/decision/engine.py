"""
Enterprise Workflow Decision Engine.
Evaluates conditional expressions, rules, and branching policies.
"""

from typing import Any, Dict, Optional


class DecisionEngine:
    """Evaluates branching decisions in execution graphs."""

    @staticmethod
    def evaluate_condition(expression: str, variables: Dict[str, Any]) -> bool:
        """Evaluate a simple boolean expression against execution variables."""
        if not expression or not expression.strip():
            return True

        expr = expression.strip()

        # Simple equality: "amount > 1000" or "status == 'approved'"
        if "==" in expr:
            var_name, expected = [p.strip() for p in expr.split("==", 1)]
            val = variables.get(var_name)
            expected = expected.strip("'\"")
            return str(val) == expected

        elif "!=" in expr:
            var_name, expected = [p.strip() for p in expr.split("!=", 1)]
            val = variables.get(var_name)
            expected = expected.strip("'\"")
            return str(val) != expected

        elif ">=" in expr:
            var_name, expected = [p.strip() for p in expr.split(">=", 1)]
            val = float(variables.get(var_name, 0))
            return val >= float(expected)

        elif "<=" in expr:
            var_name, expected = [p.strip() for p in expr.split("<=", 1)]
            val = float(variables.get(var_name, 0))
            return val <= float(expected)

        elif ">" in expr:
            var_name, expected = [p.strip() for p in expr.split(">", 1)]
            val = float(variables.get(var_name, 0))
            return val > float(expected)

        elif "<" in expr:
            var_name, expected = [p.strip() for p in expr.split("<", 1)]
            val = float(variables.get(var_name, 0))
            return val < float(expected)

        elif expr in variables:
            return bool(variables[expr])

        return False

    @staticmethod
    def evaluate_switch(value: Any, cases: Dict[str, str], default_target: Optional[str] = None) -> Optional[str]:
        """Evaluate a switch/case condition and return target node ID."""
        val_str = str(value)
        return cases.get(val_str, default_target)
