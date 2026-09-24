"""
Online Drift Detection - Statistical Drift Metrics
Implements PSI (Population Stability Index), KL Divergence, Jensen-Shannon Divergence, and Wasserstein Distance.
"""

import math
from typing import List, Tuple


class StatisticalDriftMetrics:
    """Computes distribution divergence metrics between reference (baseline) and monitored production windows."""

    @staticmethod
    def _create_histograms(
        reference: List[float],
        current: List[float],
        num_bins: int = 10,
    ) -> Tuple[List[float], List[float]]:
        if not reference or not current:
            return ([1.0 / num_bins] * num_bins, [1.0 / num_bins] * num_bins)

        min_val = min(min(reference), min(current))
        max_val = max(max(reference), max(current))

        if min_val == max_val:
            # Degenerate constant distribution
            return ([1.0] + [0.0] * (num_bins - 1), [1.0] + [0.0] * (num_bins - 1))

        bin_width = (max_val - min_val) / num_bins
        ref_counts = [0] * num_bins
        cur_counts = [0] * num_bins

        for val in reference:
            idx = min(int((val - min_val) / bin_width), num_bins - 1)
            ref_counts[idx] += 1

        for val in current:
            idx = min(int((val - min_val) / bin_width), num_bins - 1)
            cur_counts[idx] += 1

        # Smooth to prevent zero probabilities (Laplace smoothing)
        epsilon = 1e-4
        n_ref = len(reference) + (epsilon * num_bins)
        n_cur = len(current) + (epsilon * num_bins)

        ref_probs = [(c + epsilon) / n_ref for c in ref_counts]
        cur_probs = [(c + epsilon) / n_cur for c in cur_counts]

        return ref_probs, cur_probs

    @classmethod
    def calculate_psi(cls, reference: List[float], current: List[float], num_bins: int = 10) -> float:
        """Population Stability Index (PSI) = sum((P_i - Q_i) * ln(P_i / Q_i))"""
        ref_p, cur_p = cls._create_histograms(reference, current, num_bins)
        psi = 0.0
        for p, q in zip(ref_p, cur_p):
            if p > 0 and q > 0:
                psi += (q - p) * math.log(q / p)
        return max(0.0, round(psi, 5))

    @classmethod
    def calculate_kl_divergence(cls, reference: List[float], current: List[float], num_bins: int = 10) -> float:
        """KL(P || Q) = sum(P_i * ln(P_i / Q_i))"""
        ref_p, cur_p = cls._create_histograms(reference, current, num_bins)
        kl = 0.0
        for p, q in zip(ref_p, cur_p):
            if p > 0 and q > 0:
                kl += p * math.log(p / q)
        return max(0.0, round(kl, 5))

    @classmethod
    def calculate_js_divergence(cls, reference: List[float], current: List[float], num_bins: int = 10) -> float:
        """Jensen-Shannon Divergence = 0.5 * KL(P || M) + 0.5 * KL(Q || M) where M = 0.5*(P + Q)"""
        ref_p, cur_p = cls._create_histograms(reference, current, num_bins)
        m = [0.5 * (p + q) for p, q in zip(ref_p, cur_p)]
        kl_pm = sum(p * math.log(p / mi) for p, mi in zip(ref_p, m) if p > 0 and mi > 0)
        kl_qm = sum(q * math.log(q / mi) for q, mi in zip(cur_p, m) if q > 0 and mi > 0)
        js = 0.5 * kl_pm + 0.5 * kl_qm
        return max(0.0, round(js, 5))

    @classmethod
    def calculate_wasserstein_distance(cls, reference: List[float], current: List[float]) -> float:
        """1D Earth Mover Distance / Wasserstein metric on sorted empirical quantiles."""
        if not reference or not current:
            return 0.0
        r_sorted = sorted(reference)
        c_sorted = sorted(current)
        # Interpolate / match length
        n = min(len(r_sorted), len(c_sorted))
        if n == 0:
            return 0.0
        r_samples = [r_sorted[int(i * len(r_sorted) / n)] for i in range(n)]
        c_samples = [c_sorted[int(i * len(c_sorted) / n)] for i in range(n)]
        dist = sum(abs(r - c) for r, c in zip(r_samples, c_samples)) / n
        return round(dist, 5)
