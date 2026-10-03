"""
Independent Evaluation Metrics for Black-Box System Assessment.
Zero internal dependencies. Computes accuracy, precision, recall, F1, Exact Match (EM),
Character Error Rate (CER), and Word Error Rate (WER) via Levenshtein edit distance.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class EvaluationMetricSummary:
    """Summary of black-box evaluation metrics."""

    total_samples: int
    exact_match_ratio: float
    precision: float
    recall: float
    f1_score: float
    mean_cer: float  # Character Error Rate
    mean_wer: float  # Word Error Rate
    field_accuracies: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_samples": self.total_samples,
            "exact_match_ratio": round(self.exact_match_ratio, 4),
            "precision": round(self.precision, 4),
            "recall": round(self.recall, 4),
            "f1_score": round(self.f1_score, 4),
            "mean_cer": round(self.mean_cer, 4),
            "mean_wer": round(self.mean_wer, 4),
            "field_accuracies": {k: round(v, 4) for k, v in self.field_accuracies.items()},
        }


class EvaluationMetrics:
    """Computes exact string and structured metrics for document intelligence and agent reasoning."""

    @classmethod
    def compute_levenshtein_distance(cls, s1: str, s2: str) -> int:
        """Dynamic programming Levenshtein edit distance."""
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

        return dp[m][n]

    @classmethod
    def compute_cer(cls, reference: str, hypothesis: str) -> float:
        """Character Error Rate = Levenshtein(ref, hyp) / max(1, len(ref))."""
        if not reference:
            return 0.0 if not hypothesis else 1.0
        dist = cls.compute_levenshtein_distance(reference, hypothesis)
        return dist / len(reference)

    @classmethod
    def compute_wer(cls, reference: str, hypothesis: str) -> float:
        """Word Error Rate over whitespace-tokenized words."""
        ref_words = reference.strip().split()
        hyp_words = hypothesis.strip().split()
        if not ref_words:
            return 0.0 if not hyp_words else 1.0

        # Word-level edit distance
        m, n = len(ref_words), len(hyp_words)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if ref_words[i - 1] == hyp_words[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

        return dp[m][n] / len(ref_words)

    @classmethod
    def evaluate_structured_extractions(
        cls,
        ground_truth: List[Dict[str, Any]],
        predictions: List[Dict[str, Any]],
    ) -> EvaluationMetricSummary:
        """Evaluates structured key-value predictions against ground truth."""
        n = min(len(ground_truth), len(predictions))
        if n == 0:
            return EvaluationMetricSummary(
                total_samples=0,
                exact_match_ratio=0.0,
                precision=0.0,
                recall=0.0,
                f1_score=0.0,
                mean_cer=0.0,
                mean_wer=0.0,
            )

        em_count = 0
        tp, fp, fn = 0, 0, 0
        cers: List[float] = []
        wers: List[float] = []
        field_matches: Dict[str, int] = {}
        field_totals: Dict[str, int] = {}

        for i in range(n):
            gt = ground_truth[i]
            pred = predictions[i]

            # Exact match
            if gt == pred:
                em_count += 1

            # Field-level alignment
            all_keys = set(gt.keys()).union(set(pred.keys()))
            for k in all_keys:
                field_totals[k] = field_totals.get(k, 0) + 1
                v_gt = str(gt.get(k, "")).strip()
                v_pred = str(pred.get(k, "")).strip()

                if k in gt and k in pred:
                    if v_gt == v_pred:
                        tp += 1
                        field_matches[k] = field_matches.get(k, 0) + 1
                    else:
                        fp += 1
                        fn += 1
                    cers.append(cls.compute_cer(v_gt, v_pred))
                    wers.append(cls.compute_wer(v_gt, v_pred))
                elif k in gt and k not in pred:
                    fn += 1
                    cers.append(1.0)
                    wers.append(1.0)
                else:
                    fp += 1
                    cers.append(1.0)
                    wers.append(1.0)

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        field_acc = {
            k: (field_matches.get(k, 0) / field_totals[k])
            for k in field_totals
        }

        return EvaluationMetricSummary(
            total_samples=n,
            exact_match_ratio=em_count / n,
            precision=prec,
            recall=rec,
            f1_score=f1,
            mean_cer=sum(cers) / len(cers) if cers else 0.0,
            mean_wer=sum(wers) / len(wers) if wers else 0.0,
            field_accuracies=field_acc,
        )
