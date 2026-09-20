"""Risk Intelligence Engine for DocuTask Autonomous Planning Platform.

Evaluates 10 distinct risk vectors, computes composite risk scores, and generates automated mitigation
and fallback strategies for every candidate execution strategy.
"""

from __future__ import annotations

import uuid
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.runtime.planning.strategy_generator import CandidateStrategy


class RiskVectorType(str, Enum):
    OCR_DEGRADATION = "OCR_DEGRADATION"
    LLM_HALLUCINATION = "LLM_HALLUCINATION"
    SCHEMA_DRIFT = "SCHEMA_DRIFT"
    API_OUTAGE = "API_OUTAGE"
    WORKER_CRASH = "WORKER_CRASH"
    SLA_VIOLATION = "SLA_VIOLATION"
    BUDGET_OVERRUN = "BUDGET_OVERRUN"
    MEMORY_CORRUPTION = "MEMORY_CORRUPTION"
    SECURITY_CLEARANCE_BREACH = "SECURITY_CLEARANCE_BREACH"
    CONCURRENCY_COLLISION = "CONCURRENCY_COLLISION"


class RiskAssessment(BaseModel):
    """Evaluation of a specific risk vector."""
    risk_id: str = Field(default_factory=lambda: f"risk_{uuid.uuid4().hex[:8]}")
    vector_type: RiskVectorType
    name: str
    probability: float = Field(ge=0.0, le=1.0)
    impact: float = Field(ge=0.0, le=1.0)
    severity_score: float = Field(ge=0.0, le=1.0, description="probability * impact")
    mitigation_strategy: str
    fallback_path: str
    trigger_threshold: float = 0.5


class StrategyRiskProfile(BaseModel):
    """Comprehensive risk intelligence report for a candidate strategy."""
    strategy_id: str
    overall_risk_score: float = Field(ge=0.0, le=1.0)
    high_risk_vectors: List[RiskAssessment] = Field(default_factory=list)
    all_assessments: List[RiskAssessment] = Field(default_factory=list)
    mitigation_coverage: float = Field(default=1.0, ge=0.0, le=1.0)
    recommended_guardrails: List[str] = Field(default_factory=list)


class RiskIntelligenceEngine:
    """Simulates operational hazards and calculates mathematical risk profiles."""

    def evaluate_strategy_risk(
        self,
        strategy: CandidateStrategy,
        document_complexity: float = 1.0,
    ) -> StrategyRiskProfile:
        assessments: List[RiskAssessment] = []
        is_pro = any("pro" in s.provider or "pro" in s.capability_id for s in strategy.steps)
        is_cloud_ocr = any("cloud_vision" in s.provider for s in strategy.steps)

        # 1. OCR Degradation
        ocr_prob = 0.15 if not is_cloud_ocr else 0.02
        assessments.append(
            RiskAssessment(
                vector_type=RiskVectorType.OCR_DEGRADATION,
                name="OCR Text Degradation & Smearing",
                probability=ocr_prob * document_complexity,
                impact=0.75,
                severity_score=round(ocr_prob * document_complexity * 0.75, 4),
                mitigation_strategy="Auto-deskew, contrast normalization, and fallback to Cloud Neural Vision.",
                fallback_path="ocr_cloud_vision",
            )
        )

        # 2. LLM Hallucination
        halluc_prob = 0.08 if not is_pro else 0.01
        assessments.append(
            RiskAssessment(
                vector_type=RiskVectorType.LLM_HALLUCINATION,
                name="Out-of-Distribution Entity Hallucination",
                probability=halluc_prob * document_complexity,
                impact=0.85,
                severity_score=round(halluc_prob * document_complexity * 0.85, 4),
                mitigation_strategy="AST deterministic validation cross-check and regex bound assertion.",
                fallback_path="llm_pro_reasoner",
            )
        )

        # 3. Schema Drift
        assessments.append(
            RiskAssessment(
                vector_type=RiskVectorType.SCHEMA_DRIFT,
                name="Payload Schema Drift & Missing Keys",
                probability=0.05,
                impact=0.60,
                severity_score=0.03,
                mitigation_strategy="Pydantic strict schema coercion and default value backfill.",
                fallback_path="schema_transformer",
            )
        )

        # 4. API Outage / Rate Limit
        assessments.append(
            RiskAssessment(
                vector_type=RiskVectorType.API_OUTAGE,
                name="Upstream LLM / Vision 429 & 503 Quota Throttling",
                probability=0.03,
                impact=0.90,
                severity_score=0.027,
                mitigation_strategy="Exponential backoff with jitter and secondary provider routing.",
                fallback_path="gemini_flash_lite",
            )
        )

        # 5. Worker Crash
        assessments.append(
            RiskAssessment(
                vector_type=RiskVectorType.WORKER_CRASH,
                name="Worker Out-of-Memory / Node Eviction",
                probability=0.015,
                impact=0.95,
                severity_score=0.0142,
                mitigation_strategy="Supervised worker restart and transactional state checkpoint replay.",
                fallback_path="worker_pool_failover",
            )
        )

        # 6. SLA Violation
        sla_prob = 0.05 if strategy.estimated_critical_path_ms > 4000 else 0.01
        assessments.append(
            RiskAssessment(
                vector_type=RiskVectorType.SLA_VIOLATION,
                name="Critical Path Latency SLA Breach",
                probability=sla_prob,
                impact=0.80,
                severity_score=round(sla_prob * 0.80, 4),
                mitigation_strategy="Elastic worker scale-out and non-blocking background reflection.",
                fallback_path="alpha_fast_turbo",
            )
        )

        # 7. Budget Overrun
        budget_prob = 0.04 if strategy.estimated_total_cost_usd > 0.05 else 0.005
        assessments.append(
            RiskAssessment(
                vector_type=RiskVectorType.BUDGET_OVERRUN,
                name="Token Explosion & Budget Cap Breach",
                probability=budget_prob,
                impact=0.50,
                severity_score=round(budget_prob * 0.50, 4),
                mitigation_strategy="Streaming token counting and immediate early termination on budget limit.",
                fallback_path="gamma_cost_frugal",
            )
        )

        # 8. Memory Corruption
        assessments.append(
            RiskAssessment(
                vector_type=RiskVectorType.MEMORY_CORRUPTION,
                name="Episodic Memory Graph Lookup Failure",
                probability=0.01,
                impact=0.40,
                severity_score=0.004,
                mitigation_strategy="Local fallback cache and read-repair on vector embeddings.",
                fallback_path="in_memory_lru_cache",
            )
        )

        # 9. Security & Clearance Breach
        assessments.append(
            RiskAssessment(
                vector_type=RiskVectorType.SECURITY_CLEARANCE_BREACH,
                name="PII / PCI Cross-Tenant Exposure",
                probability=0.001,
                impact=1.0,
                severity_score=0.001,
                mitigation_strategy="Automated redact-before-forwarding and isolated worker memory namespaces.",
                fallback_path="zero_trust_redactor",
            )
        )

        # 10. Concurrency Collision
        assessments.append(
            RiskAssessment(
                vector_type=RiskVectorType.CONCURRENCY_COLLISION,
                name="Simultaneous State Mutation Lock Contention",
                probability=0.02 if strategy.concurrency_level > 8 else 0.005,
                impact=0.50,
                severity_score=0.01,
                mitigation_strategy="Optimistic concurrency control with versioned DAG timestamps.",
                fallback_path="serialized_queue",
            )
        )

        # Calculate composite weighted risk score
        total_severity = sum(a.severity_score for a in assessments)
        composite_risk = min(1.0, total_severity * 1.5)

        high_risk = [a for a in assessments if a.severity_score >= 0.05]
        guardrails = [
            f"Activate {a.mitigation_strategy}" for a in high_risk
        ]
        if not guardrails:
            guardrails.append("Standard telemetry assertions and heartbeat supervision active.")

        return StrategyRiskProfile(
            strategy_id=strategy.strategy_id,
            overall_risk_score=round(composite_risk, 4),
            high_risk_vectors=high_risk,
            all_assessments=assessments,
            mitigation_coverage=0.98,
            recommended_guardrails=guardrails,
        )
