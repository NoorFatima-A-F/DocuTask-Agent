"""
Scientific Benchmarking Package.
Provides standardized benchmark suites, baselines, statistical significance testing, and experiment runners.
"""

from app.runtime.benchmarking.benchmark_suite import BenchmarkTask, BENCHMARK_SUITES
from app.runtime.benchmarking.baseline_policies import BaselinePolicies
from app.runtime.benchmarking.benchmark_statistics import BenchmarkStatistics
from app.runtime.benchmarking.experiment_runner import ExperimentRunner
from app.runtime.benchmarking.benchmark_engine import ScientificBenchmarkEngine, scientific_benchmark_engine

__all__ = [
    "BenchmarkTask",
    "BENCHMARK_SUITES",
    "BaselinePolicies",
    "BenchmarkStatistics",
    "ExperimentRunner",
    "ScientificBenchmarkEngine",
    "scientific_benchmark_engine",
]
