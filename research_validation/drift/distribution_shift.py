"""
Research Validation & Independent Scientific Verification Framework (RVISF)
Phase 40: Distribution Shift & Statistical Drift Laboratory

Implements mathematically rigorous divergence metrics to detect covariate and label shift:
- Population Stability Index (PSI)
- Wasserstein-1 Distance (Earth Mover's Distance)
- Kullback-Leibler (KL) Divergence
- Jensen-Shannon (JS) Divergence
- Maximum Mean Discrepancy (MMD) approximation
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


@dataclass
class DistributionDriftReport:
    """Comprehensive statistical drift quantification report."""
    feature_name: str
    psi: float
    wasserstein_distance: float
    kl_divergence: float
    js_divergence: float
    mmd_estimate: float
    drift_detected: bool
    drift_severity: str  # "NONE", "MODERATE", "SEVERE"
    interpretation: str
    details: Dict[str, Any] = field(default_factory=dict)


class DistributionShiftDetector:
    """
    Evaluates dataset drift and distribution divergence between reference (baseline) and target (production) sets.
    """

    @staticmethod
    def _create_histograms(
        ref: List[float],
        target: List[float],
        num_bins: int = 10,
        eps: float = 1e-6
    ) -> Tuple[List[float], List[float], List[float]]:
        """
        Create aligned probability histograms across reference and target data.
        Returns: (ref_probs, target_probs, bin_edges)
        """
        combined = ref + target
        min_val = min(combined)
        max_val = max(combined)
        if min_val == max_val:
            return [1.0], [1.0], [min_val, max_val + 1.0]

        bin_width = (max_val - min_val) / num_bins
        bin_edges = [min_val + i * bin_width for i in range(num_bins + 1)]

        ref_counts = [0] * num_bins
        for x in ref:
            idx = min(int((x - min_val) / bin_width), num_bins - 1)
            ref_counts[idx] += 1

        target_counts = [0] * num_bins
        for x in target:
            idx = min(int((x - min_val) / bin_width), num_bins - 1)
            target_counts[idx] += 1

        n_ref = len(ref)
        n_target = len(target)

        # Convert to probabilities with Laplace-like smoothing
        ref_probs = [(c + eps) / (n_ref + eps * num_bins) for c in ref_counts]
        target_probs = [(c + eps) / (n_target + eps * num_bins) for c in target_counts]

        return ref_probs, target_probs, bin_edges

    @classmethod
    def calculate_psi(cls, ref: List[float], target: List[float], num_bins: int = 10) -> float:
        """
        Calculate Population Stability Index (PSI):
        PSI = sum (P_target - P_ref) * ln(P_target / P_ref)
        """
        ref_p, target_p, _ = cls._create_histograms(ref, target, num_bins=num_bins)
        psi = sum((t - r) * math.log(t / r) for r, t in zip(ref_p, target_p))
        return max(0.0, psi)

    @classmethod
    def calculate_kl_divergence(cls, p: List[float], q: List[float], eps: float = 1e-12) -> float:
        """Calculate KL(P || Q) = sum P(i) * ln(P(i) / Q(i))."""
        return sum(pi * math.log(max(pi, eps) / max(qi, eps)) for pi, qi in zip(p, q) if pi > 0.0)

    @classmethod
    def calculate_js_divergence(cls, ref: List[float], target: List[float], num_bins: int = 10) -> float:
        """
        Calculate Jensen-Shannon Divergence:
        JS(P || Q) = 0.5 * KL(P || M) + 0.5 * KL(Q || M), where M = 0.5 * (P + Q)
        """
        p, q, _ = cls._create_histograms(ref, target, num_bins=num_bins)
        m = [0.5 * (pi + qi) for pi, qi in zip(p, q)]
        kl_pm = cls.calculate_kl_divergence(p, m)
        kl_qm = cls.calculate_kl_divergence(q, m)
        js = 0.5 * kl_pm + 0.5 * kl_qm
        return max(0.0, js)

    @staticmethod
    def calculate_wasserstein_1d(u: List[float], v: List[float]) -> float:
        """
        Calculate exact 1D 1-Wasserstein (Earth Mover's) Distance using sorted quantile CDF differences:
        W_1(u, v) = integral |F_u(x) - F_v(x)| dx = 1/K sum |u_sorted[k] - v_sorted[k]|
        """
        if not u or not v:
            return 0.0

        u_sorted = sorted(u)
        v_sorted = sorted(v)

        # Quantile resample to same length K
        k = 1000
        u_quantiles = [u_sorted[min(int(i * len(u_sorted) / k), len(u_sorted) - 1)] for i in range(k)]
        v_quantiles = [v_sorted[min(int(i * len(v_sorted) / k), len(v_sorted) - 1)] for i in range(k)]

        w1 = sum(abs(uq - vq) for uq, vq in zip(u_quantiles, v_quantiles)) / k
        return w1

    @staticmethod
    def calculate_mmd_rbf(x: List[float], y: List[float], gamma: float = 1.0) -> float:
        """
        Calculate Maximum Mean Discrepancy (MMD) with an RBF (Gaussian) kernel:
        MMD^2 = E[k(x,x')] + E[k(y,y')] - 2 E[k(x,y)]
        """
        if not x or not y:
            return 0.0

        len(x)
        len(y)

        # Subsample for computational efficiency if large
        max_s = 200
        sub_x = x[:max_s]
        sub_y = y[:max_s]
        nx, ny = len(sub_x), len(sub_y)

        def rbf(a: float, b: float) -> float:
            return math.exp(-gamma * ((a - b) ** 2))

        k_xx = sum(rbf(a, b) for a in sub_x for b in sub_x) / (nx * nx)
        k_yy = sum(rbf(a, b) for a in sub_y for b in sub_y) / (ny * ny)
        k_xy = sum(rbf(a, b) for a in sub_x for b in sub_y) / (nx * ny)

        mmd_sq = max(0.0, k_xx + k_yy - 2.0 * k_xy)
        return math.sqrt(mmd_sq)

    @classmethod
    def evaluate_feature_drift(
        cls,
        feature_name: str,
        baseline_samples: List[float],
        production_samples: List[float],
        psi_threshold_moderate: float = 0.1,
        psi_threshold_severe: float = 0.25
    ) -> DistributionDriftReport:
        """
        Comprehensive drift assessment across all divergence metrics.
        """
        if len(baseline_samples) < 5 or len(production_samples) < 5:
            return DistributionDriftReport(
                feature_name=feature_name,
                psi=0.0,
                wasserstein_distance=0.0,
                kl_divergence=0.0,
                js_divergence=0.0,
                mmd_estimate=0.0,
                drift_detected=False,
                drift_severity="NONE",
                interpretation="Insufficient samples for drift evaluation."
            )

        psi = cls.calculate_psi(baseline_samples, production_samples)
        w1 = cls.calculate_wasserstein_1d(baseline_samples, production_samples)
        js = cls.calculate_js_divergence(baseline_samples, production_samples)
        p, q, _ = cls._create_histograms(baseline_samples, production_samples)
        kl = cls.calculate_kl_divergence(p, q)
        mmd = cls.calculate_mmd_rbf(baseline_samples, production_samples)

        if psi >= psi_threshold_severe:
            severity = "SEVERE"
            detected = True
            interp = f"Severe distribution drift detected (PSI={psi:.4f} >= {psi_threshold_severe}). Retraining or model adjustment required."
        elif psi >= psi_threshold_moderate:
            severity = "MODERATE"
            detected = True
            interp = f"Moderate distribution drift detected (PSI={psi:.4f} >= {psi_threshold_moderate}). Investigation advised."
        else:
            severity = "NONE"
            detected = False
            interp = f"Distribution is stable (PSI={psi:.4f} < {psi_threshold_moderate}). No significant drift."

        return DistributionDriftReport(
            feature_name=feature_name,
            psi=psi,
            wasserstein_distance=w1,
            kl_divergence=kl,
            js_divergence=js,
            mmd_estimate=mmd,
            drift_detected=detected,
            drift_severity=severity,
            interpretation=interp,
            details={
                "n_baseline": len(baseline_samples),
                "n_production": len(production_samples),
            }
        )
