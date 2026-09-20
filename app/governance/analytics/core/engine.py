"""Master Governance Metrics Engine unifying warehouse queries and calculators."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from .metrics import (
    MetricPeriod,
    MetricValue,
    MetricTrend,
    DecisionMetricsSummary,
    PolicyMetricsSummary,
    AgentMetricsSummary,
    ModelMetricsSummary,
    PromptMetricsSummary,
)
from .calculators import (
    DecisionMetricsCalculator,
    PolicyMetricsCalculator,
    AgentMetricsCalculator,
    ModelMetricsCalculator,
    PromptMetricsCalculator,
)
from .aggregators import TimeSeriesAggregator
from ..warehouse.repositories import GovernanceDataWarehouseRepository
from ..warehouse.schemas import WarehouseQueryFilter


class GovernanceMetricsEngine:
    """Master engine calculating cross-governance intelligence and summaries."""

    def __init__(self, repository: Optional[GovernanceDataWarehouseRepository] = None):
        self.repo = repository or GovernanceDataWarehouseRepository()

    def get_decision_metrics(self, tenant_id: str = "*") -> DecisionMetricsSummary:
        return DecisionMetricsCalculator.calculate(self.repo, tenant_id=tenant_id)

    def get_policy_metrics(self, tenant_id: str = "*") -> PolicyMetricsSummary:
        return PolicyMetricsCalculator.calculate(self.repo, tenant_id=tenant_id)

    def get_agent_metrics(self, tenant_id: str = "*") -> AgentMetricsSummary:
        return AgentMetricsCalculator.calculate(self.repo, tenant_id=tenant_id)

    def get_model_metrics(self, tenant_id: str = "*") -> ModelMetricsSummary:
        return ModelMetricsCalculator.calculate(self.repo, tenant_id=tenant_id)

    def get_prompt_metrics(self, tenant_id: str = "*") -> PromptMetricsSummary:
        return PromptMetricsCalculator.calculate(self.repo, tenant_id=tenant_id)

    def calculate_governance_score(self, tenant_id: str = "*") -> float:
        """
        Calculates composite overall AI Governance Health Score (0.0 to 100.0).
        Weighted factors:
        - Policy Effectiveness: 25%
        - Agent Safety & Low Risk: 25%
        - Decision Compliance / Low Block Rate: 25%
        - Model Reliability: 25%
        """
        pol = self.get_policy_metrics(tenant_id)
        agent = self.get_agent_metrics(tenant_id)
        dec = self.get_decision_metrics(tenant_id)
        model = self.get_model_metrics(tenant_id)

        pol_score = pol.policy_effectiveness_score * 100.0
        agent_score = max(0.0, (1.0 - agent.avg_agent_risk_score) * 100.0)
        dec_score = dec.allow_rate * 100.0
        model_score = max(0.0, (1.0 - model.avg_model_risk_score) * 100.0)

        composite = (0.25 * pol_score) + (0.25 * agent_score) + (0.25 * dec_score) + (0.25 * model_score)
        return round(min(100.0, max(0.0, composite)), 2)
