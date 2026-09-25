"""
Enterprise Autonomous Reflection Engine.
Primary cognitive introspection facade analyzing completed executions, evaluating outcomes,
generating critiques, extracting knowledge, and emitting cross-subsystem feedback.
"""

import time
from typing import Optional
from app.agents.reflection.context import ReflectionRequest, ReflectionResult
from app.agents.reflection.interfaces import IReflectionEngine
from app.agents.reflection.lifecycle import ReflectionLifecycleState
from app.agents.reflection.manager import ReflectionManager
from app.agents.reflection.metadata import ReflectionIdentity, ReflectionStatistics
from app.agents.reflection.metrics import ReflectionMetricsCollector
from app.agents.reflection.orchestrator import ReflectionOrchestrator
from app.agents.reflection.reflection import Reflection
from app.agents.reflection.validation import ReflectionRequestValidator


class ReflectionEngine(IReflectionEngine):
    """
    Autonomous Reflection Engine.
    Examines finished execution traces, runs multi-dimensional evaluation,
    performs self-critique, distills learning artifacts, and produces structured subsystem feedback.
    Never executes work, never modifies active runtime state, and never invokes tools directly.
    """

    def __init__(
        self,
        orchestrator: Optional[ReflectionOrchestrator] = None,
        manager: Optional[ReflectionManager] = None,
        metrics_collector: Optional[ReflectionMetricsCollector] = None,
    ):
        self.orchestrator = orchestrator or ReflectionOrchestrator()
        self.manager = manager or ReflectionManager()
        self.metrics = metrics_collector or ReflectionMetricsCollector()

    async def reflect(self, request: ReflectionRequest) -> ReflectionResult:
        """Executes full reflection lifecycle on a completed execution request."""
        start_time = time.monotonic()
        identity = ReflectionIdentity(
            execution_id=request.trace.execution_id,
            plan_id=request.trace.plan_id,
            tenant_id=request.context.tenant_id,
            correlation_id=request.context.correlation_id
        )

        self.metrics.record_reflection_started()

        # 1. Validation
        validation_report = ReflectionRequestValidator.validate(request)
        if not validation_report.is_valid:
            self.metrics.record_reflection_failed()
            return ReflectionResult(
                identity=identity,
                lifecycle_state=ReflectionLifecycleState.FAILED,
                errors=validation_report.errors
            )

        try:
            # 2. Orchestration
            results = await self.orchestrator.orchestrate_reflection(request.trace)

            duration_ms = (time.monotonic() - start_time) * 1000.0
            self.metrics.record_reflection_completed(duration_ms)
            self.metrics.record_evaluation(len(results["evaluation_report"].dimensions))
            self.metrics.record_critique()
            self.metrics.record_artifacts(len(results["learning_artifacts"]))
            self.metrics.record_recommendations(len(results["recommendations"]))
            self.metrics.record_proposals(len(results["adaptation_proposals"]))

            stats = ReflectionStatistics(
                evaluation_duration_ms=duration_ms * 0.4,
                critique_duration_ms=duration_ms * 0.3,
                learning_duration_ms=duration_ms * 0.3,
                total_reflection_duration_ms=duration_ms,
                evaluators_executed=len(results["evaluation_report"].dimensions),
                critiques_generated=1,
                learning_artifacts_created=len(results["learning_artifacts"]),
                recommendations_generated=len(results["recommendations"]),
                adaptation_proposals_created=len(results["adaptation_proposals"])
            )

            # 3. Create and persist Reflection aggregate
            reflection_entity = Reflection(
                identity=identity,
                state=ReflectionLifecycleState.COMPLETED,
                statistics=stats,
                learning_artifact_ids=[a.artifact_id for a in results["learning_artifacts"]],
                recommendation_ids=[r.recommendation_id for r in results["recommendations"]],
                adaptation_proposal_ids=[p.proposal_id for p in results["adaptation_proposals"]]
            )
            await self.manager.persist_reflection(reflection_entity)

            feedback_bundle = results["feedback_bundle"]

            return ReflectionResult(
                identity=identity,
                lifecycle_state=ReflectionLifecycleState.COMPLETED,
                evaluation_report=results["evaluation_report"],
                critique=results["critique"],
                learning_artifacts=results["learning_artifacts"],
                recommendations=results["recommendations"],
                adaptation_proposals=results["adaptation_proposals"],
                planner_feedback=feedback_bundle.planner_feedback,
                execution_feedback=feedback_bundle.execution_feedback,
                memory_feedback=feedback_bundle.memory_feedback,
                tool_feedback=feedback_bundle.tool_feedback,
                statistics=stats
            )

        except Exception as e:
            self.metrics.record_reflection_failed()
            duration_ms = (time.monotonic() - start_time) * 1000.0
            return ReflectionResult(
                identity=identity,
                lifecycle_state=ReflectionLifecycleState.FAILED,
                statistics=ReflectionStatistics(total_reflection_duration_ms=duration_ms),
                errors=[str(e)]
            )
