"""Belief State Engine for DocuTask Autonomous Decision Intelligence Platform (ADIP).

Maintains probability distributions over world state variables instead of binary assertions,
supporting Bayesian updates, Shannon entropy metrics, credible intervals, Kalman filtering, and belief versioning.
"""

from __future__ import annotations

import math
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class BetaBelief(BaseModel):
    """Beta distribution parameterization for a continuous probability in [0, 1]."""
    alpha: float = Field(default=1.0, ge=0.001, description="Pseudo-counts of successes")
    beta_param: float = Field(default=1.0, ge=0.001, description="Pseudo-counts of failures")
    name: str = ""
    description: str = ""

    @property
    def mean(self) -> float:
        return self.alpha / (self.alpha + self.beta_param)

    @property
    def variance(self) -> float:
        ab = self.alpha + self.beta_param
        return (self.alpha * self.beta_param) / ((ab ** 2) * (ab + 1.0))

    @property
    def std_dev(self) -> float:
        return math.sqrt(max(1e-9, self.variance))

    def get_credible_interval_95(self) -> tuple[float, float]:
        """Normal approximation to 95% credible interval bounded to [0, 1]."""
        m = self.mean
        s = self.std_dev
        lower = max(0.0, m - (1.96 * s))
        upper = min(1.0, m + (1.96 * s))
        return (round(lower, 4), round(upper, 4))

    def shannon_entropy(self) -> float:
        """Binary Shannon entropy in bits for Bernoulli trial with parameter p = mean."""
        p = max(1e-6, min(1.0 - 1e-6, self.mean))
        return -(p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p))

    def update_evidence(self, successes: float, failures: float) -> BetaBelief:
        """Exact Bayesian conjugate update for Beta-Binomial likelihood."""
        return BetaBelief(
            alpha=self.alpha + successes,
            beta_param=self.beta_param + failures,
            name=self.name,
            description=self.description,
        )


class KalmanBelief(BaseModel):
    """1D Kalman Filter state for continuous Gaussian variables (e.g. worker latency ms)."""
    state_mean: float = 250.0
    state_variance: float = 2500.0
    process_noise_q: float = 10.0
    measurement_noise_r: float = 50.0
    name: str = "worker_latency_ms"

    def predict_step(self) -> None:
        """Time update (predict next step)."""
        self.state_variance += self.process_noise_q

    def update_measurement(self, measurement: float) -> float:
        """Measurement update with Kalman Gain."""
        self.predict_step()
        kalman_gain = self.state_variance / (self.state_variance + self.measurement_noise_r)
        self.state_mean = self.state_mean + kalman_gain * (measurement - self.state_mean)
        self.state_variance = (1.0 - kalman_gain) * self.state_variance
        return self.state_mean


class BeliefSnapshot(BaseModel):
    """Immutable snapshot of the multi-dimensional belief state."""
    snapshot_id: str = Field(default_factory=lambda: f"snap_{uuid.uuid4().hex[:8]}")
    mission_id: str
    version: int
    beliefs: Dict[str, BetaBelief] = Field(default_factory=dict)
    kalman_states: Dict[str, KalmanBelief] = Field(default_factory=dict)
    total_entropy_bits: float
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BeliefStateEngine:
    """Manages full probabilistic belief state representation and evolution."""

    def __init__(self, mission_id: str = "default_mission") -> None:
        self.mission_id = mission_id
        self.version = 1
        self._beliefs: Dict[str, BetaBelief] = {}
        self._kalman_states: Dict[str, KalmanBelief] = {}
        self._history: List[BeliefSnapshot] = []
        self._initialize_default_priors()

    def _initialize_default_priors(self) -> None:
        """Initializes 10 uninformative/empirically calibrated prior distributions."""
        priors = {
            "worker_alive": (19.0, 1.0, "Probability that cluster worker node remains operational"),
            "document_damaged": (2.0, 8.0, "Probability that document is blurry, torn, or skewed"),
            "layout_complex": (4.0, 6.0, "Probability that document has borderless tables or multi-column layout"),
            "api_failure": (1.0, 32.0, "Probability of upstream API 429/503 quota throttling"),
            "memory_corrupted": (0.5, 49.5, "Probability that vector index or context memory is corrupted"),
            "cost_overrun": (1.5, 18.5, "Probability that token consumption breaches budget"),
            "sla_violation": (1.0, 19.0, "Probability of critical path exceeding SLA deadline"),
            "ocr_success": (18.0, 2.0, "Probability of successful OCR extraction exceeding confidence bar"),
            "schema_valid": (19.0, 1.0, "Probability of extracted JSON satisfying Pydantic schema"),
            "agent_failure": (1.0, 24.0, "Probability of worker agent unhandled exception"),
        }

        for name, (alpha, beta, desc) in priors.items():
            self._beliefs[name] = BetaBelief(alpha=alpha, beta_param=beta, name=name, description=desc)

        # Kalman state trackers
        self._kalman_states["execution_latency_ms"] = KalmanBelief(state_mean=450.0, state_variance=1200.0, name="execution_latency_ms")
        self._kalman_states["worker_cpu_utilization"] = KalmanBelief(state_mean=35.0, state_variance=100.0, name="worker_cpu_utilization")

        self._record_snapshot()

    def get_belief(self, name: str) -> Optional[BetaBelief]:
        return self._beliefs.get(name)

    def list_beliefs(self) -> Dict[str, BetaBelief]:
        return dict(self._beliefs)

    def compute_total_entropy(self) -> float:
        """Computes aggregate Shannon entropy across all belief variables in bits."""
        return sum(b.shannon_entropy() for b in self._beliefs.values())

    def update_belief(self, name: str, successes: float, failures: float) -> tuple[BetaBelief, float]:
        """Performs conjugate update and returns (updated_belief, entropy_delta)."""
        current = self._beliefs.get(name)
        if not current:
            current = BetaBelief(alpha=1.0, beta_param=1.0, name=name)

        old_entropy = current.shannon_entropy()
        updated = current.update_evidence(successes, failures)
        self._beliefs[name] = updated
        new_entropy = updated.shannon_entropy()

        self.version += 1
        self._record_snapshot()
        return updated, round(new_entropy - old_entropy, 4)

    def update_continuous_metric(self, metric_name: str, observation: float) -> float:
        state = self._kalman_states.get(metric_name)
        if not state:
            state = KalmanBelief(state_mean=observation, state_variance=100.0, name=metric_name)
            self._kalman_states[metric_name] = state
        updated_mean = state.update_measurement(observation)
        self.version += 1
        return updated_mean

    def _record_snapshot(self) -> None:
        snap = BeliefSnapshot(
            mission_id=self.mission_id,
            version=self.version,
            beliefs=dict(self._beliefs),
            kalman_states=dict(self._kalman_states),
            total_entropy_bits=round(self.compute_total_entropy(), 4),
        )
        self._history.append(snap)

    def get_snapshots(self) -> List[BeliefSnapshot]:
        return list(self._history)
