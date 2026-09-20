"""Authorization security verification modules."""
from .rbac_boundary_tests import RBACBoundaryVerifier
from .privilege_escalation_tests import PrivilegeEscalationVerifier

__all__ = [
    "RBACBoundaryVerifier",
    "PrivilegeEscalationVerifier",
]
