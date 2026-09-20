"""
Playback Controller for Phase 13.4.
Controls replay stepping rates (0.25x, 0.5x, 1x, 2x, 5x, 10x) and frame loop delays.
"""

from typing import Dict, Any


class PlaybackRateController:
    """
    Manages variable playback speed and frame delay calculations.
    """

    SUPPORTED_SPEEDS = [0.25, 0.5, 1.0, 2.0, 5.0, 10.0]

    @classmethod
    def get_frame_delay_ms(cls, speed: float = 1.0, base_delay_ms: float = 500.0) -> float:
        spd = speed if speed in cls.SUPPORTED_SPEEDS else 1.0
        return max(50.0, base_delay_ms / spd)
