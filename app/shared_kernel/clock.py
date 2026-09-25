"""
Centralized Time Providers and Clock Abstractions.
Avoids direct system clock access across all platform verification workflows.
"""
from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from typing import Optional
import time

class TimeProvider(ABC):
    """Abstract Time Provider interface."""
    @abstractmethod
    def now(self) -> datetime:
        pass

    def now_iso(self) -> str:
        return self.now().isoformat()

    def now_epoch_ms(self) -> int:
        return int(self.now().timestamp() * 1000)

    @abstractmethod
    def monotonic(self) -> float:
        pass

class SystemClock(TimeProvider):
    """Production UTC System Clock."""
    def now(self) -> datetime:
        return datetime.now(timezone.utc)

    def monotonic(self) -> float:
        return time.monotonic()

class SystemTimeProvider(SystemClock):
    """Alias for SystemClock."""
    pass

class MonotonicClock:
    """High-precision duration timer."""
    def __init__(self):
        self._start = time.monotonic()

    def elapsed_seconds(self) -> float:
        return time.monotonic() - self._start

    def elapsed_ms(self) -> float:
        return self.elapsed_seconds() * 1000.0

class VirtualClock(TimeProvider):
    """Deterministic, freezeable Virtual Clock for unit testing and time-travel simulation."""
    def __init__(self, initial_time: Optional[datetime] = None):
        self._current_time = initial_time or datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        self._monotonic_val: float = 0.0

    def now(self) -> datetime:
        return self._current_time

    def monotonic(self) -> float:
        return self._monotonic_val

    def set_time(self, new_time: datetime) -> None:
        self._current_time = new_time

    def advance(self, duration: timedelta) -> None:
        self._current_time += duration
        self._monotonic_val += duration.total_seconds()

    def advance_seconds(self, seconds: float) -> None:
        self.advance(timedelta(seconds=seconds))

class DeterministicTimeProvider(VirtualClock):
    """Alias for VirtualClock."""
    pass

class FrozenClock(VirtualClock):
    """Frozen clock alias."""
    pass
