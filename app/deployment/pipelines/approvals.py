"""Pipeline Approval Gates and Security Governance."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
import uuid
from ..core.exceptions import ApprovalGateException


@dataclass
class GateApproval:
    """Individual sign-off for an approval gate."""
    approver: str
    role: str
    comment: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ApprovalGate:
    """Multi-role governance gate requiring quorum before pipeline continuation."""

    def __init__(
        self,
        name: str,
        required_roles: List[str],
        timeout_seconds: int = 3600,
        gate_id: Optional[str] = None,
    ):
        self.gate_id = gate_id or f"gate-{uuid.uuid4().hex[:8]}"
        self.name = name
        self.required_roles = required_roles
        self.timeout_seconds = timeout_seconds
        self.created_at = datetime.now(timezone.utc)
        self.approvals: List[GateApproval] = []
        self.is_emergency_bypassed = False
        self.bypass_reason: Optional[str] = None
        self.bypassed_by: Optional[str] = None

    @property
    def is_timed_out(self) -> bool:
        """Checks whether approval gate exceeded its maximum wait window."""
        elapsed = (datetime.now(timezone.utc) - self.created_at).total_seconds()
        return elapsed > self.timeout_seconds

    @property
    def is_satisfied(self) -> bool:
        """Checks if all required roles have approved or emergency bypass is active."""
        if self.is_emergency_bypassed:
            return True
        if self.is_timed_out:
            return False
        approved_roles = {a.role for a in self.approvals}
        return all(r in approved_roles for r in self.required_roles)

    def approve(self, approver: str, role: str, comment: str = "") -> GateApproval:
        """Records an approval from an authorized role."""
        if self.is_timed_out:
            raise ApprovalGateException(f"Approval gate '{self.name}' has timed out")
        
        appr = GateApproval(approver=approver, role=role, comment=comment)
        self.approvals.append(appr)
        return appr

    def emergency_bypass(self, operator: str, reason: str) -> None:
        """Bypasses approval gate under emergency protocol with mandatory audit record."""
        if not reason or len(reason.strip()) < 10:
            raise ApprovalGateException("Emergency bypass requires a detailed reason (at least 10 chars)")
        self.is_emergency_bypassed = True
        self.bypassed_by = operator
        self.bypass_reason = reason

    def verify_gate(self) -> bool:
        """Asserts gate satisfaction, raising ApprovalGateException on failure."""
        if self.is_timed_out:
            raise ApprovalGateException(f"Approval gate '{self.name}' timed out after {self.timeout_seconds}s")
        if not self.is_satisfied:
            approved_roles = {a.role for a in self.approvals}
            missing = [r for r in self.required_roles if r not in approved_roles]
            raise ApprovalGateException(
                f"Approval gate '{self.name}' unsatisfied. Missing required approvals for roles: {missing}"
            )
        return True
