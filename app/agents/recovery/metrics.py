"""
Recovery Metrics Collector.
Collects MTTR, recovery success rate, replay latency, dead-letter count, and circuit breaker activations.
"""

from pydantic import BaseModel, Field


class RecoveryMetricRecord(BaseModel):
    failures_detected_count: int = Field(default=0, ge=0)
    recoveries_attempted_count: int = Field(default=0, ge=0)
    recoveries_succeeded_count: int = Field(default=0, ge=0)
    recoveries_failed_count: int = Field(default=0, ge=0)
    incidents_created_count: int = Field(default=0, ge=0)
    dead_letters_count: int = Field(default=0, ge=0)
    reconciliations_count: int = Field(default=0, ge=0)


class RecoveryMetricsCollector:
    """Collector recording recovery and self-healing telemetry."""

    def __init__(self):
        self._record = RecoveryMetricRecord()

    def record_failure_detected(self) -> None:
        self._record.failures_detected_count += 1

    def record_recovery_attempt(self) -> None:
        self._record.recoveries_attempted_count += 1

    def record_recovery_success(self) -> None:
        self._record.recoveries_succeeded_count += 1

    def record_recovery_failed(self) -> None:
        self._record.recoveries_failed_count += 1

    def record_incident_created(self) -> None:
        self._record.incidents_created_count += 1

    def record_dead_letter(self) -> None:
        self._record.dead_letters_count += 1

    def get_metrics(self) -> RecoveryMetricRecord:
        return self._record
