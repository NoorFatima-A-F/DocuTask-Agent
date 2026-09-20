"""
Time and Clock Abstractions.
"""
from abc import ABC, abstractmethod
from datetime import datetime, timezone, timedelta
from typing import Optional

class ClockInterface(ABC):
    @abstractmethod
    def now(self) -> datetime:
        """Returns current timezone-aware UTC datetime."""
        pass

    @abstractmethod
    def now_iso(self) -> str:
        """Returns ISO 8601 formatted string."""
        pass


class SystemClock(ClockInterface):
    def now(self) -> datetime:
        return datetime.now(timezone.utc)

    def now_iso(self) -> str:
        return self.now().isoformat()


class VirtualClock(ClockInterface):
    def __init__(self, initial_time: Optional[datetime] = None):
        self._current_time = initial_time or datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    def now(self) -> datetime:
        return self._current_time

    def now_iso(self) -> str:
        return self._current_time.isoformat()

    def advance(self, delta: timedelta) -> None:
        self._current_time += delta

    def set_time(self, time: datetime) -> None:
        self._current_time = time
