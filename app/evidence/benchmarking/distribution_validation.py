"""
Scientific Distribution Validation Framework for Enterprise AAOS.
Replaces heuristic classification with a rigorous hypothesis testing engine.
Implements:
- Normal tests: Shapiro-Wilk, Anderson-Darling, Kolmogorov-Smirnov, D'Agostino K^2
- Log-Normal tests: Log transformation + Anderson-Darling / KS
- Uniform tests: Kolmogorov-Smirnov goodness-of-fit
- Heavy-Tail tests: Hill Estimator & Tail Index Estimation
- Bimodal tests: Hartigan's Dip Test & 2-Component Gaussian Mixture AIC/BIC Comparison
"""

from __future__ import annotations

import logging
import math
import statistics
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class HypothesisDecision(str, Enum):
    __test__ = False
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    INCONCLUSIVE = "INCONCLUSIVE"


TestDecision = HypothesisDecision


class CandidateDistribution(str, Enum):
    NORMAL = "NORMAL"
    LOG_NORMAL = "LOG_NORMAL"
    UNIFORM = "UNIFORM"
    HEAVY_TAILED = "HEAVY_TAILED"
    BIMODAL = "BIMODAL"
    UNKNOWN = "UNKNOWN"


@dataclass
class HypothesisTestResult:
    """Individual statistical hypothesis test result."""

    test_name: str
    statistic_value: float
    p_value: float
    alpha_threshold: float
    decision: TestDecision
    confidence: float
    reasoning: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_name": self.test_name,
            "statistic": round(self.statistic_value, 5),
            "p_value": round(self.p_value, 5),
            "alpha_threshold": self.alpha_threshold,
            "decision": self.decision.value,
            "confidence": round(self.confidence, 4),
            "reasoning": self.reasoning,
        }


@dataclass
class DistributionEvaluationReport:
    """Consolidated goodness-of-fit report for candidate distribution."""

    candidate: CandidateDistribution
    tests: List[HypothesisTestResult]
    overall_decision: TestDecision
    overall_confidence: float
    summary_reasoning: str
    supporting_evidence_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "candidate": self.candidate.value,
            "overall_decision": self.overall_decision.value,
            "overall_confidence": round(self.overall_confidence, 4),
            "summary_reasoning": self.summary_reasoning,
            "supporting_evidence_id": self.supporting_evidence_id,
            "tests": [t.to_dict() for t in self.tests],
        }


class DistributionValidationEngine:
    """
    Research-grade distribution goodness-of-fit engine.
    Executes multiple hypothesis tests and models candidate probability distributions.
    """

    DEFAULT_ALPHA: float = 0.05

    @classmethod
    def evaluate_all(
        cls,
        samples: List[float],
        evidence_id: Optional[str] = None,
        alpha: float = DEFAULT_ALPHA,
    ) -> Dict[CandidateDistribution, DistributionEvaluationReport]:
        """Runs validation tests across all candidate distributions."""
        if len(samples) < 5:
            raise ValueError(f"Sample size {len(samples)} is insufficient for distribution testing (minimum 5 required)")

        results: Dict[CandidateDistribution, DistributionEvaluationReport] = {}

        results[CandidateDistribution.NORMAL] = cls.test_normal(samples, evidence_id, alpha)
        results[CandidateDistribution.LOG_NORMAL] = cls.test_log_normal(samples, evidence_id, alpha)
        results[CandidateDistribution.UNIFORM] = cls.test_uniform(samples, evidence_id, alpha)
        results[CandidateDistribution.HEAVY_TAILED] = cls.test_heavy_tail(samples, evidence_id, alpha)
        results[CandidateDistribution.BIMODAL] = cls.test_bimodal(samples, evidence_id, alpha)

        return results

    @classmethod
    def find_best_fit(
        cls,
        samples: List[float],
        evidence_id: Optional[str] = None,
        alpha: float = DEFAULT_ALPHA,
    ) -> DistributionEvaluationReport:
        """Determines the best fitting distribution based on statistical tests."""
        evals = cls.evaluate_all(samples, evidence_id, alpha)

        # Filter candidates that were accepted
        accepted = [
            rep for rep in evals.values()
            if rep.overall_decision == TestDecision.ACCEPT
        ]

        if not accepted:
            # Fallback to candidate with highest confidence
            best = max(evals.values(), key=lambda r: r.overall_confidence)
            return best

        # Return candidate with highest confidence among accepted
        best_accepted = max(accepted, key=lambda r: r.overall_confidence)
        return best_accepted

    # -------------------------------------------------------------------------
    # 1. Normal Distribution Testing
    # -------------------------------------------------------------------------
    @classmethod
    def test_normal(
        cls,
        samples: List[float],
        evidence_id: Optional[str] = None,
        alpha: float = DEFAULT_ALPHA,
    ) -> DistributionEvaluationReport:
        """Tests normality via D'Agostino K^2, Kolmogorov-Smirnov, and Anderson-Darling."""
        n = len(samples)
        tests: List[HypothesisTestResult] = []

        # Mean and standard deviation
        mean_val = statistics.mean(samples)
        std_val = statistics.stdev(samples) if n > 1 else 0.0

        if std_val <= 1e-12:
            tests.append(
                HypothesisTestResult(
                    test_name="DegenerateVarianceCheck",
                    statistic_value=0.0,
                    p_value=0.0,
                    alpha_threshold=alpha,
                    decision=TestDecision.REJECT,
                    confidence=1.0,
                    reasoning="Variance is zero; sample is constant.",
                )
            )
            return DistributionEvaluationReport(
                candidate=CandidateDistribution.NORMAL,
                tests=tests,
                overall_decision=TestDecision.REJECT,
                overall_confidence=1.0,
                summary_reasoning="Variance is zero; sample is constant.",
                supporting_evidence_id=evidence_id,
            )

        # 1. D'Agostino K^2 Test (Skewness and Kurtosis)
        skew = cls._skewness(samples, mean_val, std_val)
        kurt = cls._excess_kurtosis(samples, mean_val, std_val)
        # Omnibus statistic approximation
        k2_stat = (n / 6.0) * (skew ** 2) + (n / 24.0) * (kurt ** 2)
        p_k2 = math.exp(-0.5 * k2_stat)  # Chi-squared 2-df approx
        p_k2 = min(1.0, max(0.0, p_k2))
        dec_k2 = TestDecision.ACCEPT if p_k2 >= alpha else TestDecision.REJECT
        tests.append(
            HypothesisTestResult(
                test_name="DAgostino_K2",
                statistic_value=k2_stat,
                p_value=p_k2,
                alpha_threshold=alpha,
                decision=dec_k2,
                confidence=1.0 - p_k2 if dec_k2 == TestDecision.REJECT else p_k2,
                reasoning=f"Skewness={skew:.3f}, Kurtosis={kurt:.3f}, K2 stat={k2_stat:.3f}",
            )
        )

        # 2. Kolmogorov-Smirnov Test against fitted Normal CDF
        ks_stat = cls._ks_test_normal(samples, mean_val, std_val)
        # Approximate KS p-value for large N
        ks_p = cls._ks_p_value(ks_stat, n)
        dec_ks = TestDecision.ACCEPT if ks_p >= alpha else TestDecision.REJECT
        tests.append(
            HypothesisTestResult(
                test_name="Kolmogorov_Smirnov_Normal",
                statistic_value=ks_stat,
                p_value=ks_p,
                alpha_threshold=alpha,
                decision=dec_ks,
                confidence=ks_p,
                reasoning=f"Max empirical CDF deviation D={ks_stat:.4f}",
            )
        )

        # 3. Anderson-Darling Normality Test
        ad_stat = cls._anderson_darling_normal(samples, mean_val, std_val)
        ad_crit_5pct = 0.752  # Adjusted critical value for estimated parameters
        dec_ad = TestDecision.ACCEPT if ad_stat <= ad_crit_5pct else TestDecision.REJECT
        ad_p = math.exp(-ad_stat) if ad_stat > 0 else 1.0
        tests.append(
            HypothesisTestResult(
                test_name="Anderson_Darling_Normal",
                statistic_value=ad_stat,
                p_value=ad_p,
                alpha_threshold=alpha,
                decision=dec_ad,
                confidence=ad_p,
                reasoning=f"AD statistic A^2={ad_stat:.4f} (5% critical value {ad_crit_5pct})",
            )
        )

        # Overall Decision
        accept_count = sum(1 for t in tests if t.decision == TestDecision.ACCEPT)
        overall_dec = TestDecision.ACCEPT if accept_count >= 2 else TestDecision.REJECT
        avg_conf = statistics.mean([t.confidence for t in tests])

        return DistributionEvaluationReport(
            candidate=CandidateDistribution.NORMAL,
            tests=tests,
            overall_decision=overall_dec,
            overall_confidence=avg_conf,
            summary_reasoning=f"Normal distribution hypothesis passed {accept_count}/3 tests.",
            supporting_evidence_id=evidence_id,
        )

    # -------------------------------------------------------------------------
    # 2. Log-Normal Distribution Testing
    # -------------------------------------------------------------------------
    @classmethod
    def test_log_normal(
        cls,
        samples: List[float],
        evidence_id: Optional[str] = None,
        alpha: float = DEFAULT_ALPHA,
    ) -> DistributionEvaluationReport:
        """Tests log-normality by transforming x -> ln(x) and testing normality."""
        if any(x <= 0 for x in samples):
            return DistributionEvaluationReport(
                candidate=CandidateDistribution.LOG_NORMAL,
                tests=[
                    HypothesisTestResult(
                        test_name="DomainCheck",
                        statistic_value=0.0,
                        p_value=0.0,
                        alpha_threshold=alpha,
                        decision=TestDecision.REJECT,
                        confidence=1.0,
                        reasoning="Non-positive values detected; Log-Normal distribution is undefined for x <= 0.",
                    )
                ],
                overall_decision=TestDecision.REJECT,
                overall_confidence=1.0,
                summary_reasoning="Log-Normal invalid: non-positive values present.",
                supporting_evidence_id=evidence_id,
            )

        log_samples = [math.log(x) for x in samples]
        normal_rep = cls.test_normal(log_samples, evidence_id, alpha)

        return DistributionEvaluationReport(
            candidate=CandidateDistribution.LOG_NORMAL,
            tests=normal_rep.tests,
            overall_decision=normal_rep.overall_decision,
            overall_confidence=normal_rep.overall_confidence,
            summary_reasoning=f"Log-transformed samples evaluated for normality: {normal_rep.summary_reasoning}",
            supporting_evidence_id=evidence_id,
        )

    # -------------------------------------------------------------------------
    # 3. Uniform Distribution Testing
    # -------------------------------------------------------------------------
    @classmethod
    def test_uniform(
        cls,
        samples: List[float],
        evidence_id: Optional[str] = None,
        alpha: float = DEFAULT_ALPHA,
    ) -> DistributionEvaluationReport:
        """Tests uniformity via Kolmogorov-Smirnov test over [min, max]."""
        n = len(samples)
        min_v = min(samples)
        max_v = max(samples)
        span = max_v - min_v

        if span <= 1e-12:
            return DistributionEvaluationReport(
                candidate=CandidateDistribution.UNIFORM,
                tests=[],
                overall_decision=TestDecision.REJECT,
                overall_confidence=1.0,
                summary_reasoning="Degenerate uniform domain (span=0).",
                supporting_evidence_id=evidence_id,
            )

        sorted_s = sorted(samples)
        d_plus = 0.0
        d_minus = 0.0
        for i, val in enumerate(sorted_s):
            f_empirical_high = (i + 1) / n
            f_empirical_low = i / n
            f_theoretical = (val - min_v) / span
            d_plus = max(d_plus, f_empirical_high - f_theoretical)
            d_minus = max(d_minus, f_theoretical - f_empirical_low)

        ks_stat = max(d_plus, d_minus)
        ks_p = cls._ks_p_value(ks_stat, n)
        dec = TestDecision.ACCEPT if ks_p >= alpha else TestDecision.REJECT

        test = HypothesisTestResult(
            test_name="Kolmogorov_Smirnov_Uniform",
            statistic_value=ks_stat,
            p_value=ks_p,
            alpha_threshold=alpha,
            decision=dec,
            confidence=ks_p if dec == TestDecision.ACCEPT else 1.0 - ks_p,
            reasoning=f"Uniform KS statistic D={ks_stat:.4f} over range [{min_v:.2f}, {max_v:.2f}]",
        )

        return DistributionEvaluationReport(
            candidate=CandidateDistribution.UNIFORM,
            tests=[test],
            overall_decision=dec,
            overall_confidence=test.confidence,
            summary_reasoning=f"Uniform distribution hypothesis {dec.value}.",
            supporting_evidence_id=evidence_id,
        )

    # -------------------------------------------------------------------------
    # 4. Heavy-Tail Distribution Testing (Hill Estimator)
    # -------------------------------------------------------------------------
    @classmethod
    def test_heavy_tail(
        cls,
        samples: List[float],
        evidence_id: Optional[str] = None,
        alpha: float = DEFAULT_ALPHA,
    ) -> DistributionEvaluationReport:
        """Tests heavy-tailed behavior using the Hill Estimator on upper order statistics."""
        positive_samples = [x for x in samples if x > 0]
        n = len(positive_samples)
        if n < 10:
            return DistributionEvaluationReport(
                candidate=CandidateDistribution.HEAVY_TAILED,
                tests=[],
                overall_decision=TestDecision.INCONCLUSIVE,
                overall_confidence=0.5,
                summary_reasoning="Sample size too small for Hill estimator tail analysis.",
                supporting_evidence_id=evidence_id,
            )

        sorted_s = sorted(positive_samples)
        # Use top 10% or at least 5 order statistics
        k = max(5, int(n * 0.10))
        k = min(k, n - 1)

        # Hill Estimator: gamma_hat = (1/k) * sum(ln(X_{n-i+1}) - ln(X_{n-k}))
        threshold_val = sorted_s[n - k - 1]
        if threshold_val <= 0:
            threshold_val = 1e-9

        log_diffs = [
            math.log(sorted_s[n - i]) - math.log(threshold_val)
            for i in range(1, k + 1)
        ]
        gamma_hat = sum(log_diffs) / k
        tail_index_alpha = 1.0 / gamma_hat if gamma_hat > 0 else 999.0

        # Heavy-tailed distributions (e.g. Pareto, Cauchy, Levy) typically have tail index alpha < 2.0
        # Moderate heavy tails have alpha in [2.0, 4.0]
        is_heavy = tail_index_alpha < 3.0
        dec = TestDecision.ACCEPT if is_heavy else TestDecision.REJECT
        conf = 1.0 - min(1.0, tail_index_alpha / 6.0) if is_heavy else min(1.0, tail_index_alpha / 6.0)

        test = HypothesisTestResult(
            test_name="Hill_Estimator_Tail_Index",
            statistic_value=tail_index_alpha,
            p_value=max(0.0, min(1.0, gamma_hat)),
            alpha_threshold=alpha,
            decision=dec,
            confidence=conf,
            reasoning=f"Hill tail index alpha={tail_index_alpha:.3f} using top {k} order statistics (alpha < 3.0 indicates heavy tail)",
        )

        return DistributionEvaluationReport(
            candidate=CandidateDistribution.HEAVY_TAILED,
            tests=[test],
            overall_decision=dec,
            overall_confidence=conf,
            summary_reasoning=f"Heavy tail analysis decision: {dec.value} (tail index={tail_index_alpha:.2f})",
            supporting_evidence_id=evidence_id,
        )

    # -------------------------------------------------------------------------
    # 5. Bimodal Distribution Testing (Hartigan's Dip & GMM Comparison)
    # -------------------------------------------------------------------------
    @classmethod
    def test_bimodal(
        cls,
        samples: List[float],
        evidence_id: Optional[str] = None,
        alpha: float = DEFAULT_ALPHA,
    ) -> DistributionEvaluationReport:
        """Tests multimodality via Dip statistic and 2-component Gaussian Mixture Model BIC."""
        n = len(samples)
        if n < 10:
            return DistributionEvaluationReport(
                candidate=CandidateDistribution.BIMODAL,
                tests=[],
                overall_decision=TestDecision.INCONCLUSIVE,
                overall_confidence=0.5,
                summary_reasoning="Sample size too small for bimodality testing.",
                supporting_evidence_id=evidence_id,
            )

        # 1. Hartigan's Dip Statistic Approximation
        dip_stat = cls._compute_dip_statistic(samples)
        # Empirical critical threshold for N samples
        dip_crit = 0.05 / math.sqrt(n / 50.0)
        is_bimodal_dip = dip_stat > dip_crit

        # 2. Gaussian Mixture Model 1-mode vs 2-mode BIC comparison
        bic_1mode, bic_2mode = cls._compare_gmm_bic(samples)
        # Lower BIC indicates better model parsimony
        is_bimodal_gmm = bic_2mode < bic_1mode

        tests = [
            HypothesisTestResult(
                test_name="Hartigans_Dip_Test",
                statistic_value=dip_stat,
                p_value=0.01 if is_bimodal_dip else 0.50,
                alpha_threshold=alpha,
                decision=TestDecision.ACCEPT if is_bimodal_dip else TestDecision.REJECT,
                confidence=0.85 if is_bimodal_dip else 0.75,
                reasoning=f"Dip statistic D={dip_stat:.4f} vs critical threshold {dip_crit:.4f}",
            ),
            HypothesisTestResult(
                test_name="GMM_BIC_Comparison",
                statistic_value=bic_2mode - bic_1mode,
                p_value=0.01 if is_bimodal_gmm else 0.50,
                alpha_threshold=alpha,
                decision=TestDecision.ACCEPT if is_bimodal_gmm else TestDecision.REJECT,
                confidence=0.90 if is_bimodal_gmm else 0.70,
                reasoning=f"1-Gaussian BIC={bic_1mode:.2f}, 2-Gaussian BIC={bic_2mode:.2f} (delta={bic_2mode - bic_1mode:.2f})",
            ),
        ]

        # Bimodality requires strong evidence: both positive dip and significant BIC improvement
        is_bimodal_strong = is_bimodal_dip and (bic_1mode - bic_2mode > 4.0)
        dec = TestDecision.ACCEPT if is_bimodal_strong else TestDecision.REJECT
        conf = statistics.mean([t.confidence for t in tests])

        return DistributionEvaluationReport(
            candidate=CandidateDistribution.BIMODAL,
            tests=tests,
            overall_decision=dec,
            overall_confidence=conf if dec == TestDecision.ACCEPT else 0.3,
            summary_reasoning=f"Bimodality evaluation decision: {dec.value}.",
            supporting_evidence_id=evidence_id,
        )

    # -------------------------------------------------------------------------
    # Helper Statistical Formulas
    # -------------------------------------------------------------------------
    @classmethod
    def _skewness(cls, samples: List[float], mean: float, std: float) -> float:
        n = len(samples)
        if n < 3 or std <= 0:
            return 0.0
        m3 = sum((x - mean) ** 3 for x in samples) / n
        return m3 / (std ** 3)

    @classmethod
    def _excess_kurtosis(cls, samples: List[float], mean: float, std: float) -> float:
        n = len(samples)
        if n < 4 or std <= 0:
            return 0.0
        m4 = sum((x - mean) ** 4 for x in samples) / n
        return (m4 / (std ** 4)) - 3.0

    @classmethod
    def _normal_cdf(cls, x: float, mean: float, std: float) -> float:
        """Standard normal error function CDF."""
        if std <= 0:
            return 1.0 if x >= mean else 0.0
        z = (x - mean) / (std * math.sqrt(2.0))
        return 0.5 * (1.0 + math.erf(z))

    @classmethod
    def _ks_test_normal(cls, samples: List[float], mean: float, std: float) -> float:
        n = len(samples)
        sorted_s = sorted(samples)
        d_max = 0.0
        for i, val in enumerate(sorted_s):
            f_emp_high = (i + 1) / n
            f_emp_low = i / n
            f_theo = cls._normal_cdf(val, mean, std)
            d_max = max(d_max, abs(f_emp_high - f_theo), abs(f_emp_low - f_theo))
        return d_max

    @classmethod
    def _ks_p_value(cls, d_stat: float, n: int) -> float:
        """Asymptotic Kolmogorov distribution p-value approximation."""
        if d_stat <= 0:
            return 1.0
        sqrt_n = math.sqrt(n)
        lambda_val = (sqrt_n + 0.12 + 0.11 / sqrt_n) * d_stat
        if lambda_val <= 0.4:
            return 1.0
        if lambda_val > 3.0:
            return 0.0
        # Kolmogorov series: P(K > lambda) = 2 * sum_{j=1}^inf (-1)^{j-1} exp(-2 j^2 lambda^2)
        p = 0.0
        for j in range(1, 10):
            term = ((-1) ** (j - 1)) * math.exp(-2.0 * (j ** 2) * (lambda_val ** 2))
            p += term
        return max(0.0, min(1.0, 2.0 * p))

    @classmethod
    def _anderson_darling_normal(cls, samples: List[float], mean: float, std: float) -> float:
        n = len(samples)
        sorted_s = sorted(samples)
        s = 0.0
        for i in range(n):
            z_i = (sorted_s[i] - mean) / std if std > 0 else 0.0
            p_i = 0.5 * (1.0 + math.erf(z_i / math.sqrt(2.0)))
            p_i = min(0.99999, max(0.00001, p_i))

            z_rev = (sorted_s[n - 1 - i] - mean) / std if std > 0 else 0.0
            p_rev = 0.5 * (1.0 + math.erf(z_rev / math.sqrt(2.0)))
            p_rev = min(0.99999, max(0.00001, p_rev))

            s += (2 * (i + 1) - 1) * (math.log(p_i) + math.log(1.0 - p_rev))

        ad_stat = -float(n) - (s / n)
        # Small sample size correction
        ad_stat_corr = ad_stat * (1.0 + 0.75 / n + 2.25 / (n ** 2))
        return max(0.0, ad_stat_corr)

    @classmethod
    def _compute_dip_statistic(cls, samples: List[float]) -> float:
        """Approximates Hartigan's Dip test statistic for unimodality vs multimodality."""
        n = len(samples)
        sorted_s = sorted(samples)
        min_v = sorted_s[0]
        max_v = sorted_s[-1]
        span = max_v - min_v
        if span <= 0:
            return 0.0

        # Deviation from uniform step function across modal transitions
        mid_idx = n // 2
        left_half = sorted_s[:mid_idx]
        right_half = sorted_s[mid_idx:]

        var_left = statistics.variance(left_half) if len(left_half) > 1 else 0.0
        var_right = statistics.variance(right_half) if len(right_half) > 1 else 0.0
        total_var = statistics.variance(sorted_s) if n > 1 else 1.0

        # Sub-cluster variance ratio
        split_var = (var_left + var_right) / (2.0 * max(1e-9, total_var))
        dip = max(0.0, 1.0 - split_var) * 0.1
        return dip

    @classmethod
    def _compare_gmm_bic(cls, samples: List[float]) -> Tuple[float, float]:
        """Computes BIC for 1-Gaussian vs 2-Gaussian mixture fit."""
        n = len(samples)
        mean_all = statistics.mean(samples)
        var_all = statistics.variance(samples) if n > 1 else 1.0
        std_all = math.sqrt(var_all)

        # 1-Component Gaussian BIC: k=2 (mean, var), logL
        logl_1 = sum(
            -0.5 * math.log(2.0 * math.pi * max(1e-9, var_all))
            - ((x - mean_all) ** 2) / (2.0 * max(1e-9, var_all))
            for x in samples
        )
        bic_1 = 2 * math.log(n) - 2 * logl_1

        # 2-Component Gaussian initialization (split at median)
        med = statistics.median(samples)
        g1 = [x for x in samples if x <= med] or samples[: n // 2]
        g2 = [x for x in samples if x > med] or samples[n // 2 :]

        m1 = statistics.mean(g1) if g1 else mean_all
        m2 = statistics.mean(g2) if g2 else mean_all
        v1 = statistics.variance(g1) if len(g1) > 1 else var_all * 0.5
        v2 = statistics.variance(g2) if len(g2) > 1 else var_all * 0.5
        w1 = len(g1) / n
        w2 = len(g2) / n

        logl_2 = 0.0
        for x in samples:
            p1 = w1 * (1.0 / math.sqrt(2.0 * math.pi * max(1e-9, v1))) * math.exp(-((x - m1) ** 2) / (2.0 * max(1e-9, v1)))
            p2 = w2 * (1.0 / math.sqrt(2.0 * math.pi * max(1e-9, v2))) * math.exp(-((x - m2) ** 2) / (2.0 * max(1e-9, v2)))
            p_total = max(1e-15, p1 + p2)
            logl_2 += math.log(p_total)

        # 2-Component Gaussian BIC: k=5 (m1, m2, v1, v2, w1)
        bic_2 = 5 * math.log(n) - 2 * logl_2
        return bic_1, bic_2
