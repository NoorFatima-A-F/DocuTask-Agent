"""
Central Metric Registry for standard verification metric definitions, versioning, and explanations.
"""
from __future__ import annotations
from typing import Dict, List, Optional
from app.platform_verification.evaluation_engine.domain.models import (
    MetricDefinition,
    MetricCategory,
    MetricMetadata,
    MetricExplanation,
)
from app.platform_verification.evaluation_engine.domain.interfaces import IMetricRegistry


class MetricRegistry(IMetricRegistry):
    """Thread-safe registry of standardized verification metrics."""

    def __init__(self) -> None:
        self._registry: Dict[str, MetricDefinition] = {}
        self._explanations: Dict[str, MetricExplanation] = {}
        self._load_standard_definitions()

    def register(self, definition: MetricDefinition) -> None:
        self._registry[definition.id] = definition

    def register_explanation(self, explanation: MetricExplanation) -> None:
        self._explanations[explanation.name] = explanation

    def get(self, metric_id: str) -> MetricDefinition:
        if metric_id not in self._registry:
            raise KeyError(f"Metric '{metric_id}' is not registered in the MetricRegistry.")
        return self._registry[metric_id]

    def list_all(self) -> List[MetricDefinition]:
        return list(self._registry.values())

    def list_by_category(self, category: MetricCategory) -> List[MetricDefinition]:
        return [m for m in self._registry.values() if m.category == category]

    def get_metadata(self, metric_id: str) -> MetricMetadata:
        m = self.get(metric_id)
        return MetricMetadata(
            id=m.id,
            name=m.name,
            category=m.category.value,
            description=m.description,
            formula=m.formula,
            source=m.source,
            version=m.version,
            threshold=m.threshold,
            weight=m.weight,
            owner=m.owner,
        )

    def get_explanation(self, metric_id_or_name: str) -> MetricExplanation:
        if metric_id_or_name in self._explanations:
            return self._explanations[metric_id_or_name]
        m = self._registry.get(metric_id_or_name)
        if m and m.name in self._explanations:
            return self._explanations[m.name]
        return MetricExplanation(
            name=metric_id_or_name,
            formula=m.formula if m else "Custom Formula",
            purpose=m.description if m else "Evaluation of system performance.",
            interpretation="Higher is better." if (m and m.is_higher_better) else "Lower is better.",
            limitations="Statistical sample size requirements must be satisfied.",
        )

    def _load_standard_definitions(self) -> None:
        # PART 2 — Functional Correctness
        self.register(
            MetricDefinition(
                id="func_accuracy",
                name="Accuracy",
                category=MetricCategory.FUNCTIONAL_CORRECTNESS,
                description="Percentage of correct predictions over total predictions.",
                formula="Correct Predictions / Total Predictions",
                source="classification, extraction, routing",
                calculation_method="binary_classification_accuracy",
                threshold=95.0,
                weight=0.25,
            )
        )
        self.register_explanation(
            MetricExplanation(
                name="Accuracy",
                formula="Correct Predictions / Total Predictions",
                purpose="Evaluate correctness across classification and field extractions.",
                interpretation="Values >= 95% indicate enterprise readiness.",
                limitations="May be misleading on highly imbalanced target distributions.",
            )
        )

        self.register(
            MetricDefinition(
                id="func_precision",
                name="Precision",
                category=MetricCategory.FUNCTIONAL_CORRECTNESS,
                description="Percentage of positive predictions that were correct.",
                formula="True Positives / (True Positives + False Positives)",
                source="fraud detection, security alert verification",
                calculation_method="precision_score",
                threshold=90.0,
                weight=0.20,
            )
        )

        self.register(
            MetricDefinition(
                id="func_recall",
                name="Recall",
                category=MetricCategory.FUNCTIONAL_CORRECTNESS,
                description="Percentage of actual positives correctly detected.",
                formula="True Positives / (True Positives + False Negatives)",
                source="missing critical documents, compliance auditing",
                calculation_method="recall_score",
                threshold=90.0,
                weight=0.20,
            )
        )

        self.register(
            MetricDefinition(
                id="func_f1",
                name="F1 Score",
                category=MetricCategory.FUNCTIONAL_CORRECTNESS,
                description="Harmonic mean of precision and recall.",
                formula="2 * (Precision * Recall) / (Precision + Recall)",
                source="balanced classification evaluation",
                calculation_method="f1_score",
                threshold=92.0,
                weight=0.15,
            )
        )

        self.register(
            MetricDefinition(
                id="func_exact_match",
                name="Exact Match",
                category=MetricCategory.FUNCTIONAL_CORRECTNESS,
                description="Percentage of structured outputs matching ground truth exactly.",
                formula="Exact Match Count / Total Count",
                source="structured outputs, JSON extraction",
                calculation_method="exact_match_ratio",
                threshold=90.0,
                weight=0.10,
            )
        )

        self.register(
            MetricDefinition(
                id="func_schema_validity",
                name="Schema Validity Rate",
                category=MetricCategory.FUNCTIONAL_CORRECTNESS,
                description="Percentage of generated outputs strictly matching the required schema.",
                formula="Schema Valid Count / Total Count",
                source="JSON schema validation",
                calculation_method="schema_validation_ratio",
                threshold=99.0,
                weight=0.10,
            )
        )

        # PART 3 — AI Quality Metrics
        self.register(
            MetricDefinition(
                id="ai_grounding",
                name="Grounding Score",
                category=MetricCategory.AI_QUALITY,
                description="Measures whether generated output relies strictly on provided evidence.",
                formula="Evidence Supported Claims / Total Generated Claims",
                source="retrieval-augmented generation, document reasoning",
                calculation_method="claim_evidence_support_ratio",
                threshold=90.0,
                weight=0.20,
            )
        )

        self.register(
            MetricDefinition(
                id="ai_faithfulness",
                name="Faithfulness Score",
                category=MetricCategory.AI_QUALITY,
                description="Measures whether output faithfully represents source information without distortion.",
                formula="Faithful Facts / Total Extracted Facts",
                source="source document truth verification",
                calculation_method="fact_alignment_score",
                threshold=92.0,
                weight=0.20,
            )
        )

        self.register(
            MetricDefinition(
                id="ai_hallucination_rate",
                name="Hallucination Rate",
                category=MetricCategory.AI_QUALITY,
                description="Percentage of unsupported or fabricated claims.",
                formula="Fabricated Claims / Total Generated Claims",
                source="hallucination detection pipeline",
                calculation_method="unsupported_claims_ratio",
                threshold=5.0,
                weight=0.20,
                is_higher_better=False,
            )
        )

        self.register(
            MetricDefinition(
                id="ai_completeness",
                name="Completeness Score",
                category=MetricCategory.AI_QUALITY,
                description="Percentage of required target information included in response.",
                formula="Included Required Entities / Total Required Entities",
                source="information extraction",
                calculation_method="coverage_ratio",
                threshold=90.0,
                weight=0.15,
            )
        )

        self.register(
            MetricDefinition(
                id="ai_consistency",
                name="Consistency Score",
                category=MetricCategory.AI_QUALITY,
                description="Stability of output semantics across repeated executions.",
                formula="Semantic Similarity across N Runs",
                source="multi-run stability testing",
                calculation_method="semantic_embedding_cosine_consistency",
                threshold=88.0,
                weight=0.10,
            )
        )

        self.register(
            MetricDefinition(
                id="ai_context_utilization",
                name="Context Utilization Score",
                category=MetricCategory.AI_QUALITY,
                description="How effectively relevant retrieved context influenced the output.",
                formula="Utilized Relevant Context Chunks / Retrieved Relevant Chunks",
                source="RAG context analyzer",
                calculation_method="context_relevance_utilization",
                threshold=85.0,
                weight=0.08,
            )
        )

        self.register(
            MetricDefinition(
                id="ai_citation_accuracy",
                name="Citation Accuracy",
                category=MetricCategory.AI_QUALITY,
                description="Correctness of referenced evidence citations.",
                formula="Valid Citations / Total Citations Provided",
                source="citation auditor",
                calculation_method="citation_validation_rate",
                threshold=95.0,
                weight=0.07,
            )
        )

        # PART 4 — Performance Metrics
        self.register(
            MetricDefinition(
                id="perf_avg_latency",
                name="Average Latency",
                category=MetricCategory.PERFORMANCE,
                description="Average response time in milliseconds.",
                formula="Sum(Response Times) / Total Requests",
                source="runtime tracing",
                calculation_method="mean_duration_ms",
                threshold=1000.0,
                weight=0.15,
                is_higher_better=False,
                unit="ms",
                max_value=10000.0,
            )
        )

        self.register(
            MetricDefinition(
                id="perf_p95_latency",
                name="P95 Latency",
                category=MetricCategory.PERFORMANCE,
                description="95th percentile latency representing enterprise SLA measurement.",
                formula="95th Percentile Duration",
                source="runtime tracing",
                calculation_method="percentile_95_ms",
                threshold=2000.0,
                weight=0.25,
                is_higher_better=False,
                unit="ms",
                max_value=10000.0,
            )
        )

        self.register(
            MetricDefinition(
                id="perf_p99_latency",
                name="P99 Latency",
                category=MetricCategory.PERFORMANCE,
                description="99th percentile worst-case latency.",
                formula="99th Percentile Duration",
                source="runtime tracing",
                calculation_method="percentile_99_ms",
                threshold=3500.0,
                weight=0.20,
                is_higher_better=False,
                unit="ms",
                max_value=10000.0,
            )
        )

        self.register(
            MetricDefinition(
                id="perf_throughput_rps",
                name="Throughput RPS",
                category=MetricCategory.PERFORMANCE,
                description="Requests processed per second.",
                formula="Completed Requests / Duration (seconds)",
                source="load testing harness",
                calculation_method="requests_per_second",
                threshold=50.0,
                weight=0.20,
                is_higher_better=True,
                unit="req/sec",
                max_value=1000.0,
            )
        )

        self.register(
            MetricDefinition(
                id="perf_cost_per_doc",
                name="Cost Per Document",
                category=MetricCategory.PERFORMANCE,
                description="Total compute and token inference cost per document processed in USD.",
                formula="Total Cost / Total Documents",
                source="billing telemetry",
                calculation_method="cost_per_unit_usd",
                threshold=0.05,
                weight=0.20,
                is_higher_better=False,
                unit="USD",
                max_value=1.0,
            )
        )

        # PART 5 — Reliability Metrics
        self.register(
            MetricDefinition(
                id="rel_availability",
                name="Availability",
                category=MetricCategory.RELIABILITY,
                description="System uptime percentage.",
                formula="(Uptime / Total Time) * 100",
                source="health monitor",
                calculation_method="uptime_percentage",
                threshold=99.9,
                weight=0.30,
            )
        )

        self.register(
            MetricDefinition(
                id="rel_success_rate",
                name="Success Rate",
                category=MetricCategory.RELIABILITY,
                description="Percentage of successful verification runs.",
                formula="Successful Executions / Total Executions",
                source="execution engine",
                calculation_method="success_ratio",
                threshold=98.0,
                weight=0.30,
            )
        )

        self.register(
            MetricDefinition(
                id="rel_failure_rate",
                name="Failure Rate",
                category=MetricCategory.RELIABILITY,
                description="Percentage of failed executions due to errors or timeouts.",
                formula="Failed Executions / Total Executions",
                source="execution engine",
                calculation_method="failure_ratio",
                threshold=2.0,
                weight=0.20,
                is_higher_better=False,
            )
        )

        self.register(
            MetricDefinition(
                id="rel_recovery_success_rate",
                name="Recovery Success Rate",
                category=MetricCategory.RELIABILITY,
                description="Percentage of failures successfully recovered via self-healing or retry.",
                formula="Recovered Failures / Total Triggered Failures",
                source="chaos engineering engine",
                calculation_method="recovery_success_ratio",
                threshold=95.0,
                weight=0.20,
            )
        )

        # PART 6 — Security Metrics
        self.register(
            MetricDefinition(
                id="sec_critical_vulns",
                name="Critical Vulnerability Count",
                category=MetricCategory.SECURITY,
                description="Number of unmitigated critical security vulnerabilities.",
                formula="Count(Critical Vulnerabilities)",
                source="security scanner",
                calculation_method="integer_count",
                threshold=0.0,
                weight=0.35,
                is_higher_better=False,
                unit="count",
                max_value=10.0,
            )
        )

        self.register(
            MetricDefinition(
                id="sec_prompt_injection_resistance",
                name="Prompt Injection Resistance",
                category=MetricCategory.SECURITY,
                description="Percentage of adversarial prompt injection attacks successfully blocked.",
                formula="Blocked Attacks / Total Adversarial Attacks",
                source="security laboratory",
                calculation_method="blocked_attacks_ratio",
                threshold=98.0,
                weight=0.35,
            )
        )

        self.register(
            MetricDefinition(
                id="sec_data_leakage_rate",
                name="Data Leakage Rate",
                category=MetricCategory.SECURITY,
                description="Percentage of executions exposing sensitive or PII data.",
                formula="Leaked PII Instances / Total Evaluated Instances",
                source="privacy auditor",
                calculation_method="leakage_ratio",
                threshold=0.0,
                weight=0.30,
                is_higher_better=False,
            )
        )
