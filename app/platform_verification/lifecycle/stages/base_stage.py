"""
Base Lifecycle Stage Contract.
Enforces explicit entry criteria, exit criteria, retries, timeouts, and compensation.
"""
from abc import ABC, abstractmethod
import time
from datetime import datetime, timezone
from app.platform_verification.lifecycle.context import VerificationExecutionContext, StageResult
from app.platform_verification.lifecycle.states import LifecycleState

class BaseLifecycleStage(ABC):
    @property
    @abstractmethod
    def stage_number(self) -> int:
        pass

    @property
    @abstractmethod
    def stage_name(self) -> str:
        pass

    @property
    @abstractmethod
    def target_state(self) -> LifecycleState:
        pass

    @property
    def timeout_seconds(self) -> int:
        return 120

    @property
    def max_retries(self) -> int:
        return 2

    @abstractmethod
    def validate_entry_criteria(self, context: VerificationExecutionContext) -> bool:
        """Evaluates prerequisites before stage execution."""
        pass

    @abstractmethod
    def execute_stage(self, context: VerificationExecutionContext) -> StageResult:
        """Executes the specific stage business logic."""
        pass

    @abstractmethod
    def validate_exit_criteria(self, context: VerificationExecutionContext, result: StageResult) -> bool:
        """Validates outputs before allowing progression to next stage."""
        pass

    def compensate(self, context: VerificationExecutionContext, error: Exception) -> None:
        """Rollback or compensation logic in case of stage failure."""
        pass

    def run(self, context: VerificationExecutionContext) -> StageResult:
        t0 = time.perf_counter()
        
        # 1. Entry Criteria Check
        if not self.validate_entry_criteria(context):
            raise ValueError(f"Stage {self.stage_number} ({self.stage_name}) Entry Criteria failed.")

        context.record_transition(self.target_state, actor="STAGE_RUNNER", reason=f"Entering {self.stage_name}")

        # 2. Execution with Retries
        result: StageResult
        for attempt in range(self.max_retries + 1):
            try:
                result = self.execute_stage(context)
                result.retry_count = attempt
                break
            except Exception as e:
                if attempt == self.max_retries:
                    self.compensate(context, e)
                    result = StageResult(
                        stage_number=self.stage_number,
                        stage_name=self.stage_name,
                        status="FAILED",
                        error_message=str(e),
                        duration_ms=round((time.perf_counter() - t0) * 1000, 2),
                        completed_at=datetime.now(timezone.utc).isoformat()
                    )
                    context.stage_results.append(result)
                    return result

        result.duration_ms = round((time.perf_counter() - t0) * 1000, 2)
        result.completed_at = datetime.now(timezone.utc).isoformat()

        # 3. Exit Criteria Check
        if not self.validate_exit_criteria(context, result):
            result.status = "FAILED"
            result.error_message = f"Stage {self.stage_number} Exit Criteria validation failed."

        context.stage_results.append(result)
        return result
