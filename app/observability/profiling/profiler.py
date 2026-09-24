"""Continuous Profiler for Execution Latencies and Resource Spikes."""

from __future__ import annotations

import contextlib
import time
from dataclasses import dataclass, field
from typing import Generator, List, Optional


@dataclass
class ProfileSample:
    function_name: str
    duration_ms: float
    cpu_time_ms: float = 0.0
    memory_delta_kb: float = 0.0
    timestamp: float = field(default_factory=time.time)


class ContinuousProfiler:
    """Continuous lightweight profiler collecting function and pipeline execution performance samples."""

    def __init__(self, max_samples: int = 5000):
        self.max_samples = max_samples
        self._samples: List[ProfileSample] = []

    def record_sample(
        self,
        function_name: str,
        duration_ms: float,
        cpu_time_ms: float = 0.0,
        memory_delta_kb: float = 0.0,
    ) -> ProfileSample:
        sample = ProfileSample(
            function_name=function_name,
            duration_ms=duration_ms,
            cpu_time_ms=cpu_time_ms,
            memory_delta_kb=memory_delta_kb,
        )
        self._samples.append(sample)
        if len(self._samples) > self.max_samples:
            self._samples.pop(0)
        return sample

    @contextlib.contextmanager
    def profile_block(self, block_name: str) -> Generator[None, None, None]:
        start_time = time.time()
        try:
            yield
        finally:
            duration_ms = (time.time() - start_time) * 1000.0
            self.record_sample(block_name, duration_ms)

    def list_samples(self, function_name: Optional[str] = None) -> List[ProfileSample]:
        if function_name:
            return [s for s in self._samples if s.function_name == function_name]
        return list(self._samples)

    def clear(self) -> None:
        self._samples.clear()
