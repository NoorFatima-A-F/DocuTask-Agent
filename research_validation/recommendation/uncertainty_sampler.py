"""
Uncertainty Sampler (Phase 85C)
==============================
Identifies regions of experimental parameter space or benchmark coverage
with the highest epistemic uncertainty or lowest statistical sample power.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class UncertaintyTarget:
    """A scientific domain or benchmark region requiring more empirical observations."""
    target_name: str
    current_sample_count: int
    current_uncertainty_std: float
    required_sample_count: int
    epistemic_gap: float
    priority_level: str  # "HIGH", "MEDIUM", "LOW"


class UncertaintySampler:
    """
    Active learning uncertainty sampler to prioritize high-entropy experiments.
    """

    @classmethod
    def identify_gaps(
        cls,
        benchmark_observations: Dict[str, Tuple[int, float]],  # name -> (sample_count, std_dev)
        min_desired_samples: int = 100,
        target_max_std: float = 0.02,
    ) -> List[UncertaintyTarget]:
        targets: List[UncertaintyTarget] = []

        for name, (count, std_dev) in benchmark_observations.items():
            sample_gap = max(0, min_desired_samples - count)
            std_gap = max(0.0, std_dev - target_max_std)
            epistemic_gap = (sample_gap / min_desired_samples) * 0.5 + (std_gap / max(1e-4, target_max_std)) * 0.5

            if epistemic_gap > 0.6:
                prio = "HIGH"
            elif epistemic_gap > 0.2:
                prio = "MEDIUM"
            else:
                prio = "LOW"

            targets.append(UncertaintyTarget(
                target_name=name,
                current_sample_count=count,
                current_uncertainty_std=std_dev,
                required_sample_count=min_desired_samples,
                epistemic_gap=epistemic_gap,
                priority_level=prio,
            ))

        return sorted(targets, key=lambda t: t.epistemic_gap, reverse=True)
