"""
Recovery Runtime Coordinator.
Wires event listening, health monitoring, circuit breaker tracking, and recovery engine invocation.
"""

from typing import Optional
from app.agents.recovery.bulkhead import BulkheadManager
from app.agents.recovery.circuit_breaker import CircuitBreaker
from app.agents.recovery.context import RecoveryRequest, RecoveryResult
from app.agents.recovery.engine import RecoveryEngine
from app.agents.recovery.health_monitor import RecoveryHealthMonitor


class RecoveryRuntime:
    """Supervises the recovery runtime environment and protective circuit breakers."""

    def __init__(
        self,
        engine: Optional[RecoveryEngine] = None,
        health_monitor: Optional[RecoveryHealthMonitor] = None,
        bulkhead_manager: Optional[BulkheadManager] = None
    ):
        self.engine = engine or RecoveryEngine()
        self.health_monitor = health_monitor or RecoveryHealthMonitor()
        self.bulkhead_manager = bulkhead_manager or BulkheadManager()
        self.circuit_breakers = {}

    def get_circuit_breaker(self, name: str) -> CircuitBreaker:
        if name not in self.circuit_breakers:
            self.circuit_breakers[name] = CircuitBreaker(name)
        return self.circuit_breakers[name]

    async def run_recovery(self, request: RecoveryRequest) -> RecoveryResult:
        return await self.engine.recover(request)
