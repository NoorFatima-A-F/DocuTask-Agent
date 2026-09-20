"""
Workflow Subsystem Factory.
Factory and Dependency Injection container for assembling workflow engines, orchestrators, sagas, and runtimes.
"""

from typing import Any, Optional
from app.agents.workflow.approval_workflow import ApprovalWorkflowEngine
from app.agents.workflow.child_workflow import ChildWorkflowManager
from app.agents.workflow.coordination_adapter import WorkflowCoordinationAdapter
from app.agents.workflow.decision_adapter import WorkflowDecisionAdapter
from app.agents.workflow.engine import WorkflowEngine
from app.agents.workflow.execution_adapter import WorkflowExecutionAdapter
from app.agents.workflow.manager import WorkflowManager
from app.agents.workflow.memory_adapter import WorkflowMemoryAdapter
from app.agents.workflow.metrics import WorkflowMetricsCollector
from app.agents.workflow.orchestrator import WorkflowOrchestrator
from app.agents.workflow.parallel_workflow import ParallelWorkflowEngine
from app.agents.workflow.planner_adapter import WorkflowPlannerAdapter
from app.agents.workflow.recovery_adapter import WorkflowRecoveryAdapter
from app.agents.workflow.reflection_adapter import WorkflowReflectionAdapter
from app.agents.workflow.runtime import WorkflowRuntime
from app.agents.workflow.saga import SagaOrchestrator
from app.agents.workflow.signal_manager import SignalManager
from app.agents.workflow.timer_manager import TimerManager
from app.agents.workflow.workflow_dispatcher import WorkflowDispatcher
from app.agents.workflow.workflow_migration import WorkflowMigrationEngine
from app.agents.workflow.workflow_registry import WorkflowRegistry
from app.agents.workflow.workflow_replay import WorkflowReplayEngine
from app.agents.workflow.workflow_repository import InMemoryWorkflowRepository
from app.agents.workflow.workflow_scheduler import WorkflowScheduler


class WorkflowFactory:
    """Constructs fully configured workflow instances and runtime environments."""

    @staticmethod
    def create_runtime(
        event_bus: Optional[Any] = None,
        execution_engine: Optional[Any] = None,
        coordination_engine: Optional[Any] = None,
        decision_engine: Optional[Any] = None,
        planner: Optional[Any] = None,
        recovery_engine: Optional[Any] = None,
        reflection_engine: Optional[Any] = None,
        memory_foundation: Optional[Any] = None,
    ) -> WorkflowRuntime:
        """Assembles a production-grade WorkflowRuntime with all adapters and components wired."""
        # Repositories & Registries
        repo = InMemoryWorkflowRepository()
        registry = WorkflowRegistry()
        metrics = WorkflowMetricsCollector()

        # Adapters
        exec_adapter = WorkflowExecutionAdapter(execution_engine)
        coord_adapter = WorkflowCoordinationAdapter(coordination_engine)
        decision_adapter = WorkflowDecisionAdapter(decision_engine)
        planner_adapter = WorkflowPlannerAdapter(planner)
        recovery_adapter = WorkflowRecoveryAdapter(recovery_engine)
        reflection_adapter = WorkflowReflectionAdapter(reflection_engine)
        memory_adapter = WorkflowMemoryAdapter(memory_foundation)

        # Dispatcher & Sub-engines
        dispatcher = WorkflowDispatcher(
            execution_adapter=exec_adapter,
            coordination_adapter=coord_adapter,
        )
        saga = SagaOrchestrator()
        parallel = ParallelWorkflowEngine()
        approval = ApprovalWorkflowEngine()
        child_mgr = ChildWorkflowManager()
        timer_mgr = TimerManager()
        signal_mgr = SignalManager()

        manager = WorkflowManager(repository=repo, event_bus=event_bus, metrics=metrics)
        orchestrator = WorkflowOrchestrator(
            dispatcher=dispatcher,
            saga_orchestrator=saga,
            parallel_engine=parallel,
            approval_engine=approval,
            child_manager=child_mgr,
            timer_manager=timer_mgr,
        )

        engine = WorkflowEngine(
            manager=manager,
            orchestrator=orchestrator,
            registry=registry,
            signal_manager=signal_mgr,
            approval_engine=approval,
            timer_manager=timer_mgr,
        )

        scheduler = WorkflowScheduler()
        replay = WorkflowReplayEngine()
        migration = WorkflowMigrationEngine()

        return WorkflowRuntime(
            engine=engine,
            registry=registry,
            repository=repo,
            scheduler=scheduler,
            saga_orchestrator=saga,
            replay_engine=replay,
            migration_engine=migration,
            metrics=metrics,
        )
