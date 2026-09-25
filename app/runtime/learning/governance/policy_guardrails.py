"""
Policy Guardrails Validator for Phase 13.5 (ARLP-KIP).
Enforces hard safety boundaries, parameter clamps, and invariant thresholds for autonomous policy updates.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field


class GuardrailEnforcement(BaseModel):
    is_compliant: bool
    violations: List[str] = Field(default_factory=list)
    enforced_bounds: Dict[str, Any] = Field(default_factory=dict)


class PolicyGuardrailsValidator:
    """
    Validates candidate parameters against absolute production safety boundaries.
    """

    GUARDRAIL_BOUNDS = {
        "max_retries": {"min": 0, "max": 10, "type": "int"},
        "concurrency_limit": {"min": 1, "max": 32, "type": "int"},
        "timeout_seconds": {"min": 5, "max": 300, "type": "int"},
        "confidence_threshold": {"min": 0.50, "max": 1.00, "type": "float"},
        "replanning_sensitivity": {"min": 0.05, "max": 0.95, "type": "float"},
    }

    @classmethod
    def get_guardrail_spec(cls) -> Dict[str, Any]:
        return cls.GUARDRAIL_BOUNDS

    @classmethod
    def validate_parameters(cls, parameters: Dict[str, Any]) -> GuardrailEnforcement:
        violations = []
        for k, v in parameters.items():
            if k in cls.GUARDRAIL_BOUNDS:
                spec = cls.GUARDRAIL_BOUNDS[k]
                min_v = spec["min"]
                max_v = spec["max"]
                if not (min_v <= v <= max_v):
                    violations.append(f"Parameter '{k}' value {v} violates guardrail range [{min_v}, {max_v}]")

        return GuardrailEnforcement(
            is_compliant=len(violations) == 0,
            violations=violations,
            enforced_bounds=cls.GUARDRAIL_BOUNDS,
        )
