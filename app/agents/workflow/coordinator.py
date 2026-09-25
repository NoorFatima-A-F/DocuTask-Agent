"""
Workflow Coordinator.
Coordinates concurrent workflows, child workflow trees, barrier waits, and cross-workflow signal synchronization.
"""

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID
from app.agents.workflow.child_workflow import ChildWorkflowManager
from app.agents.workflow.signal_manager import SignalManager
from app.agents.workflow.wait_manager import WaitManager

logger = logging.getLogger(__name__)


class WorkflowCoordinator:
    """Coordinates multi-workflow barrier synchronization, signals, and child hierarchies."""

    def __init__(
        self,
        child_manager: Optional[ChildWorkflowManager] = None,
        signal_manager: Optional[SignalManager] = None,
        wait_manager: Optional[WaitManager] = None,
    ) -> None:
        self.child_manager = child_manager or ChildWorkflowManager()
        self.signal_manager = signal_manager or SignalManager()
        self.wait_manager = wait_manager or WaitManager()

    def register_child_workflow(
        self,
        parent_id: UUID,
        child_id: UUID,
        node_id: str,
    ) -> None:
        """Registers a child workflow relationship."""
        self.child_manager.register_child(parent_id, child_id, node_id)

    def send_signal(
        self,
        instance_id: UUID,
        signal_name: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Sends an asynchronous signal to a workflow instance."""
        self.signal_manager.send_signal(instance_id, signal_name, payload or {})

    def register_barrier(
        self,
        workflow_id: UUID,
        required_signals: List[str],
    ) -> None:
        """Sets a multi-signal barrier wait condition."""
        self.wait_manager.register_wait(workflow_id, required_signals)

    def check_barrier_satisfied(self, workflow_id: UUID) -> bool:
        """Returns True if all required barrier conditions are met."""
        return self.wait_manager.is_satisfied(workflow_id)
