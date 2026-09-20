"""
Online Drift Detection - Sequential Drift Detectors
Implements streaming sequential change-point algorithms: CUSUM, Page-Hinkley, and ADWIN.
"""

import math
from typing import List, Dict, Any, Optional


class CUSUMDetector:
    """Cumulative Sum (CUSUM) change detection algorithm."""

    def __init__(self, target_mean: float = 0.0, allowance_k: float = 0.5, threshold_h: float = 5.0):
        self.target_mean = target_mean
        self.k = allowance_k
        self.h = threshold_h
        self.s_pos = 0.0
        self.s_neg = 0.0
        self.change_detected = False

    def update(self, value: float) -> bool:
        diff = value - self.target_mean
        self.s_pos = max(0.0, self.s_pos + diff - self.k)
        self.s_neg = max(0.0, self.s_neg - diff - self.k)
        if self.s_pos > self.h or self.s_neg > self.h:
            self.change_detected = True
            return True
        return False

    def reset(self):
        self.s_pos = 0.0
        self.s_neg = 0.0
        self.change_detected = False


class PageHinkleyDetector:
    """Page-Hinkley sequential test for detecting changes in average values."""

    def __init__(self, delta: float = 0.005, threshold_lambda: float = 50.0, alpha: float = 0.9999):
        self.delta = delta
        self.threshold = threshold_lambda
        self.alpha = alpha
        self.mean = 0.0
        self.n = 0
        self.sum_val = 0.0
        self.min_sum = 0.0

    def update(self, value: float) -> bool:
        self.n += 1
        self.mean = self.mean + (value - self.mean) / self.n
        self.sum_val = self.sum_val + (value - self.mean - self.delta)
        if self.sum_val < self.min_sum:
            self.min_sum = self.sum_val
        ph_stat = self.sum_val - self.min_sum
        return ph_stat > self.threshold

    def reset(self):
        self.mean = 0.0
        self.n = 0
        self.sum_val = 0.0
        self.min_sum = 0.0


class ADWINDetector:
    """Adaptive Windowing (ADWIN) algorithm for streaming concept drift detection."""

    def __init__(self, delta: float = 0.002, max_window_size: int = 1000):
        self.delta = delta
        self.max_window_size = max_window_size
        self.window: List[float] = []

    def update(self, value: float) -> bool:
        self.window.append(value)
        if len(self.window) > self.max_window_size:
            self.window.pop(0)

        n = len(self.window)
        if n < 10:
            return False

        # Test sub-window partition splits
        for split in range(5, n - 5, max(1, n // 20)):
            w0 = self.window[:split]
            w1 = self.window[split:]
            n0 = len(w0)
            n1 = len(w1)
            mu0 = sum(w0) / n0
            mu1 = sum(w1) / n1
            m = 1.0 / (1.0 / n0 + 1.0 / n1)
            # Hoeffding-like bound
            eps_cut = math.sqrt((1.0 / (2.0 * m)) * math.log(4.0 * n / self.delta))
            if abs(mu0 - mu1) >= eps_cut:
                # Drift detected! Shrink window to recent partition
                self.window = w1
                return True
        return False
