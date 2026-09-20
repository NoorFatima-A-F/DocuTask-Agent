"""Model Routing and Failover Engine (Phase 8C).

Orchestrates live model invocation with dynamic fallback, retries, circuit breaking,
and latency-based / health-based routing.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field
from app.model_governance.registry.models import Model, ModelLifecycleState
from app.model_governance.registry.repository import ModelRegistryRepository
from app.model_governance.selection.selector import (
    ModelSelectionRequest,
    ModelSelectionResult,
    ModelSelectionService,
)


class ModelInvocationRecord(BaseModel):
    """Execution telemetry record for model routing."""
    model_id: str
    organization_id: str
    task_name: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_ms: float = 0.0
    status: str = "SUCCESS"  # SUCCESS, FAILOVER, ERROR
    error_message: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)
    failover_chain: List[str] = Field(default_factory=list)


class ModelRouter:
    """Intelligent router executing tasks with automated failover across primary & fallback models."""

    def __init__(
        self,
        repository: ModelRegistryRepository,
        selection_service: ModelSelectionService,
    ):
        self.repository = repository
        self.selection_service = selection_service
        self.invocation_history: List[ModelInvocationRecord] = []
        self._circuit_breakers: Dict[str, int] = {}  # model_id -> consecutive failure count

    def execute_with_failover(
        self,
        request: ModelSelectionRequest,
        executor_fn: Callable[[Model], Any],
        max_retries: int = 2,
    ) -> tuple[Any, ModelInvocationRecord]:
        """Executes a function against selected model with automated fallback if execution fails."""
        selection = self.selection_service.select_model(request)
        target_model_ids = [selection.selected_model.model_id] + selection.fallback_models

        attempted_models: List[str] = []
        last_error: Optional[Exception] = None

        for model_id in target_model_ids:
            # Check circuit breaker
            if self._circuit_breakers.get(model_id, 0) >= 3:
                continue

            model = self.repository.get_model(model_id, request.organization_id)
            if not model or model.lifecycle_state != ModelLifecycleState.ACTIVE:
                continue

            attempted_models.append(model_id)
            start_time = time.time()

            try:
                result = executor_fn(model)
                latency = (time.time() - start_time) * 1000.0

                # Reset circuit breaker
                self._circuit_breakers[model_id] = 0

                record = ModelInvocationRecord(
                    model_id=model_id,
                    organization_id=request.organization_id,
                    task_name=request.task_name,
                    latency_ms=latency,
                    status="FAILOVER" if len(attempted_models) > 1 else "SUCCESS",
                    failover_chain=attempted_models,
                )
                self.invocation_history.append(record)
                return result, record

            except Exception as e:
                last_error = e
                self._circuit_breakers[model_id] = self._circuit_breakers.get(model_id, 0) + 1
                continue

        # All candidates failed
        failed_record = ModelInvocationRecord(
            model_id=target_model_ids[0] if target_model_ids else "unknown",
            organization_id=request.organization_id,
            task_name=request.task_name,
            status="ERROR",
            error_message=str(last_error),
            failover_chain=attempted_models,
        )
        self.invocation_history.append(failed_record)
        raise RuntimeError(
            f"All candidate models failed for task {request.task_name}. "
            f"Attempted: {attempted_models}. Last error: {last_error}"
        )
