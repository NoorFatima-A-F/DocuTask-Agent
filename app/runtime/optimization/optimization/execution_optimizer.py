"""
Execution Optimizer for Phase 13.6 (ARIA-EOP).
Translates selected strategy into execution directives (batching chunks, concurrency pool bounds, retry delays).
"""

from pydantic import BaseModel


class ExecutionDirective(BaseModel):
    concurrency_pool_size: int = 6
    batch_chunk_size: int = 4
    base_retry_delay_ms: float = 250.0
    timeout_budget_ms: float = 4500.0
    model_routing_target: str = "gemini-1.5-flash"
    ocr_engine_target: str = "TESSERACT_FAST"
    validation_depth: str = "SMT_SYMBOLIC"


class ExecutionOptimizer:
    """
    Generates actionable runtime directives for the execution engine.
    """

    @classmethod
    def generate_directives(
        cls,
        page_count: int,
        complexity: float,
        priority: str = "BALANCED",
    ) -> ExecutionDirective:
        if page_count > 10 or complexity > 0.7:
            return ExecutionDirective(
                concurrency_pool_size=8,
                batch_chunk_size=4,
                base_retry_delay_ms=200.0,
                timeout_budget_ms=6000.0,
                model_routing_target="gemini-1.5-pro" if complexity > 0.85 else "gemini-1.5-flash",
                ocr_engine_target="DOCUMENT_AI_ADVANCED" if complexity > 0.75 else "TESSERACT_FAST",
                validation_depth="SMT_SYMBOLIC",
            )
        return ExecutionDirective(
            concurrency_pool_size=4,
            batch_chunk_size=2,
            base_retry_delay_ms=250.0,
            timeout_budget_ms=3500.0,
            model_routing_target="gemini-1.5-flash",
            ocr_engine_target="TESSERACT_FAST",
            validation_depth="HEURISTIC_CONSISTENCY",
        )
