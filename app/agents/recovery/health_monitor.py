"""
Recovery Health Monitor.
Evaluates overall resilience and availability of the recovery subsystem, queues, and adapters.
"""

from pydantic import BaseModel, Field


class SubsystemHealthReport(BaseModel):
    is_healthy: bool = Field(default=True)
    active_incidents_count: int = Field(default=0, ge=0)
    dead_letters_count: int = Field(default=0, ge=0)
    circuit_breakers_open_count: int = Field(default=0, ge=0)
    model_config = {"frozen": True}


class RecoveryHealthMonitor:
    """Continuously monitors health of recovery pipelines and protective circuit breakers."""

    def get_health_report(
        self,
        active_incidents: int = 0,
        dead_letters: int = 0,
        open_circuits: int = 0
    ) -> SubsystemHealthReport:
        is_healthy = (active_incidents == 0 and open_circuits == 0)
        return SubsystemHealthReport(
            is_healthy=is_healthy,
            active_incidents_count=active_incidents,
            dead_letters_count=dead_letters,
            circuit_breakers_open_count=open_circuits
        )
