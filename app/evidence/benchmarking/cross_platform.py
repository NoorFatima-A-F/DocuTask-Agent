"""
Cross-Platform Validation Framework for AAOS.
Evaluates portability and performance divergence across host platforms:
- Windows (Local Desktop / Workstation)
- Linux (POSIX Standard)
- GitHub Actions CI (Virtual Host)
- Google Cloud Run (Container Sandbox)
- Google Kubernetes Engine (GKE Cluster Node)

Computes environment-normalized metrics, cross-platform effect sizes, and divergence factors.
"""

from __future__ import annotations

import logging
import math
import statistics
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class PlatformEnvironment(str, Enum):
    WINDOWS_DESKTOP = "WINDOWS_DESKTOP"
    LINUX_POSIX = "LINUX_POSIX"
    GITHUB_ACTIONS_CI = "GITHUB_ACTIONS_CI"
    GCP_CLOUD_RUN = "GCP_CLOUD_RUN"
    GCP_GKE_NODE = "GCP_GKE_NODE"


class PortabilityVerdict(str, Enum):
    PORTABLE_CONSISTENT = "PORTABLE_CONSISTENT"
    PORTABLE_SCALED = "PORTABLE_SCALED"
    PLATFORM_DIVERGENT = "PLATFORM_DIVERGENT"


@dataclass
class PlatformExecutionProfile:
    """Execution telemetry captured on a specific platform."""

    platform_env: PlatformEnvironment
    mean_duration_ms: float
    p95_duration_ms: float
    std_dev_ms: float
    cpu_cores: int
    ram_gb: float
    normalized_relative_speed: float  # Baseline = 1.0


@dataclass
class CrossPlatformReport:
    """Cross-platform comparative analysis report."""

    benchmark_name: str
    baseline_platform: PlatformEnvironment
    profiles: List[PlatformExecutionProfile]
    max_divergence_ratio: float
    platform_effect_size_d: float
    verdict: PortabilityVerdict
    summary_rationale: str
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "benchmark_name": self.benchmark_name,
            "baseline_platform": self.baseline_platform.value,
            "profiles": [asdict(p) for p in self.profiles],
            "max_divergence_ratio": round(self.max_divergence_ratio, 3),
            "platform_effect_size_d": round(self.platform_effect_size_d, 3),
            "verdict": self.verdict.value,
            "summary_rationale": self.summary_rationale,
        }


class CrossPlatformValidationEngine:
    """
    Evaluates benchmark results across diverse operating systems and cloud runtime environments.
    """

    MAX_ACCEPTABLE_DIVERGENCE: float = 3.5  # Max 3.5x ratio across hardware tiers

    @classmethod
    def compare_platforms(
        cls,
        benchmark_name: str,
        platform_samples: Dict[PlatformEnvironment, List[float]],
        baseline: PlatformEnvironment = PlatformEnvironment.LINUX_POSIX,
    ) -> CrossPlatformReport:
        """Analyzes execution samples collected across multiple target environments."""
        if not platform_samples:
            raise ValueError("Must provide at least one platform dataset for comparison")

        if baseline not in platform_samples:
            baseline = next(iter(platform_samples.keys()))

        baseline_mean = statistics.mean(platform_samples[baseline]) if platform_samples[baseline] else 1.0
        baseline_std = statistics.stdev(platform_samples[baseline]) if len(platform_samples[baseline]) > 1 else 1.0

        profiles: List[PlatformExecutionProfile] = []
        all_means: List[float] = []

        for p_env, samples in platform_samples.items():
            if not samples:
                continue
            mean_v = statistics.mean(samples)
            std_v = statistics.stdev(samples) if len(samples) > 1 else 0.0
            sorted_v = sorted(samples)
            p95_v = sorted_v[int(len(samples) * 0.95)]
            rel_speed = mean_v / max(1e-9, baseline_mean)

            profiles.append(
                PlatformExecutionProfile(
                    platform_env=p_env,
                    mean_duration_ms=mean_v,
                    p95_duration_ms=p95_v,
                    std_dev_ms=std_v,
                    cpu_cores=8,
                    ram_gb=16.0,
                    normalized_relative_speed=rel_speed,
                )
            )
            all_means.append(mean_v)

        max_mean = max(all_means)
        min_mean = min(all_means)
        divergence_ratio = max_mean / max(1e-9, min_mean)

        # Cross-platform effect size (Cohen's d max vs min)
        effect_d = (max_mean - min_mean) / max(1e-9, baseline_std)

        if divergence_ratio <= 1.5:
            verdict = PortabilityVerdict.PORTABLE_CONSISTENT
            rationale = f"Workload shows near-identical performance across platforms (Divergence: {divergence_ratio:.2f}x <= 1.5x)."
        elif divergence_ratio <= cls.MAX_ACCEPTABLE_DIVERGENCE:
            verdict = PortabilityVerdict.PORTABLE_SCALED
            rationale = f"Workload scales predictably with platform virtualization overhead (Divergence: {divergence_ratio:.2f}x)."
        else:
            verdict = PortabilityVerdict.PLATFORM_DIVERGENT
            rationale = f"REJECTED: Severe platform divergence detected ({divergence_ratio:.2f}x > {cls.MAX_ACCEPTABLE_DIVERGENCE}x). Workload is non-portable."

        return CrossPlatformReport(
            benchmark_name=benchmark_name,
            baseline_platform=baseline,
            profiles=profiles,
            max_divergence_ratio=divergence_ratio,
            platform_effect_size_d=effect_d,
            verdict=verdict,
            summary_rationale=rationale,
        )
