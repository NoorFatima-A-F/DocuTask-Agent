"""
Recovery Session Aggregate Root.
Maintains state, diagnosed failure, selected strategy, and resolution history for a recovery operation.
"""

from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.agents.recovery.failure import Failure
from app.agents.recovery.lifecycle import RecoveryLifecycleState
from app.agents.recovery.metadata import RecoveryIdentity, RecoveryMetadata, RecoveryStatistics
from app.agents.recovery.recovery_graph import RecoveryGraph
from app.agents.recovery.recovery_strategy import RecoveryStrategyDefinition
from app.agents.recovery.root_cause import RootCauseReport


class RecoverySession(BaseModel):
    """Autonomous Recovery Session Aggregate Root."""
    identity: RecoveryIdentity
    failure: Failure
    root_cause: Optional[RootCauseReport] = None
    strategy_definition: Optional[RecoveryStrategyDefinition] = None
    recovery_graph: Optional[RecoveryGraph] = None
    lifecycle_state: RecoveryLifecycleState = Field(default=RecoveryLifecycleState.INITIALIZING)
    metadata: RecoveryMetadata = Field(default_factory=RecoveryMetadata)
    statistics: RecoveryStatistics = Field(default_factory=RecoveryStatistics)
    resolution_notes: Optional[str] = None
    model_config = {"frozen": True}
