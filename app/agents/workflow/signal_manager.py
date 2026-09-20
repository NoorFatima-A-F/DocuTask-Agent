"""
Workflow Signal Manager.
Receives, buffers, and routes external asynchronous signals to waiting workflow instances.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class WorkflowSignal(BaseModel):
    """External signal sent to a workflow instance."""
    signal_name: str
    instance_id: UUID
    payload: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class SignalManager:
    """Buffers and dispatches signals directed at workflows."""

    def __init__(self):
        self._pending_signals: Dict[UUID, List[WorkflowSignal]] = {}

    def receive_signal(self, signal: WorkflowSignal) -> None:
        """Buffers an incoming signal for the target instance."""
        if signal.instance_id not in self._pending_signals:
            self._pending_signals[signal.instance_id] = []
        self._pending_signals[signal.instance_id].append(signal)

    def consume_signal(self, instance_id: UUID, signal_name: str) -> Optional[WorkflowSignal]:
        """Consumes first matching signal if available."""
        signals = self._pending_signals.get(instance_id, [])
        for idx, sig in enumerate(signals):
            if sig.signal_name == signal_name:
                return signals.pop(idx)
        return None
