"""Exploration Engine & Multi-Armed Bandits for DocuTask ADIP Meta Layer.

Implements Upper Confidence Bound (UCB1) and Thompson Sampling to enable autonomous experimentation
and capability discovery with bounded exploration regret.
"""

from __future__ import annotations

import math
import random
from typing import Dict
from pydantic import BaseModel


class BanditArmState(BaseModel):
    """Execution statistics for a candidate planner capability arm."""
    arm_id: str
    name: str
    pull_count: int = 0
    total_reward: float = 0.0
    alpha_successes: float = 1.0
    beta_failures: float = 1.0

    @property
    def empirical_mean(self) -> float:
        return self.total_reward / max(1, self.pull_count)


class ExplorationDecision(BaseModel):
    """Result of Multi-Armed Bandit arm selection."""
    selected_arm_id: str
    strategy_name: str
    algorithm: str = "UCB1"
    score: float
    exploration_bonus: float
    is_exploratory_pull: bool
    rationale: str


class ExplorationEngine:
    """Manages exploration vs exploitation trade-offs across planning policies."""

    def __init__(self, exploration_c: float = 1.414, seed: int = 42) -> None:
        self.exploration_c = exploration_c
        self.random = random.Random(seed)
        self._arms: Dict[str, BanditArmState] = {
            "strat_alpha": BanditArmState(arm_id="strat_alpha", name="Strategy Alpha (Fast Turbo)", pull_count=12, total_reward=9.6, alpha_successes=10, beta_failures=3),
            "strat_beta": BanditArmState(arm_id="strat_beta", name="Strategy Beta (Deep Reasoning)", pull_count=18, total_reward=16.2, alpha_successes=17, beta_failures=2),
            "strat_gamma": BanditArmState(arm_id="strat_gamma", name="Strategy Gamma (Budget Frugal)", pull_count=8, total_reward=5.6, alpha_successes=6, beta_failures=3),
            "strat_delta": BanditArmState(arm_id="strat_delta", name="Strategy Delta (Adaptive Pareto)", pull_count=24, total_reward=22.8, alpha_successes=23, beta_failures=2),
        }

    def select_arm_ucb1(self) -> ExplorationDecision:
        total_pulls = sum(a.pull_count for a in self._arms.values())
        best_arm_id = None
        best_ucb = -1e9
        best_bonus = 0.0

        for arm_id, arm in self._arms.items():
            if arm.pull_count == 0:
                return ExplorationDecision(
                    selected_arm_id=arm_id,
                    strategy_name=arm.name,
                    algorithm="UCB1",
                    score=1e6,
                    exploration_bonus=1e6,
                    is_exploratory_pull=True,
                    rationale="Arm uninitialized; mandatory initial exploration pull.",
                )

            bonus = self.exploration_c * math.sqrt(math.log(max(1, total_pulls)) / arm.pull_count)
            ucb = arm.empirical_mean + bonus

            if ucb > best_ucb:
                best_ucb = ucb
                best_arm_id = arm_id
                best_bonus = bonus

        selected = self._arms[best_arm_id or "strat_delta"]
        is_exploratory = best_bonus > 0.35

        return ExplorationDecision(
            selected_arm_id=selected.arm_id,
            strategy_name=selected.name,
            algorithm="UCB1",
            score=round(best_ucb, 4),
            exploration_bonus=round(best_bonus, 4),
            is_exploratory_pull=is_exploratory,
            rationale=f"UCB1 score {best_ucb:.4f} (Mean {selected.empirical_mean:.3f} + Bonus {best_bonus:.3f}).",
        )

    def select_arm_thompson_sampling(self) -> ExplorationDecision:
        best_arm_id = None
        best_sample = -1.0

        for arm_id, arm in self._arms.items():
            # Sample from Beta distribution
            sample = self.random.betavariate(arm.alpha_successes, arm.beta_failures)
            if sample > best_sample:
                best_sample = sample
                best_arm_id = arm_id

        selected = self._arms[best_arm_id or "strat_delta"]
        return ExplorationDecision(
            selected_arm_id=selected.arm_id,
            strategy_name=selected.name,
            algorithm="ThompsonSampling",
            score=round(best_sample, 4),
            exploration_bonus=0.0,
            is_exploratory_pull=True,
            rationale=f"Thompson Sample drawn from Beta({selected.alpha_successes:.1f}, {selected.beta_failures:.1f}) = {best_sample:.4f}.",
        )

    def update_arm_reward(self, arm_id: str, reward: float) -> None:
        arm = self._arms.get(arm_id)
        if arm:
            arm.pull_count += 1
            arm.total_reward += reward
            if reward >= 0.7:
                arm.alpha_successes += 1.0
            else:
                arm.beta_failures += 1.0
