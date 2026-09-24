"""
CPU Profiler & Hotspot Detector.

Provides sampling-based CPU profiling, call-stack aggregation,
and identification of computational hotspots across worker nodes.
"""

from __future__ import annotations

import logging
import time
from typing import Dict, List
from pydantic import BaseModel, Field

logger = logging.getLogger("infrastructure.observability.profiling.cpu")


class StackFrame(BaseModel):
    """Single execution frame in a call stack."""
    function_name: str
    file_name: str
    line_number: int


class CPUProfileSample(BaseModel):
    """CPU execution sample containing stack trace and execution weight."""
    sample_id: str
    thread_id: str
    frames: List[StackFrame] = Field(default_factory=list)
    duration_ms: float = 10.0
    timestamp: float = Field(default_factory=time.time)


class CPUHotspot(BaseModel):
    """Detected function consuming significant CPU runtime."""
    function_name: str
    file_name: str
    total_time_ms: float
    percentage_of_total: float
    sample_count: int


class CPUProfiler:
    """
    Collects execution stack samples and computes CPU hotspot analysis.
    """

    def __init__(self) -> None:
        self._samples: List[CPUProfileSample] = []

    def record_sample(
        self,
        sample_id: str,
        frames: List[StackFrame],
        thread_id: str = "main",
        duration_ms: float = 10.0,
    ) -> CPUProfileSample:
        """Record a sampled CPU execution state."""
        sample = CPUProfileSample(
            sample_id=sample_id,
            thread_id=thread_id,
            frames=frames,
            duration_ms=duration_ms,
        )
        self._samples.append(sample)
        if len(self._samples) > 2000:
            self._samples.pop(0)
        return sample

    def analyze_hotspots(self, top_n: int = 10) -> List[CPUHotspot]:
        """Identify top functions by execution time across recorded samples."""
        if not self._samples:
            return []

        total_cpu_time = sum(s.duration_ms for s in self._samples)
        fn_times: Dict[str, float] = {}
        fn_counts: Dict[str, int] = {}
        fn_files: Dict[str, str] = {}

        for sample in self._samples:
            if sample.frames:
                # Top-of-stack is executing function
                top = sample.frames[-1]
                fn_key = f"{top.file_name}:{top.function_name}"
                fn_times[fn_key] = fn_times.get(fn_key, 0.0) + sample.duration_ms
                fn_counts[fn_key] = fn_counts.get(fn_key, 0) + 1
                fn_files[fn_key] = top.file_name

        hotspots: List[CPUHotspot] = []
        for fn_key, t_ms in fn_times.items():
            fn_name = fn_key.split(":")[-1]
            pct = (t_ms / total_cpu_time * 100.0) if total_cpu_time > 0 else 0.0
            hotspots.append(CPUHotspot(
                function_name=fn_name,
                file_name=fn_files[fn_key],
                total_time_ms=round(t_ms, 2),
                percentage_of_total=round(pct, 2),
                sample_count=fn_counts[fn_key],
            ))

        hotspots.sort(key=lambda h: h.total_time_ms, reverse=True)
        return hotspots[:top_n]

    def clear(self) -> None:
        self._samples.clear()
