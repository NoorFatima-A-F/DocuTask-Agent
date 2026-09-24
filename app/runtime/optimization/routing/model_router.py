"""
Model & Tool Router for Phase 13.6 (ARIA-EOP).
Policy-driven routing for LLMs (Gemini Flash, Gemini Pro, Claude), OCR engines, and verification depths.
"""

from pydantic import BaseModel


class RouteDecision(BaseModel):
    task_id: str
    target_engine: str
    routing_type: str  # MODEL | OCR | VALIDATION | WORKER
    confidence_expectation: float
    estimated_cost_usd: float
    rationale: str


class ModelRouter:
    """
    Routes document tasks to optimal LLMs based on complexity, token load, and confidence requirements.
    """

    @classmethod
    def route_model(cls, task_id: str, complexity: float, confidence_floor: float) -> RouteDecision:
        if complexity > 0.85 or confidence_floor > 0.98:
            return RouteDecision(
                task_id=task_id,
                target_engine="gemini-1.5-pro",
                routing_type="MODEL",
                confidence_expectation=0.992,
                estimated_cost_usd=0.012,
                rationale="High complexity / strict confidence floor warrants Gemini 1.5 Pro reasoning.",
            )
        return RouteDecision(
            task_id=task_id,
            target_engine="gemini-1.5-flash",
            routing_type="MODEL",
            confidence_expectation=0.965,
            estimated_cost_usd=0.002,
            rationale="Standard complexity document handled efficiently by Gemini 1.5 Flash.",
        )


class OCRRouter:
    """
    Routes document pages to appropriate OCR engines.
    """

    @classmethod
    def route_ocr(cls, task_id: str, is_scanned_handwriting: bool, page_count: int) -> RouteDecision:
        if is_scanned_handwriting:
            return RouteDecision(
                task_id=task_id,
                target_engine="DOCUMENT_AI_ADVANCED",
                routing_type="OCR",
                confidence_expectation=0.975,
                estimated_cost_usd=0.0015 * page_count,
                rationale="Noisy scanned handwriting requires Document AI Advanced parser.",
            )
        return RouteDecision(
            task_id=task_id,
            target_engine="TESSERACT_FAST",
            routing_type="OCR",
            confidence_expectation=0.985,
            estimated_cost_usd=0.0001 * page_count,
            rationale="Clean digital PDF efficiently extracted using local high-speed Tesseract OCR.",
        )


class ValidationRouter:
    """
    Routes extracted schemas to appropriate invariant verification depth.
    """

    @classmethod
    def route_validation(cls, task_id: str, is_financial_audit: bool) -> RouteDecision:
        if is_financial_audit:
            return RouteDecision(
                task_id=task_id,
                target_engine="SMT_SYMBOLIC_PROVER",
                routing_type="VALIDATION",
                confidence_expectation=0.999,
                estimated_cost_usd=0.001,
                rationale="Financial totals require rigorous Z3 symbolic SMT invariant verification.",
            )
        return RouteDecision(
            task_id=task_id,
            target_engine="HEURISTIC_CONSISTENCY",
            routing_type="VALIDATION",
            confidence_expectation=0.950,
            estimated_cost_usd=0.0001,
            rationale="General schema validated via regex and heuristic schema consistency checks.",
        )
