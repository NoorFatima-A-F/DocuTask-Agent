"""Automated Rollback Triggers & Safety Policies (Req 42, 44)."""
from enum import Enum


class RollbackTriggerType(str, Enum):
    """Triggers causing an automatic or manual rollback (Req 42)."""
    SLO_BURN = "SLO_BURN"
    HEALTH_FAILURE = "HEALTH_FAILURE"
    SECURITY_INCIDENT = "SECURITY_INCIDENT"
    COMPATIBILITY_FAILURE = "COMPATIBILITY_FAILURE"
    MIGRATION_FAILURE = "MIGRATION_FAILURE"
    AI_REGRESSION = "AI_REGRESSION"
    MANUAL_ABORT = "MANUAL_ABORT"
