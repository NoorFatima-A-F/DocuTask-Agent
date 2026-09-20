"""
Interfaces for the Enterprise Workflow Runtime & Orchestration Engine.
Defines abstract contracts for workflow engines, saga orchestrators, schedulers, and replay engines.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import UUID


class IWorkflowEngine(ABC):
    """Core contract for starting, signaling, pausing, and resuming long-running workflows."""

    @abstractmethod
    async def start_workflow(self, request: Any) -> Any:
        """Initiates execution of a workflow instance."""
        raise NotImplementedError

    @abstractmethod
    async def signal_workflow(self, instance_id: UUID, signal_name: str, payload: Any) -> None:
        """Sends an external signal to a running or waiting workflow instance."""
        raise NotImplementedError

    @abstractmethod
    async def get_workflow_status(self, instance_id: UUID) -> Any:
        """Retrieves status and output state of a workflow instance."""
        raise NotImplementedError


class ISagaOrchestrator(ABC):
    """Contract for coordinating distributed Saga transactions and compensations."""

    @abstractmethod
    async def execute_saga_step(self, step: Any, context: Any) -> Any:
        """Executes forward step of a Saga."""
        raise NotImplementedError

    @abstractmethod
    async def execute_compensation(self, step: Any, context: Any) -> Any:
        """Executes backward compensating step upon failure."""
        raise NotImplementedError


class IWorkflowScheduler(ABC):
    """Contract for scheduling workflow instances on cron or delayed timers."""

    @abstractmethod
    async def schedule(self, scheduled_item: Any) -> None:
        """Schedules a workflow execution."""
        raise NotImplementedError


class IWorkflowReplayEngine(ABC):
    """Contract for deterministically replaying workflows from audit histories."""

    @abstractmethod
    async def replay(self, history: Any) -> Any:
        """Reconstructs state by replaying workflow events."""
        raise NotImplementedError
