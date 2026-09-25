"""
Cost Model for Phase 13.6 (ARIA-EOP).
Parametric pricing models for LLMs (Gemini, Claude), OCR engines, CPU/GPU compute, and storage.
"""

from pydantic import BaseModel


class UnitCostBreakdown(BaseModel):
    model_cost_usd: float = 0.0018
    ocr_cost_usd: float = 0.0006
    compute_cost_usd: float = 0.0005
    storage_cost_usd: float = 0.0001
    total_cost_usd: float = 0.0030


class CostModel:
    """
    Computes exact granular costs across all resource dimensions.
    """

    PRICING = {
        "gemini-1.5-flash": {"input_1k": 0.000075, "output_1k": 0.00030},
        "gemini-1.5-pro": {"input_1k": 0.00125, "output_1k": 0.00500},
        "claude-3-5-sonnet": {"input_1k": 0.00300, "output_1k": 0.01500},
        "ocr_tesseract": 0.0001,  # per page
        "ocr_document_ai": 0.0015,  # per page
        "gpu_second": 0.0008,
    }

    @classmethod
    def calculate_cost(
        cls,
        model_name: str,
        input_tokens: int,
        output_tokens: int,
        pages: int = 1,
        ocr_engine: str = "ocr_tesseract",
    ) -> UnitCostBreakdown:
        p = cls.PRICING.get(model_name, cls.PRICING["gemini-1.5-flash"])
        model_cost = (input_tokens / 1000.0) * p["input_1k"] + (output_tokens / 1000.0) * p["output_1k"]
        ocr_unit_price = cls.PRICING.get(ocr_engine, 0.0001)
        ocr_cost = pages * ocr_unit_price
        compute_cost = pages * 0.0003
        storage_cost = 0.0001
        total = round(model_cost + ocr_cost + compute_cost + storage_cost, 6)

        return UnitCostBreakdown(
            model_cost_usd=round(model_cost, 6),
            ocr_cost_usd=round(ocr_cost, 6),
            compute_cost_usd=round(compute_cost, 6),
            storage_cost_usd=round(storage_cost, 6),
            total_cost_usd=total,
        )
