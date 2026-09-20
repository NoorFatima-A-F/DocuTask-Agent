"""
ARTEICP Cost Intelligence - Multi-Dimensional Cost Aggregator
Aggregates multidimensional financial telemetry per tool, model, retry attempt, document, and mission.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from app.runtime.cost_intelligence.cost_calculator import CostCalculator, CostAndEnergyBreakdown


@dataclass
class MissionCostReport:
    mission_id: str
    total_net_cost_usd: float
    total_tokens_consumed: int
    prompt_cache_savings_usd: float
    total_energy_kwh: float
    total_co2_grams: float
    cost_by_model: Dict[str, float]
    cost_by_tool: Dict[str, float]
    retry_cost_overhead_usd: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CostAggregator:
    """Aggregates execution cost metrics into comprehensive multidimensional reports."""

    @classmethod
    def get_canonical_mission_cost(cls, mission_id: str = "mission_live_001") -> MissionCostReport:
        step_ocr = CostCalculator.calculate_step_cost(
            model_id="local-ocr-specialist",
            input_tokens=800,
            output_tokens=300,
            cached_tokens=0,
            api_overhead_usd=0.0001,
        )
        step_flash = CostCalculator.calculate_step_cost(
            model_id="gemini-2.5-flash",
            input_tokens=2200,
            output_tokens=650,
            cached_tokens=1000,
            api_overhead_usd=0.0002,
        )
        step_val = CostCalculator.calculate_step_cost(
            model_id="gemini-flash-lite",
            input_tokens=600,
            output_tokens=150,
            cached_tokens=400,
            api_overhead_usd=0.0001,
        )

        steps = [step_ocr, step_flash, step_val]

        total_net = sum(s.net_cost_usd for s in steps)
        total_tok = sum(s.input_tokens + s.output_tokens for s in steps)
        total_cache_sav = sum(s.cached_cost_discount_usd for s in steps)
        total_e = sum(s.energy_kwh for s in steps)
        total_co2 = sum(s.co2_grams for s in steps)

        by_model = {
            "gemini-2.5-flash": step_flash.net_cost_usd,
            "gemini-flash-lite": step_val.net_cost_usd,
            "local-ocr-specialist": step_ocr.net_cost_usd,
        }

        by_tool = {
            "OCR_INGEST": step_ocr.net_cost_usd,
            "LLM_STRUCTURED_EXTRACTION": step_flash.net_cost_usd,
            "SCHEMA_VALIDATION": step_val.net_cost_usd,
        }

        return MissionCostReport(
            mission_id=mission_id,
            total_net_cost_usd=round(total_net, 5),
            total_tokens_consumed=total_tok,
            prompt_cache_savings_usd=round(total_cache_sav, 5),
            total_energy_kwh=round(total_e, 6),
            total_co2_grams=round(total_co2, 4),
            cost_by_model=by_model,
            cost_by_tool=by_tool,
            retry_cost_overhead_usd=0.0000,
        )
