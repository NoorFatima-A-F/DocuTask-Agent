"""
Autonomous Research - Exploration Strategies
Implements Multi-Armed Bandit exploration algorithms (Thompson Sampling & UCB1).
"""

import math
import random
from typing import Dict, List, Any


class ThompsonSamplingBandit:
    """Thompson Sampling for Bernoulli reward arms (explore vs exploit)."""

    def __init__(self, arm_names: List[str]):
        self.arm_names = arm_names
        # Beta priors (alpha=1, beta=1)
        self.alphas: Dict[str, float] = {arm: 1.0 for arm in arm_names}
        self.betas: Dict[str, float] = {arm: 1.0 for arm in arm_names}
        self.pull_counts: Dict[str, int] = {arm: 0 for arm in arm_names}

    def select_arm(self) -> str:
        sampled_theta: Dict[str, float] = {}
        for arm in self.arm_names:
            sampled_theta[arm] = random.betavariate(self.alphas[arm], self.betas[arm])
        best_arm = max(sampled_theta, key=sampled_theta.get)
        self.pull_counts[best_arm] += 1
        return best_arm

    def update(self, arm: str, reward: float):
        if arm in self.alphas:
            if reward > 0.5:
                self.alphas[arm] += 1.0
            else:
                self.betas[arm] += 1.0

    def get_arm_statistics(self) -> List[Dict[str, Any]]:
        stats = []
        for arm in self.arm_names:
            a = self.alphas[arm]
            b = self.betas[arm]
            expected_mean = a / (a + b)
            stats.append({
                "arm": arm,
                "pull_count": self.pull_counts[arm],
                "alpha": round(a, 2),
                "beta": round(b, 2),
                "expected_reward": round(expected_mean, 4),
            })
        return stats


class UCB1Bandit:
    """Upper Confidence Bound (UCB1) for bounded rewards."""

    def __init__(self, arm_names: List[str]):
        self.arm_names = arm_names
        self.counts: Dict[str, int] = {arm: 0 for arm in arm_names}
        self.values: Dict[str, float] = {arm: 0.0 for arm in arm_names}
        self.total_pulls = 0

    def select_arm(self) -> str:
        # First pull each arm once
        for arm in self.arm_names:
            if self.counts[arm] == 0:
                self.counts[arm] += 1
                self.total_pulls += 1
                return arm

        # Compute UCB scores
        scores: Dict[str, float] = {}
        for arm in self.arm_names:
            bonus = math.sqrt((2.0 * math.log(self.total_pulls)) / self.counts[arm])
            scores[arm] = self.values[arm] + bonus

        best_arm = max(scores, key=scores.get)
        self.counts[best_arm] += 1
        self.total_pulls += 1
        return best_arm

    def update(self, arm: str, reward: float):
        if arm in self.counts:
            n = self.counts[arm]
            val = self.values[arm]
            self.values[arm] = val + (reward - val) / n
