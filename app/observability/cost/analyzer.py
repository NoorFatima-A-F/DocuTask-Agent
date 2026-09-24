"""Operational Cost Intelligence and AI Token Unit Economics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CostBreakdown:
    tenant_id: str
    compute_usd: float = 0.0
    storage_usd: float = 0.0
    network_usd: float = 0.0
    ai_tokens_usd: float = 0.0
    total_cost_usd: float = 0.0


class CostAnalyzer:
    """Analyzes and attributes infrastructure and generative AI execution expenses."""

    def __init__(
        self,
        cost_per_cpu_hour_usd: float = 0.04,
        cost_per_gb_storage_month_usd: float = 0.02,
        cost_per_1k_prompt_tokens_usd: float = 0.0005,
        cost_per_1k_completion_tokens_usd: float = 0.0015,
    ):
        self.cost_per_cpu_hour = cost_per_cpu_hour_usd
        self.cost_per_gb_storage = cost_per_gb_storage_month_usd
        self.cost_per_1k_prompt = cost_per_1k_prompt_tokens_usd
        self.cost_per_1k_completion = cost_per_1k_completion_tokens_usd

    def calculate_cost(
        self,
        tenant_id: str,
        cpu_hours: float,
        storage_gb: float,
        prompt_tokens: int,
        completion_tokens: int,
        network_gb: float = 0.0,
    ) -> CostBreakdown:
        compute = cpu_hours * self.cost_per_cpu_hour
        storage = storage_gb * (self.cost_per_gb_storage / (30 * 24))
        ai_cost = (
            (prompt_tokens / 1000.0) * self.cost_per_1k_prompt
            + (completion_tokens / 1000.0) * self.cost_per_1k_completion
        )
        network = network_gb * 0.01
        total = compute + storage + ai_cost + network

        return CostBreakdown(
            tenant_id=tenant_id,
            compute_usd=round(compute, 4),
            storage_usd=round(storage, 4),
            network_usd=round(network, 4),
            ai_tokens_usd=round(ai_cost, 4),
            total_cost_usd=round(total, 4),
        )
