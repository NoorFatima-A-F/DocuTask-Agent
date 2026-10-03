"""
Clock Interface
===============
Provides time abstractions for deterministic replay, testing, and production runtime.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone


class IClock(ABC):
    """Abstract clock interface."""

    @abstractmethod
    def now_utc(self) -> datetime:
        """Returns current datetime in UTC timezone."""
        raise NotImplementedError

    @abstractmethod
    def now_utc_iso(self) -> str:
        """Returns ISO 8601 string representation of UTC now."""
        raise NotImplementedError

    @abstractmethod
    def timestamp_epoch(self) -> float:
        """Returns Unix epoch timestamp in seconds."""
        raise NotImplementedError


class SystemClock(IClock):
    """Standard system clock based on wall-clock time."""

    def now_utc(self) -> datetime:
        return datetime.now(timezone.utc)

    def now_utc_iso(self) -> str:
        return self.now_utc().isoformat()

    def timestamp_epoch(self) -> float:
        return self.now_utc().timestamp()


class FrozenClock(IClock):
    """Deterministic frozen clock for testing and verifiable replay."""

    def __init__(self, fixed_datetime: datetime):
        self._dt = fixed_datetime if fixed_datetime.tzinfo else fixed_datetime.replace(tzinfo=timezone.utc)

    def set_time(self, new_dt: datetime) -> None:
        self._dt = new_dt if new_dt.tzinfo else new_dt.replace(tzinfo=timezone.utc)

    def advance_seconds(self, seconds: float) -> None:
        from datetime import timedelta
        self._dt += timedelta(seconds=seconds)

    def now_utc(self) -> datetime:
        return self._dt

    def now_utc_iso(self) -> str:
        return self._dt.isoformat()

    def timestamp_epoch(self) -> float:
        return self._dt.timestamp()
