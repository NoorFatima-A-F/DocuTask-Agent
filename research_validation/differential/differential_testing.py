"""
Research Validation & Independent Scientific Verification Framework (RVISF)
Phase 46: Differential Testing Framework

Executes differential cross-model and cross-engine comparative testing across:
- Gemini 1.5 Pro / Flash
- GPT-4o
- Claude 3.5 Sonnet
- Internal Deterministic Rule Parsers
Quantifies consensus rates, divergence categories, and semantic disagreements.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


class DivergenceType(str, Enum):
    NONE = "NONE"
    FORMATTING = "FORMATTING"
    NUMERICAL_PRECISION = "NUMERICAL_PRECISION"
    SEMANTIC_DISAGREEMENT = "SEMANTIC_DISAGREEMENT"
    OMISSION = "OMISSION"
    HALLUCINATION = "HALLUCINATION"


@dataclass
class DifferentialSampleResult:
    """Comparison of outputs for a single test input across multiple engines."""
    sample_id: str
    engine_outputs: Dict[str, str]  # {engine_name: output_str}
    consensus_reached: bool
    majority_output: str
    divergence_type: DivergenceType
    inter_engine_agreement_ratio: float


@dataclass
class DifferentialTestingReport:
    """Comprehensive differential cross-model comparison report."""
    total_samples_evaluated: int
    engines_participating: List[str]
    overall_consensus_rate: float
    mean_pairwise_agreement: float
    divergence_breakdown: Dict[str, int]
    disputed_samples_count: int
    status: str  # "PASS", "MODERATE_DIVERGENCE", "HIGH_DISAGREEMENT"
    details: Dict[str, Any] = field(default_factory=dict)


class DifferentialTestingEngine:
    """
    Evaluates multi-model differential testing without runtime dependencies.
    """

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Strip whitespace and lower text for robust consensus matching."""
        return " ".join(text.strip().lower().split())

    @classmethod
    def evaluate_sample(cls, sample_id: str, outputs: Dict[str, str]) -> DifferentialSampleResult:
        """Evaluate a single input across all engine responses."""
        if not outputs:
            return DifferentialSampleResult(
                sample_id=sample_id,
                engine_outputs={},
                consensus_reached=False,
                majority_output="",
                divergence_type=DivergenceType.OMISSION,
                inter_engine_agreement_ratio=0.0
            )

        norm_outputs = {k: cls._normalize_text(v) for k, v in outputs.items()}
        # Count frequency of each normalized output
        freq: Dict[str, int] = {}
        for text in norm_outputs.values():
            freq[text] = freq.get(text, 0) + 1

        total_engines = len(outputs)
        best_text, best_count = max(freq.items(), key=lambda x: x[1])

        agreement_ratio = best_count / total_engines
        consensus = agreement_ratio >= 0.66

        # Classify divergence type if disagreement exists
        if agreement_ratio == 1.0:
            div_type = DivergenceType.NONE
        elif any(len(v) == 0 for v in norm_outputs.values()):
            div_type = DivergenceType.OMISSION
        elif any(any(c.isdigit() for c in v) for v in norm_outputs.values()):
            div_type = DivergenceType.NUMERICAL_PRECISION
        else:
            div_type = DivergenceType.SEMANTIC_DISAGREEMENT

        return DifferentialSampleResult(
            sample_id=sample_id,
            engine_outputs=outputs,
            consensus_reached=consensus,
            majority_output=best_text,
            divergence_type=div_type,
            inter_engine_agreement_ratio=agreement_ratio
        )

    @classmethod
    def run_differential_campaign(
        cls,
        dataset: List[Tuple[str, Dict[str, str]]],
        consensus_threshold: float = 0.85
    ) -> DifferentialTestingReport:
        """
        Run differential campaign on a dataset of (sample_id, {engine_name: output}).
        """
        if not dataset:
            return DifferentialTestingReport(
                total_samples_evaluated=0,
                engines_participating=[],
                overall_consensus_rate=0.0,
                mean_pairwise_agreement=0.0,
                divergence_breakdown={},
                disputed_samples_count=0,
                status="INSUFFICIENT_EVIDENCE"
            )

        sample_results = [cls.evaluate_sample(s_id, outs) for s_id, outs in dataset]
        engines = list(set().union(*(outs.keys() for _, outs in dataset)))

        total_samples = len(sample_results)
        consensus_count = sum(1 for r in sample_results if r.consensus_reached)
        consensus_rate = consensus_count / total_samples

        mean_agreement = sum(r.inter_engine_agreement_ratio for r in sample_results) / total_samples

        div_breakdown: Dict[str, int] = {}
        for r in sample_results:
            div_breakdown[r.divergence_type.value] = div_breakdown.get(r.divergence_type.value, 0) + 1

        disputed_count = sum(1 for r in sample_results if not r.consensus_reached)

        status = "PASS" if consensus_rate >= consensus_threshold else "MODERATE_DIVERGENCE" if consensus_rate >= 0.70 else "HIGH_DISAGREEMENT"

        return DifferentialTestingReport(
            total_samples_evaluated=total_samples,
            engines_participating=engines,
            overall_consensus_rate=consensus_rate,
            mean_pairwise_agreement=mean_agreement,
            divergence_breakdown=div_breakdown,
            disputed_samples_count=disputed_count,
            status=status,
            details={"samples": [r.sample_id for r in sample_results if not r.consensus_reached]}
        )
