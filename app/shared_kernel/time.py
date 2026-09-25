"""
Alias forwarding for clock.py
"""
from .clock import (
    TimeProvider,
    SystemClock,
    SystemTimeProvider,
    MonotonicClock,
    VirtualClock,
    DeterministicTimeProvider,
    FrozenClock
)

__all__ = [
    "TimeProvider",
    "SystemClock",
    "SystemTimeProvider",
    "MonotonicClock",
    "VirtualClock",
    "DeterministicTimeProvider",
    "FrozenClock"
]
