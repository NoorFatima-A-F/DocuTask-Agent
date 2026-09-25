"""Extension Contract and Capability Validators."""

from typing import Any, List
from .contracts import (
    CustomRiskEvaluatorContract,
    ExtensionCapability,
    MetricProviderContract,
    PolicyExtensionContract,
)


class ExtensionValidationError(Exception):
    """Raised when an extension does not satisfy required contract interfaces."""
    pass


class ExtensionValidator:
    """Validates extension classes and instances against governance contracts."""

    @classmethod
    def validate_extension(cls, extension_obj: Any, declared_capabilities: List[str]) -> bool:
        """Verify extension implements contracts matching its declared capabilities."""
        if not extension_obj:
            raise ExtensionValidationError("Extension instance cannot be None.")

        for cap in declared_capabilities:
            if cap == ExtensionCapability.POLICY_EVALUATOR:
                if not isinstance(extension_obj, PolicyExtensionContract) and not hasattr(extension_obj, "evaluate_rule"):
                    raise ExtensionValidationError(
                        f"Extension declared capability '{cap}' but does not implement 'evaluate_rule(rule_config, context)'."
                    )
            elif cap == ExtensionCapability.RISK_SCORER:
                if not isinstance(extension_obj, CustomRiskEvaluatorContract) and not hasattr(extension_obj, "calculate_risk"):
                    raise ExtensionValidationError(
                        f"Extension declared capability '{cap}' but does not implement 'calculate_risk(action, resource, context)'."
                    )
            elif cap == ExtensionCapability.METRIC_PROVIDER:
                if not isinstance(extension_obj, MetricProviderContract) and not hasattr(extension_obj, "compute_metrics"):
                    raise ExtensionValidationError(
                        f"Extension declared capability '{cap}' but does not implement 'compute_metrics(tenant_id, timeframe)'."
                    )

        return True
