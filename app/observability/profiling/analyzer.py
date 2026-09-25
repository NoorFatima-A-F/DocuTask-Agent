"""Performance Hotspot Analyzer and Flamegraph Data Generator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .profiler import ContinuousProfiler, ProfileSample


@dataclass
class Hotspot:
    function_name: str
    total_duration_ms: float
    avg_duration_ms: float
    max_duration_ms: float
    call_count: int
    percent_of_total_time: float


class HotspotAnalyzer:
    """Analyzes continuous profiling samples to identify performance bottlenecks and flamegraphs."""

    def __init__(self, profiler: Optional[ContinuousProfiler] = None):
        self.profiler = profiler or ContinuousProfiler()

    def identify_hotspots(self) -> List[Hotspot]:
        samples = self.profiler.list_samples()
        if not samples:
            return []

        grouped: Dict[str, List[ProfileSample]] = {}
        total_time_all = sum(s.duration_ms for s in samples)

        for s in samples:
            if s.function_name not in grouped:
                grouped[s.function_name] = []
            grouped[s.function_name].append(s)

        hotspots: List[Hotspot] = []
        for fn_name, fn_samples in grouped.items():
            total_fn = sum(s.duration_ms for s in fn_samples)
            count = len(fn_samples)
            avg_fn = total_fn / count
            max_fn = max(s.duration_ms for s in fn_samples)
            pct = (total_fn / total_time_all * 100.0) if total_time_all > 0 else 0.0

            hotspots.append(
                Hotspot(
                    function_name=fn_name,
                    total_duration_ms=round(total_fn, 2),
                    avg_duration_ms=round(avg_fn, 2),
                    max_duration_ms=round(max_fn, 2),
                    call_count=count,
                    percent_of_total_time=round(pct, 2),
                )
            )

        hotspots.sort(key=lambda h: h.total_duration_ms, reverse=True)
        return hotspots

    def generate_flamegraph_hierarchy(self) -> Dict[str, Any]:
        """Generate hierarchical node structure for flamegraph visualization."""
        hotspots = self.identify_hotspots()
        return {
            "name": "root",
            "value": sum(h.total_duration_ms for h in hotspots),
            "children": [
                {
                    "name": h.function_name,
                    "value": h.total_duration_ms,
                    "call_count": h.call_count,
                    "percent": h.percent_of_total_time,
                }
                for h in hotspots
            ],
        }
