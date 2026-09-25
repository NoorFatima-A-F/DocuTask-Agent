"""
Hypothesis Generation Engine for Phase 10 (AISLCOP).

Discovers optimization opportunities from empirical experience patterns, failures,
and prediction errors, then formats them into rigorous testable hypotheses.
"""

from __future__ import annotations

import uuid
from typing import Dict, List, Optional

from app.runtime.intelligence.experience.experience_record import ExperienceRecord
from app.runtime.intelligence.hypothesis.hypothesis_model import (
    Hypothesis,
    HypothesisCategory,
    HypothesisStatus,
)


class HypothesisEngine:
    """
    Synthesizes and catalogs testable optimization hypotheses.
    """

    def __init__(self):
        self._hypotheses: Dict[str, Hypothesis] = {}

    def register_hypothesis(self, hypothesis: Hypothesis) -> str:
        self._hypotheses[hypothesis.hypothesis_id] = hypothesis
        return hypothesis.hypothesis_id

    def generate_from_experiences(
        self,
        experiences: List[ExperienceRecord],
        domain: Optional[str] = None,
    ) -> List[Hypothesis]:
        """
        Scans experiences to identify high-latency bottlenecks, retry hot-spots,
        or excessive costs and auto-generates testable hypotheses.
        """
        filtered = [e for e in experiences if not domain or e.document_type.lower() == domain.lower()]
        if not filtered:
            return []

        generated: List[Hypothesis] = []
        target_domain = domain or filtered[0].document_type

        # 1. Check for retry frequency bottleneck
        retries = sum(e.retries_count for e in filtered)
        if retries > 0:
            avg_retries = retries / len(filtered)
            hyp = Hypothesis(
                hypothesis_id=f"hyp_{uuid.uuid4().hex[:10]}",
                title=f"Pre-validation Invariant Check for {target_domain.title()}",
                category=HypothesisCategory.RETRY_MINIMIZATION,
                premise=f"{target_domain.title()} missions exhibit average of {avg_retries:.2f} retries due to downstream schema mismatches.",
                proposed_action="Inject pre-extraction schema invariant validation node in DAG pipeline",
                target_metric="retries_count",
                baseline_value=avg_retries,
                expected_value=max(0.0, avg_retries * 0.2),
                expected_improvement_pct=80.0,
                status=HypothesisStatus.PROPOSED,
                source_domain=target_domain,
                supporting_experience_ids=[e.experience_id for e in filtered if e.retries_count > 0][:5],
            )
            self.register_hypothesis(hyp)
            generated.append(hyp)

        # 2. Check for latency optimization
        latencies = [e.total_latency_ms for e in filtered]
        avg_latency = sum(latencies) / len(latencies)
        if avg_latency > 800.0:
            hyp = Hypothesis(
                hypothesis_id=f"hyp_{uuid.uuid4().hex[:10]}",
                title=f"Parallel Sub-DAG Fan-Out for {target_domain.title()}",
                category=HypothesisCategory.LATENCY_REDUCTION,
                premise=f"Sequential OCR and table extraction accounts for {avg_latency:.1f}ms latency.",
                proposed_action="Execute table parsing and metadata extraction concurrently in parallel DAG workers",
                target_metric="latency_ms",
                baseline_value=avg_latency,
                expected_value=avg_latency * 0.70,
                expected_improvement_pct=30.0,
                status=HypothesisStatus.PROPOSED,
                source_domain=target_domain,
                supporting_experience_ids=[e.experience_id for e in filtered][:5],
            )
            self.register_hypothesis(hyp)
            generated.append(hyp)

        # 3. Check for cost optimization
        costs = [e.total_cost_usd for e in filtered]
        avg_cost = sum(costs) / len(costs)
        if avg_cost > 0.008:
            hyp = Hypothesis(
                hypothesis_id=f"hyp_{uuid.uuid4().hex[:10]}",
                title=f"Flash-Tier Fallback Strategy for Clean {target_domain.title()} Docs",
                category=HypothesisCategory.COST_OPTIMIZATION,
                premise=f"High-quality digital {target_domain.title()} documents achieve >98% confidence on Gemini Flash.",
                proposed_action="Route documents with initial clarity score > 0.92 directly to Gemini 1.5 Flash",
                target_metric="cost_usd",
                baseline_value=avg_cost,
                expected_value=avg_cost * 0.55,
                expected_improvement_pct=45.0,
                status=HypothesisStatus.PROPOSED,
                source_domain=target_domain,
                supporting_experience_ids=[e.experience_id for e in filtered][:5],
            )
            self.register_hypothesis(hyp)
            generated.append(hyp)

        return generated

    def get(self, hypothesis_id: str) -> Optional[Hypothesis]:
        return self._hypotheses.get(hypothesis_id)

    def list_all(self, status: Optional[HypothesisStatus] = None) -> List[Hypothesis]:
        if status:
            return [h for h in self._hypotheses.values() if h.status == status]
        return list(self._hypotheses.values())

    def update_status(self, hypothesis_id: str, new_status: HypothesisStatus, p_value: Optional[float] = None) -> bool:
        hyp = self._hypotheses.get(hypothesis_id)
        if not hyp:
            return False
        hyp.status = new_status
        if p_value is not None:
            hyp.validation_p_value = p_value
        return True
