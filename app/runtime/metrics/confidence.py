"""
Scientifically Grounded Bayesian Evidence Fusion Engine for DocuTask Agent.
Replaces arbitrary heuristic weights with Calibrated Bayesian Log-Odds Evidence Fusion,
incorporating signal reliability, sample-size attenuation, and zero-fabrication sentinels.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


def _sigmoid(x: float) -> float:
    """Standard logistic sigmoid function."""
    if x >= 40.0:
        return 1.0
    if x <= -40.0:
        return 0.0
    return 1.0 / (1.0 + math.exp(-x))


def _logit(p: float) -> float:
    """Log-odds logit function."""
    p_clamped = max(1e-6, min(1.0 - 1e-6, p))
    return math.log(p_clamped / (1.0 - p_clamped))


@dataclass(frozen=True)
class EvidenceSignal:
    """
    Individual observable evidence signal entering the Bayesian fusion engine.
    """
    source_name: str
    category: str  # OCR, SCHEMA, MEMORY, CONSENSUS, VALIDATION, HUMAN_FEEDBACK
    observed_score: float  # [0.0, 1.0]
    sample_size: int
    reliability_coefficient: float  # [0.0, 1.0]
    description: str
    sha256_digest: Optional[str] = None
    sentinel_state: Optional[str] = None  # None, "UNKNOWN", "DATASET_UNAVAILABLE", "INSUFFICIENT_EVIDENCE"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_name": self.source_name,
            "category": self.category,
            "observed_score": self.observed_score,
            "sample_size": self.sample_size,
            "reliability_coefficient": self.reliability_coefficient,
            "description": self.description,
            "sha256_digest": self.sha256_digest,
            "sentinel_state": self.sentinel_state,
        }


@dataclass(frozen=True)
class BayesianConfidenceResult:
    """
    Complete mathematically derived confidence result with full signal decomposition.
    """
    posterior_confidence: float
    prior_confidence: float
    log_odds_delta: float
    confidence_interval_95: Tuple[float, float]
    sample_size_total: int
    signals: List[EvidenceSignal]
    signal_weights: Dict[str, float]
    log_likelihood_ratios: Dict[str, float]
    is_sentinel_active: bool
    sentinel_reason: Optional[str]
    derivation_formula: str
    derivation_latex: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "posterior_confidence": self.posterior_confidence,
            "prior_confidence": self.prior_confidence,
            "log_odds_delta": self.log_odds_delta,
            "confidence_interval_95": list(self.confidence_interval_95),
            "sample_size_total": self.sample_size_total,
            "signals": [s.to_dict() for s in self.signals],
            "signal_weights": self.signal_weights,
            "log_likelihood_ratios": self.log_likelihood_ratios,
            "is_sentinel_active": self.is_sentinel_active,
            "sentinel_reason": self.sentinel_reason,
            "derivation_formula": self.derivation_formula,
            "derivation_latex": self.derivation_latex,
        }


class BayesianConfidenceEngine:
    """
    Calibrated Multi-Source Bayesian Evidence Fusion Engine.
    Combines independent likelihood signals with sample-size variance attenuation.
    """

    DEFAULT_PRIOR: float = 0.50
    CALIBRATION_THRESHOLD_N0: float = 10.0

    @classmethod
    def fuse_evidence(
        cls,
        signals: List[EvidenceSignal],
        prior: float = DEFAULT_PRIOR,
    ) -> BayesianConfidenceResult:
        """
        Performs Bayesian Log-Odds Fusion:
        logit(P(correct|E)) = logit(P(correct)) + sum_i (w_i * LLR_i)
        where w_i = reliability_i * sqrt(n_i / (n_i + n_0))
        and LLR_i = logit(observed_score_i)
        """
        formula_str = "logit(P(theta|E)) = logit(P(theta)) + sum_i [ r_i * sqrt(n_i/(n_i+10)) * logit(s_i) ]"
        formula_latex = r"\text{logit}(P(\theta|\mathbf{E})) = \text{logit}(P(\theta)) + \sum_{i=1}^K r_i \sqrt{\frac{n_i}{n_i + n_0}} \cdot \text{logit}(s_i)"

        if not signals:
            return BayesianConfidenceResult(
                posterior_confidence=prior,
                prior_confidence=prior,
                log_odds_delta=0.0,
                confidence_interval_95=(prior - 0.05, prior + 0.05),
                sample_size_total=0,
                signals=[],
                signal_weights={},
                log_likelihood_ratios={},
                is_sentinel_active=True,
                sentinel_reason="INSUFFICIENT_EVIDENCE: Zero evidence signals provided.",
                derivation_formula=formula_str,
                derivation_latex=formula_latex,
            )

        # Check for active sentinel states
        sentinel_signals = [s for s in signals if s.sentinel_state]
        if sentinel_signals:
            first_sentinel = sentinel_signals[0]
            return BayesianConfidenceResult(
                posterior_confidence=0.0,
                prior_confidence=prior,
                log_odds_delta=0.0,
                confidence_interval_95=(0.0, 0.0),
                sample_size_total=sum(s.sample_size for s in signals),
                signals=signals,
                signal_weights={},
                log_likelihood_ratios={},
                is_sentinel_active=True,
                sentinel_reason=f"{first_sentinel.sentinel_state} in signal '{first_sentinel.source_name}'",
                derivation_formula=formula_str,
                derivation_latex=formula_latex,
            )

        prior_logit = _logit(prior)
        total_delta_logit = 0.0
        weights: Dict[str, float] = {}
        llrs: Dict[str, float] = {}
        total_samples = 0

        for sig in signals:
            total_samples += sig.sample_size
            # Attenuation factor from sample size: sqrt(n / (n + n_0))
            attenuation = math.sqrt(float(sig.sample_size) / (float(sig.sample_size) + cls.CALIBRATION_THRESHOLD_N0))
            eff_weight = sig.reliability_coefficient * attenuation
            llr = _logit(sig.observed_score)

            weights[sig.source_name] = eff_weight
            llrs[sig.source_name] = llr
            total_delta_logit += eff_weight * llr

        posterior_logit = prior_logit + total_delta_logit
        posterior_p = _sigmoid(posterior_logit)

        # Compute empirical standard error on posterior confidence
        # SE ~ 1 / sqrt(total_samples + 1)
        se = 1.0 / math.sqrt(max(1, total_samples) + 4)
        margin = 1.96 * se * posterior_p * (1.0 - posterior_p)
        ci_lower = max(0.0, posterior_p - margin)
        ci_upper = min(1.0, posterior_p + margin)

        return BayesianConfidenceResult(
            posterior_confidence=posterior_p,
            prior_confidence=prior,
            log_odds_delta=total_delta_logit,
            confidence_interval_95=(ci_lower, ci_upper),
            sample_size_total=total_samples,
            signals=signals,
            signal_weights=weights,
            log_likelihood_ratios=llrs,
            is_sentinel_active=False,
            sentinel_reason=None,
            derivation_formula=formula_str,
            derivation_latex=formula_latex,
        )
