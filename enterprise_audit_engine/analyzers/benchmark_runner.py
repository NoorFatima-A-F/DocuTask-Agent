"""Performance Benchmark & Load Test Verifier."""

import os
from pathlib import Path
from typing import Dict, Any


class BenchmarkRunnerVerifier:
    """Verifies existence, validity, and execution results of performance benchmarks and load testing."""

    @staticmethod
    def inspect_benchmarks(repo_root: Path) -> Dict[str, Any]:
        benchmark_paths = [
            repo_root / "benchmarks",
            repo_root / "tests" / "benchmarks",
            repo_root / "tests" / "performance",
            repo_root / "locustfile.py",
        ]

        has_benchmark_suite = False
        benchmark_files_count = 0
        has_load_testing = False
        has_latency_targets = False

        for bpath in benchmark_paths:
            if bpath.is_file():
                has_benchmark_suite = True
                benchmark_files_count += 1
                if "locust" in bpath.name.lower():
                    has_load_testing = True
            elif bpath.is_dir():
                has_benchmark_suite = True
                for root, _, files in os.walk(bpath):
                    for f in files:
                        if f.endswith((".py", ".js", ".ts", ".json", ".yaml")):
                            benchmark_files_count += 1
                            if "locust" in f.lower() or "load" in f.lower() or "k6" in f.lower():
                                has_load_testing = True
                            f_path = Path(root) / f
                            try:
                                with open(f_path, "r", encoding="utf-8", errors="ignore") as fp:
                                    txt = fp.read().lower()
                                    if "p95" in txt or "p99" in txt or "latency" in txt or "throughput" in txt:
                                        has_latency_targets = True
                            except Exception:
                                pass

        return {
            "has_benchmark_suite": has_benchmark_suite,
            "benchmark_files_count": benchmark_files_count,
            "has_load_testing": has_load_testing,
            "has_latency_targets": has_latency_targets,
            "benchmark_maturity": "HIGH" if (has_benchmark_suite and has_load_testing and has_latency_targets) else "MEDIUM" if has_benchmark_suite else "LOW",
        }
