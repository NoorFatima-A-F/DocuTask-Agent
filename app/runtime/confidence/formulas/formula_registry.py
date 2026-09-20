"""
Formula Registry for Phase 13.3 (ASCE-CGP).
Registry for version-controlled mathematical confidence calculation formulas.
"""

from typing import Dict, List, Any


class FormulaRegistry:
    """
    Registry of mathematical models available to the confidence engine.
    """

    FORMULAS: Dict[str, Dict[str, Any]] = {
        "WeightedEnsemble": {
            "version": "v1.3.0",
            "type": "LINEAR_ENSEMBLE",
            "description": "Multi-dimensional weighted sum with policy-driven dynamic weighting",
            "formula_expr": "sum(w_i * f_i) / sum(w_i)",
            "supports_uncertainty": True,
        },
        "BayesianInference": {
            "version": "v2.0.0",
            "type": "PROBABILISTIC",
            "description": "Bayesian prior-posterior updating using historical likelihood distributions",
            "formula_expr": "(P(E|H) * P(H)) / P(E)",
            "supports_uncertainty": True,
        },
        "ReliabilityMultiplication": {
            "version": "v1.1.0",
            "type": "STOCHASTIC",
            "description": "Multiplicative reliability pipeline for series dependency chains",
            "formula_expr": "prod(R_i)",
            "supports_uncertainty": False,
        },
    }

    @classmethod
    def get(cls, name: str) -> Dict[str, Any]:
        return cls.FORMULAS.get(name, cls.FORMULAS["WeightedEnsemble"])

    @classmethod
    def list_all(cls) -> List[Dict[str, Any]]:
        return [{"name": k, **v} for k, v in cls.FORMULAS.items()]
