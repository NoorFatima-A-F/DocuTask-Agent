"""
Approval Recovery Manager.
Remediates rejected or stalled human approval gates.
"""

from uuid import UUID


class ApprovalRecoveryManager:
    """Handles recovery when approval gates are rejected or time out."""

    def handle_rejection(self, execution_id: UUID, gate_id: str, reason: str) -> str:
        """Determines if the rejected branch can be rerouted or requires rollback."""
        return "TRIGGER_ROLLBACK"
