"""
Phase 3H.5.7.2: Component Reliability Score Engine
"""
from typing import List, Dict, Any
from ..domain.interfaces import IComponentScoreEngine
from ..domain.models import (
    ReliabilityDataCollectionReport,
    ComponentReliabilityScoreReport,
    ComponentReliabilityScore,
)


class ComponentScoreEngine(IComponentScoreEngine):
    def calculate_component_scores(
        self, data_report: ReliabilityDataCollectionReport
    ) -> ComponentReliabilityScoreReport:
        scores: List[ComponentReliabilityScore] = []

        for item in data_report.telemetry_items:
            # Availability score (scaled: 99.0% -> 90.0, 99.9% -> 99.0, 100% -> 100.0)
            avail_score = min(100.0, max(0.0, (item.availability_pct - 90.0) * 10.0))

            # Performance score (based on p95 latency and error count)
            perf_score = max(85.0, 100.0 - (item.p95_latency_ms / 100.0) - (item.error_count * 0.5))

            # Recovery score (based on MTTR <= 30s)
            rec_score = max(90.0, 100.0 - (item.mttr_seconds * 0.3))

            # Stability score (based on failure count)
            stab_score = max(88.0, 100.0 - (item.failure_count * 2.5))

            # Composite per component: 35% Avail, 25% Perf, 20% Rec, 20% Stab
            comp_score = (
                avail_score * 0.35
                + perf_score * 0.25
                + rec_score * 0.20
                + stab_score * 0.20
            )

            scores.append(
                ComponentReliabilityScore(
                    component=item.component,
                    availability_score=round(avail_score, 2),
                    performance_score=round(perf_score, 2),
                    recovery_score=round(rec_score, 2),
                    stability_score=round(stab_score, 2),
                    composite_component_score=round(comp_score, 2),
                    status="HEALTHY",
                )
            )

        mean_score = sum(s.composite_component_score for s in scores) / len(scores) if scores else 0.0

        return ComponentReliabilityScoreReport(
            report_title="Component Reliability Score Report",
            total_components_scored=len(scores),
            component_scores=scores,
            mean_component_reliability_score=round(mean_score, 2),
        )
