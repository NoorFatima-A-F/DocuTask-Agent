"""
ARTEICP Cost Intelligence - Granular Cost & Energy Calculator
Calculates exact token pricing, prompt cache discounts, API baseline charges, and compute carbon/energy footprints.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class CostAndEnergyBreakdown:
    model_id: str
    input_tokens: int
    output_tokens: int
    cached_tokens: int
    input_cost_usd: float
    output_cost_usd: float
    cached_cost_discount_usd: float
    api_overhead_cost_usd: float
    net_cost_usd: float
    energy_kwh: float
    co2_grams: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Pricing per 1,000,000 tokens (Standard Google AI Gemini pricing schedule)
MODEL_PRICING = {
    "gemini-2.5-flash": {"input_per_m": 0.075, "output_per_m": 0.30, "cached_input_per_m": 0.01875},
    "gemini-1.5-flash": {"input_per_m": 0.075, "output_per_m": 0.30, "cached_input_per_m": 0.01875},
    "gemini-1.5-pro": {"input_per_m": 1.25, "output_per_m": 5.00, "cached_input_per_m": 0.3125},
    "gemini-flash-lite": {"input_per_m": 0.025, "output_per_m": 0.10, "cached_input_per_m": 0.00625},
    "local-ocr-specialist": {"input_per_m": 0.0, "output_per_m": 0.0, "cached_input_per_m": 0.0},
}


class CostCalculator:
    """Calculates granular financial cost and datacenter energy footprint per execution step."""

    @classmethod
    def calculate_step_cost(
        cls,
        model_id: str,
        input_tokens: int,
        output_tokens: int,
        cached_tokens: int = 0,
        api_overhead_usd: float = 0.0001,
    ) -> CostAndEnergyBreakdown:
        rates = MODEL_PRICING.get(model_id, MODEL_PRICING["gemini-2.5-flash"])

        raw_in_cost = ((input_tokens - cached_tokens) / 1_000_000.0) * rates["input_per_m"]
        cached_in_cost = (cached_tokens / 1_000_000.0) * rates["cached_input_per_m"]
        standard_cached_cost = (cached_tokens / 1_000_000.0) * rates["input_per_m"]
        cache_discount = standard_cached_cost - cached_in_cost

        out_cost = (output_tokens / 1_000_000.0) * rates["output_per_m"]
        net_cost = raw_in_cost + cached_in_cost + out_cost + api_overhead_usd

        # Energy & Carbon Footprint Model:
        # ~0.0003 kWh per 1000 tokens on modern TPU/GPU clusters
        total_tokens = input_tokens + output_tokens
        energy_kwh = (total_tokens / 1000.0) * 0.0003
        # ~385g CO2 per kWh (global average grid intensity)
        co2_g = energy_kwh * 385.0

        return CostAndEnergyBreakdown(
            model_id=model_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_tokens=cached_tokens,
            input_cost_usd=round(raw_in_cost + cached_in_cost, 6),
            output_cost_usd=round(out_cost, 6),
            cached_cost_discount_usd=round(cache_discount, 6),
            api_overhead_cost_usd=round(api_overhead_usd, 6),
            net_cost_usd=round(net_cost, 6),
            energy_kwh=round(energy_kwh, 6),
            co2_grams=round(co2_g, 4),
        )
