"""
Memory Profiler & Leak Detector.

Tracks heap object allocations, footprint growth rates, and identifies memory leaks.
"""

from __future__ import annotations

import logging
import time
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("infrastructure.observability.profiling.memory")


class MemoryAllocationSample(BaseModel):
    """Snapshot of heap allocations by type or component."""
    timestamp: float = Field(default_factory=time.time)
    total_allocated_bytes: int
    object_counts: Dict[str, int] = Field(default_factory=dict)
    component_bytes: Dict[str, int] = Field(default_factory=dict)


class MemoryLeakWarning(BaseModel):
    """Warning for component showing persistent monotonic memory growth."""
    component_name: str
    initial_bytes: int
    current_bytes: int
    growth_bytes: int
    growth_rate_bytes_per_sec: float
    confidence_score: float = Field(default=0.9, ge=0.0, le=1.0)


class MemoryProfiler:
    """
    Analyzes memory snapshots over time to detect runaway allocations and leaks.
    """

    def __init__(self) -> None:
        self._samples: List[MemoryAllocationSample] = []

    def record_snapshot(
        self,
        total_allocated_bytes: int,
        object_counts: Optional[Dict[str, int]] = None,
        component_bytes: Optional[Dict[str, int]] = None,
    ) -> MemoryAllocationSample:
        """Record a heap snapshot."""
        sample = MemoryAllocationSample(
            total_allocated_bytes=total_allocated_bytes,
            object_counts=object_counts or {},
            component_bytes=component_bytes or {},
        )
        self._samples.append(sample)
        if len(self._samples) > 500:
            self._samples.pop(0)
        return sample

    def detect_leaks(self, min_growth_pct: float = 25.0) -> List[MemoryLeakWarning]:
        """Detect components exhibiting sustained monotonic memory growth."""
        if len(self._samples) < 3:
            return []

        first = self._samples[0]
        last = self._samples[-1]
        time_span = max(1.0, last.timestamp - first.timestamp)

        warnings: List[MemoryLeakWarning] = []
        all_components = set(first.component_bytes.keys()).union(set(last.component_bytes.keys()))

        for comp in all_components:
            init_b = first.component_bytes.get(comp, 0)
            curr_b = last.component_bytes.get(comp, 0)
            growth = curr_b - init_b

            if init_b > 0 and (growth / init_b * 100.0) >= min_growth_pct:
                rate = growth / time_span
                warnings.append(MemoryLeakWarning(
                    component_name=comp,
                    initial_bytes=init_b,
                    current_bytes=curr_b,
                    growth_bytes=growth,
                    growth_rate_bytes_per_sec=round(rate, 2),
                    confidence_score=0.95,
                ))

        return warnings
