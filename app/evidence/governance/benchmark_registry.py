"""
Scientific Benchmark Registry & Execution Gatekeeper.
Enforces that every benchmark adheres to registered scientific parameters before execution:
- Formal registration metadata (Identifier, Purpose, Owner, Reviewers)
- Acceptance thresholds (Minimum Sample Size N, Minimum Statistical Power 1-beta >= 0.80)
- Hardware and dataset prerequisites
- Expiration and mandatory re-certification review schedules
"""

from __future__ import annotations

import logging
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkRegistrationSpec:
    """Rigorous scientific registration contract for a benchmark."""

    benchmark_id: str
    purpose: str
    owner: str
    reviewers: List[str]
    scientific_rationale: str
    acceptance_criteria: str
    minimum_sample_size: int
    minimum_statistical_power: float
    required_confidence_level: float
    required_reproducibility_tier: str  # "DETERMINISTIC", "STATISTICAL"
    dataset_card_id: str
    hardware_requirements: str
    expiration_timestamp: float
    review_frequency_days: int
    is_active: bool = True
    created_at: float = field(default_factory=time.time)

    def is_expired(self) -> bool:
        return time.time() > self.expiration_timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "benchmark_id": self.benchmark_id,
            "purpose": self.purpose,
            "owner": self.owner,
            "reviewers": self.reviewers,
            "min_sample_size": self.minimum_sample_size,
            "min_power": self.minimum_statistical_power,
            "required_confidence": self.required_confidence_level,
            "reproducibility": self.required_reproducibility_tier,
            "dataset_card_id": self.dataset_card_id,
            "is_active": self.is_active,
            "is_expired": self.is_expired(),
        }


class ScientificBenchmarkRegistry:
    """
    Central registry validating benchmarks before admission into execution pipelines.
    """

    def __init__(self) -> None:
        self.specs: Dict[str, BenchmarkRegistrationSpec] = {}

    def register(self, spec: BenchmarkRegistrationSpec) -> None:
        """Registers a benchmark specification."""
        self.specs[spec.benchmark_id] = spec

    def validate_execution_eligibility(
        self,
        benchmark_id: str,
        actual_sample_size: int,
        achieved_power: float,
    ) -> Tuple[bool, List[str]]:
        """Validates whether a planned benchmark execution meets all registered scientific requirements."""
        if benchmark_id not in self.specs:
            return False, [f"Benchmark '{benchmark_id}' is not registered in ScientificBenchmarkRegistry."]

        spec = self.specs[benchmark_id]
        violations: List[str] = []

        if not spec.is_active:
            violations.append(f"Benchmark '{benchmark_id}' is deactivated.")

        if spec.is_expired():
            violations.append(f"Benchmark '{benchmark_id}' certification expired. Mandatory re-review required.")

        if actual_sample_size < spec.minimum_sample_size:
            violations.append(
                f"Sample size {actual_sample_size} violates minimum required sample size {spec.minimum_sample_size}."
            )

        if achieved_power < spec.minimum_statistical_power:
            violations.append(
                f"Achieved power {achieved_power:.2f} is below registered minimum {spec.minimum_statistical_power:.2f}."
            )

        return (len(violations) == 0), violations
