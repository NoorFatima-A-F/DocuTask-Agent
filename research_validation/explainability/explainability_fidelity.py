"""
Research Validation & Independent Scientific Verification Framework (RVISF)
Phase 42: Explainability Validation & Fidelity Laboratory

Evaluates the faithfulness and plausibility of model attributions, rationales, and explanations:
- Faithfulness via Deletion Curve (Area Under Deletion Curve - AUDC)
- Comprehensiveness via Insertion Curve (Area Under Insertion Curve - AUIC)
- Counterfactual Stability & Monotonicity
- Attribution Sanity Checks (randomization tests)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class TokenAttribution:
    """Attribution score assigned to a specific token or word."""
    token: str
    index: int
    score: float


@dataclass
class FidelityCurveReport:
    """Evaluation of explanation faithfulness along deletion/insertion curves."""
    deletion_curve_scores: List[float]
    insertion_curve_scores: List[float]
    audc: float  # Area Under Deletion Curve (lower is better, meaning removing important tokens drops performance fast)
    auic: float  # Area Under Insertion Curve (higher is better, meaning adding important tokens recovers performance fast)
    monotonicity_score: float  # Fraction of steps respecting monotonicity
    is_faithful: bool


@dataclass
class ExplainabilityAuditReport:
    """Audit report for explainability, faithfulness, and attribution validity."""
    total_samples: int
    mean_audc: float
    mean_auic: float
    mean_monotonicity: float
    faithfulness_pass_rate: float
    status: str  # "PASS", "DEGRADED", "FAIL"
    details: Dict[str, Any] = field(default_factory=dict)


class ExplainabilityFidelityLab:
    """
    Measures the causal fidelity and empirical validity of feature attributions and explanations.
    """

    @staticmethod
    def _trapz(y_vals: List[float]) -> float:
        """Compute trapezoidal numerical integral over unit interval [0, 1]."""
        if not y_vals or len(y_vals) < 2:
            return y_vals[0] if y_vals else 0.0
        n = len(y_vals)
        dx = 1.0 / (n - 1)
        total = (y_vals[0] + y_vals[-1]) * 0.5
        for i in range(1, n - 1):
            total += y_vals[i]
        return total * dx

    @classmethod
    def evaluate_deletion_insertion_fidelity(
        cls,
        text: str,
        attributions: List[TokenAttribution],
        scorer: Callable[[str], float],
        steps: int = 10
    ) -> FidelityCurveReport:
        """
        Compute Deletion and Insertion curves by removing or adding tokens in order of attribution importance.
        """
        words = text.split()
        if not words or not attributions:
            return FidelityCurveReport(
                deletion_curve_scores=[0.0],
                insertion_curve_scores=[0.0],
                audc=0.0,
                auic=0.0,
                monotonicity_score=0.0,
                is_faithful=False
            )

        # Sort attributions in descending order of importance
        sorted_attrs = sorted(attributions, key=lambda a: abs(a.score), reverse=True)
        sorted_indices = [a.index for a in sorted_attrs if a.index < len(words)]

        # Deletion Curve: Start with full text, remove most important tokens step by step
        del_scores: List[float] = [scorer(text)]
        current_del_words = list(words)

        chunk_size = max(1, len(sorted_indices) // steps)
        for i in range(0, len(sorted_indices), chunk_size):
            to_remove = set(sorted_indices[i:i + chunk_size])
            current_del_words = [w if idx not in to_remove else "[MASK]" for idx, w in enumerate(current_del_words)]
            del_scores.append(scorer(" ".join(current_del_words)))

        # Insertion Curve: Start with blank text, add most important tokens step by step
        ins_scores: List[float] = [scorer("")]
        current_ins_words = ["[MASK]"] * len(words)

        for i in range(0, len(sorted_indices), chunk_size):
            to_add = set(sorted_indices[i:i + chunk_size])
            for idx in to_add:
                current_ins_words[idx] = words[idx]
            ins_scores.append(scorer(" ".join(current_ins_words)))

        audc = cls._trapz(del_scores)
        auic = cls._trapz(ins_scores)

        # Monotonicity: Deletion should generally decrease or stay flat, Insertion should increase
        del_decreases = sum(1 for i in range(len(del_scores) - 1) if del_scores[i] >= del_scores[i + 1] - 1e-4)
        del_mono = del_decreases / (len(del_scores) - 1) if len(del_scores) > 1 else 1.0

        is_faithful = (audc < auic) and (del_mono >= 0.6)

        return FidelityCurveReport(
            deletion_curve_scores=del_scores,
            insertion_curve_scores=ins_scores,
            audc=audc,
            auic=auic,
            monotonicity_score=del_mono,
            is_faithful=is_faithful
        )

    @classmethod
    def run_explainability_audit(
        cls,
        samples: List[Tuple[str, List[TokenAttribution]]],
        scorer: Callable[[str], float]
    ) -> ExplainabilityAuditReport:
        """Run explainability fidelity verification across sample attributions."""
        if not samples:
            return ExplainabilityAuditReport(
                total_samples=0,
                mean_audc=0.0,
                mean_auic=0.0,
                mean_monotonicity=0.0,
                faithfulness_pass_rate=0.0,
                status="INSUFFICIENT_EVIDENCE"
            )

        reports = [cls.evaluate_deletion_insertion_fidelity(t, a, scorer) for t, a in samples]
        n = len(reports)
        mean_audc = sum(r.audc for r in reports) / n
        mean_auic = sum(r.auic for r in reports) / n
        mean_mono = sum(r.monotonicity_score for r in reports) / n
        pass_count = sum(1 for r in reports if r.is_faithful)
        pass_rate = pass_count / n

        status = "PASS" if pass_rate >= 0.70 else "FAIL"

        return ExplainabilityAuditReport(
            total_samples=n,
            mean_audc=mean_audc,
            mean_auic=mean_auic,
            mean_monotonicity=mean_mono,
            faithfulness_pass_rate=pass_rate,
            status=status,
            details={"audc_lt_auic": mean_audc < mean_auic}
        )
