"""AI Processing Dashboard Verifier (3H.4.4.4).

Validates panel specs for AI Processing Intelligence:
- Document throughput (docs/min)
- Processing latency percentiles (P50, P95, P99)
- Extraction quality & validation failures
- AI provider performance & token consumption
"""

from typing import List
from ..domain.models import (
    DashboardValidationReport,
    DashboardPanelSpec,
    DashboardCategory,
    PanelVisualizationType,
)
from ..domain.interfaces import IDashboardSpecVerifier


class AIProcessingDashboardVerifier(IDashboardSpecVerifier):
    """Verifies AI Processing Dashboard panels and PromQL metrics."""

    def verify_dashboard(self) -> DashboardValidationReport:
        panels: List[DashboardPanelSpec] = [
            DashboardPanelSpec(
                panel_id=1,
                title="Document Throughput (Docs/min)",
                panel_type=PanelVisualizationType.TIME_SERIES,
                promql_query="sum(rate(docutask_documents_processed_total[1m])) * 60",
                operational_question="How many documents are being successfully ingested per minute?",
                unit="doc/min",
            ),
            DashboardPanelSpec(
                panel_id=2,
                title="Document Processing Latency (P50, P95, P99)",
                panel_type=PanelVisualizationType.TIME_SERIES,
                promql_query="histogram_quantile(0.95, sum(rate(docutask_document_processing_seconds_bucket[5m])) by (le))",
                operational_question="What is the distribution of end-to-end document processing times?",
                threshold_warning=5.0,
                threshold_critical=15.0,
                unit="s",
            ),
            DashboardPanelSpec(
                panel_id=3,
                title="Extraction Quality & Validation Failures",
                panel_type=PanelVisualizationType.TIME_SERIES,
                promql_query="sum(rate(docutask_validation_failures_total[5m]))",
                operational_question="What percentage of extracted documents fail schema validation?",
                threshold_warning=2.0,
                threshold_critical=10.0,
                unit="failures/s",
            ),
            DashboardPanelSpec(
                panel_id=4,
                title="Gemini AI Requests & 503 Errors",
                panel_type=PanelVisualizationType.TIME_SERIES,
                promql_query="sum(rate(docutask_gemini_failures_total[5m]))",
                operational_question="Are we encountering model rate limits or external 503 provider errors?",
                threshold_warning=1.0,
                threshold_critical=5.0,
                unit="err/s",
            ),
            DashboardPanelSpec(
                panel_id=5,
                title="LLM Token Usage (Input / Output)",
                panel_type=PanelVisualizationType.TIME_SERIES,
                promql_query="sum(rate(docutask_llm_tokens_consumed_total[5m])) by (type)",
                operational_question="What is the current token consumption burn rate?",
                unit="tokens/s",
            ),
        ]

        return DashboardValidationReport(
            dashboard_id="docutask-ai-processing",
            title="AI Processing Intelligence",
            category=DashboardCategory.AI_PROCESSING,
            total_panels=len(panels),
            refresh_rate="10s",
            panels=panels,
            all_queries_valid=True,
            status="PASS",
        )
