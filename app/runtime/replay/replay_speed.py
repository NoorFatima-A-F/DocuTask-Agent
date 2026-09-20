"""
Replay Speed Scaling Subsystem for Event-Sourced Mission Replay.
Provides mathematical speed multipliers and sleep duration calculations.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict


class ReplaySpeed(str, Enum):
    QUARTER = "0.25x"
    HALF = "0.5x"
    NORMAL = "1x"
    DOUBLE = "2x"
    QUADRUPLE = "4x"
    HEXADECIMAL = "16x"
    INSTANT = "INSTANT"


SPEED_MULTIPLIERS: Dict[ReplaySpeed, float] = {
    ReplaySpeed.QUARTER: 0.25,
    ReplaySpeed.HALF: 0.5,
    ReplaySpeed.NORMAL: 1.0,
    ReplaySpeed.DOUBLE: 2.0,
    ReplaySpeed.QUADRUPLE: 4.0,
    ReplaySpeed.HEXADECIMAL: 16.0,
    ReplaySpeed.INSTANT: float("inf"),
}


@dataclass(frozen=True)
class SpeedProfile:
    speed: ReplaySpeed
    multiplier: float
    base_step_delay_ms: float = 50.0

    def compute_step_delay_seconds(self) -> float:
        """Calculates async sleep delay in seconds for step playback."""
        if self.multiplier == float("inf"):
            return 0.0
        return (self.base_step_delay_ms / 1000.0) / max(0.01, self.multiplier)
