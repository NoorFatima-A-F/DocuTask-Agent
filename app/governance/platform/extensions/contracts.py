"""Extension Contracts and Interfaces for Governance Extensibility."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ExtensionCapability(str):
    POLICY_EVALUATOR = "extension.policy_evaluator"
    RISK_SCORER = "extension.risk_scorer"
    METRIC_PROVIDER = "extension.metric_provider"
    COMPLIANCE_CHECKER = "extension.compliance_checker"


class PolicyExtensionContract(ABC):
    """Contract for custom policy rule evaluators."""

    @abstractmethod
    def evaluate_rule(self, rule_config: Dict[str, Any], context: Dict[str, Any]) -> tuple[bool, str]:
        """Evaluate custom rule. Returns (is_satisfied, message)."""
        pass


class CustomRiskEvaluatorContract(ABC):
    """Contract for custom domain risk scoring extensions."""

    @abstractmethod
    def calculate_risk(self, action: str, resource: str, context: Dict[str, Any]) -> float:
        """Compute numeric risk score in range [0.0, 100.0]."""
        pass


class MetricProviderContract(ABC):
    """Contract for custom governance metrics extensions."""

    @abstractmethod
    def compute_metrics(self, tenant_id: str, timeframe: str) -> Dict[str, Any]:
        """Compute custom governance telemetry metrics."""
        pass
