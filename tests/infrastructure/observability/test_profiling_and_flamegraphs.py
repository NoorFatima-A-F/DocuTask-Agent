"""
Tests for CPU Profiler, Memory Profiler, and Flamegraph Generation.
"""

import time
import pytest

from app.infrastructure.observability.profiling.cpu import (
    CPUHotspot,
    CPUProfileSample,
    CPUProfiler,
    StackFrame,
)
from app.infrastructure.observability.profiling.memory import (
    MemoryAllocationSample,
    MemoryLeakWarning,
    MemoryProfiler,
)
from app.infrastructure.observability.profiling.flamegraphs import (
    FlamegraphGenerator,
)


def test_cpu_profiler_and_hotspots():
    profiler = CPUProfiler()

    # Record stack samples
    frame_root = StackFrame(function_name="main", file_name="app.py", line_number=10)
    frame_ocr = StackFrame(function_name="tesseract_ocr", file_name="ocr.py", line_number=45)
    frame_embed = StackFrame(function_name="embed_vector", file_name="embed.py", line_number=88)

    for i in range(8):
        profiler.record_sample(
            sample_id=f"sample-ocr-{i}",
            frames=[frame_root, frame_ocr],
            duration_ms=20.0,
        )

    for i in range(2):
        profiler.record_sample(
            sample_id=f"sample-embed-{i}",
            frames=[frame_root, frame_embed],
            duration_ms=10.0,
        )

    hotspots = profiler.analyze_hotspots(top_n=5)
    assert len(hotspots) == 2
    assert hotspots[0].function_name == "tesseract_ocr"
    assert hotspots[0].percentage_of_total > 80.0
    assert hotspots[0].sample_count == 8


def test_memory_profiler_leak_detection():
    profiler = MemoryProfiler()
    now = time.time()

    # Simulate monotonic heap growth in 'embedding_cache'
    for i in range(5):
        profiler._samples.append(
            MemoryAllocationSample(
                timestamp=now + (i * 10.0),
                total_allocated_bytes=100_000_000 + (i * 50_000_000),
                component_bytes={"embedding_cache": 50_000_000 + (i * 40_000_000)},
            )
        )

    warnings = profiler.detect_leaks(min_growth_pct=50.0)
    assert len(warnings) == 1
    assert warnings[0].component_name == "embedding_cache"
    assert warnings[0].growth_rate_bytes_per_sec > 0


def test_flamegraph_generator():
    frame1 = StackFrame(function_name="main", file_name="main.py", line_number=1)
    frame2 = StackFrame(function_name="process_batch", file_name="batch.py", line_number=10)
    frame3 = StackFrame(function_name="tokenize", file_name="tok.py", line_number=20)

    samples = [
        CPUProfileSample(sample_id="s1", thread_id="t1", frames=[frame1, frame2, frame3], duration_ms=50.0),
        CPUProfileSample(sample_id="s2", thread_id="t1", frames=[frame1, frame2], duration_ms=25.0),
    ]

    # Folded stacks
    collapsed = FlamegraphGenerator.generate_collapsed_stacks(samples)
    assert len(collapsed) == 2
    assert "main;process_batch;tokenize 50" in collapsed
    assert "main;process_batch 25" in collapsed

    # Flamegraph tree
    tree = FlamegraphGenerator.generate_tree(samples)
    assert tree.name == "root"
    assert tree.value == 75.0
    assert len(tree.children) == 1
    assert tree.children[0].name == "main"
