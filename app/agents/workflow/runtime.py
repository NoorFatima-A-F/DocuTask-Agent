"""
Workflow Runtime Container.
Encapsulates all workflow subsystems: engine, scheduler, registry, saga orchestrator, replay, migration, and adapters.
"""

import logging
from typing import Optional
from app.agents.workflow.engine import WorkflowEngine
from app.agents.workflow.metrics import WorkflowMetricsCollector
from app.agents.workflow.saga import SagaOrchestrator
from app.agents.workflow.workflow_migration import WorkflowMigrationEngine
from app.agents.workflow.workflow_registry import WorkflowRegistry
from app.agents.workflow.workflow_replay import WorkflowReplayEngine
from app.agents.workflow.workflow_repository import (
    IWorkflowRepository,
    InMemoryWorkflowRepository,
)
from app.agents.workflow.workflow_scheduler import WorkflowScheduler

logger = logging.getLogger(__name__)


class WorkflowRuntime:
    """Enterprise Workflow Runtime coordinating engines, schedulers, sagas, and telemetry."""

    def __init__(
        self,
        engine: Optional[WorkflowEngine] = None,
        registry: Optional[WorkflowRegistry] = None,
        repository: Optional[IWorkflowRepository] = None,
        scheduler: Optional[WorkflowScheduler] = None,
        saga_orchestrator: Optional[SagaOrchestrator] = None,
        replay_engine: Optional[WorkflowReplayEngine] = None,
        migration_engine: Optional[WorkflowMigrationEngine] = None,
        metrics: Optional[WorkflowMetricsCollector] = None,
    ) -> None:
        self.repository = repository or InMemoryWorkflowRepository()
        self.registry = registry or WorkflowRegistry()
        self.engine = engine or WorkflowEngine(registry=self.registry)
        self.scheduler = scheduler or WorkflowScheduler()
        self.saga_orchestrator = saga_orchestrator or SagaOrchestrator()
        self.replay_engine = replay_engine or WorkflowReplayEngine()
        self.migration_engine = migration_engine or WorkflowMigrationEngine()
        self.metrics = metrics or WorkflowMetricsCollector()
        self._is_active = False

    @property
    def is_active(self) -> bool:
        return self._is_active

    async def initialize(self) -> None:
        """Initializes runtime components and binds listeners."""
        logger.info("Initializing Enterprise Workflow Runtime...")
        self._is_active = True

    async def shutdown(self) -> None:
        """Gracefully shuts down active workflows and scheduler."""
        logger.info("Shutting down Enterprise Workflow Runtime...")
        self._is_active = False
