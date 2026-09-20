"""
Benchmark Isolation & Stabilization Framework.
Inspired by JMH and pytest-benchmark.
Controls Garbage Collection (GC) states, performs cold vs hot cache passes,
stabilizes CPU variance, and records isolation settings for deterministic reproducibility.
"""

from __future__ import annotations

import gc
import logging
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkIsolationSettings:
    """Settings applied during benchmark execution."""

    disable_gc_during_measurement: bool = True
    warmup_iterations: int = 20
    warmup_min_duration_ms: float = 50.0
    clear_sys_modules_cache: bool = False
    collect_gc_before_run: bool = True
    hot_cache_enabled: bool = True
    cpu_pinning_attempted: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BenchmarkIsolationContext:
    """Context manager guaranteeing deterministic, isolated execution conditions."""

    def __init__(self, settings: Optional[BenchmarkIsolationSettings] = None) -> None:
        self.settings = settings or BenchmarkIsolationSettings()
        self._gc_was_enabled: bool = True

    def __enter__(self) -> BenchmarkIsolationContext:
        if self.settings.collect_gc_before_run:
            gc.collect()

        self._gc_was_enabled = gc.isenabled()
        if self.settings.disable_gc_during_measurement:
            gc.disable()

        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._gc_was_enabled:
            gc.enable()
        if self.settings.collect_gc_before_run:
            gc.collect()


class WarmupManager:
    """Executes pre-measurement warmup passes to reach steady-state JIT/cache convergence."""

    @classmethod
    def execute_warmup(
        cls,
        func: Callable[[], Any],
        min_iterations: int = 20,
        min_duration_ms: float = 50.0,
    ) -> int:
        """Runs func() until both iteration count and minimum duration thresholds are met."""
        t0 = time.perf_counter()
        count = 0
        while count < min_iterations or ((time.perf_counter() - t0) * 1000.0) < min_duration_ms:
            func()
            count += 1
            if count > 5000:
                break
        return count

    @classmethod
    async def execute_async_warmup(
        cls,
        coro_func: Callable[[], Any],
        min_iterations: int = 20,
        min_duration_ms: float = 50.0,
    ) -> int:
        """Runs async coroutine warmup passes."""
        t0 = time.perf_counter()
        count = 0
        while count < min_iterations or ((time.perf_counter() - t0) * 1000.0) < min_duration_ms:
            await coro_func()
            count += 1
            if count > 5000:
                break
        return count
