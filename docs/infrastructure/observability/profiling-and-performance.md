# Continuous Profiling & Performance Analysis Guide

## 1. CPU Sampling Profiler & Hotspot Detection
`CPUProfiler` collects stack traces at regular intervals (e.g. 10ms - 100Hz) with minimal CPU overhead.

```python
from app.infrastructure.observability.profiling import CPUProfiler

profiler = CPUProfiler(sampling_interval_ms=10)
profiler.start()
# ... workload executes ...
profile = profiler.stop()

# Detect functions consuming > 15% of total CPU time
hotspots = profiler.get_hotspots(threshold_percent=15.0)
for hs in hotspots:
    print(f"Hotspot: {hs.function_name} in {hs.file_name} ({hs.cpu_percent:.1f}%)")
```

## 2. Memory Allocation Profiler & Leak Detection
`MemoryProfiler` monitors heap allocations, object churn, and monotonic growth patterns:
```python
from app.infrastructure.observability.profiling import MemoryProfiler

mem_profiler = MemoryProfiler()
mem_profiler.start()
# ... workload executes ...
leak_warnings = mem_profiler.detect_leaks(growth_threshold_mb=50.0)
```

## 3. Interactive Flamegraph Generation
`FlamegraphGenerator` converts captured stack frames into hierarchical JSON and collapsed stack formats compatible with Speedscope and d3-flame-graph:
```python
from app.infrastructure.observability.profiling import FlamegraphGenerator

generator = FlamegraphGenerator()
flamegraph_json = generator.generate_flamegraph(profile)
collapsed_stacks = generator.export_collapsed_format(profile)
```
