"""
Scientific Benchmark Engine - Benchmark Suite
Defines standardized enterprise document processing test suites and synthetic workload distributions.
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass(frozen=True)
class BenchmarkTask:
    task_id: str
    workload_type: str
    document_complexity: float
    token_count: int
    ideal_accuracy: float
    sla_deadline_ms: float
    max_budget_usd: float


BENCHMARK_SUITES: Dict[str, List[BenchmarkTask]] = {
    "enterprise_invoices": [
        BenchmarkTask(f"inv_{i}", "Standard Invoice", 0.35, 1800, 0.98, 2000.0, 0.03)
        for i in range(1, 11)
    ],
    "tax_forms_multilingual": [
        BenchmarkTask(f"tax_{i}", "Tax Form 1040/W2", 0.75, 4500, 0.99, 4000.0, 0.05)
        for i in range(1, 11)
    ],
    "legal_contracts_dense": [
        BenchmarkTask(f"legal_{i}", "Legal Contract & NDA", 0.85, 8000, 0.97, 6000.0, 0.08)
        for i in range(1, 11)
    ],
    "high_volume_batch": [
        BenchmarkTask(f"batch_{i}", "High Volume Receipt", 0.20, 800, 0.92, 1000.0, 0.01)
        for i in range(1, 11)
    ],
}
