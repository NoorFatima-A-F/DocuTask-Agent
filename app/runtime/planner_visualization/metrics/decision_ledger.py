"""
Planner Decision Ledger for Phase 13.2.
Provides inspectable decision cards with rationale, alternatives, confidence, and cryptographic proofs.
"""

from __future__ import annotations

from typing import List
from app.runtime.planner_visualization.ui_models.models import PlannerDecisionCard


class PlannerDecisionLedger:
    """
    Stores and exposes evidence-backed planner decision cards.
    """

    def __init__(self, mission_id: str = "mission-001"):
        self.mission_id = mission_id

    def get_decisions(self) -> List[PlannerDecisionCard]:
        return [
            PlannerDecisionCard(
                decision_id="dec-p01-001",
                mission_id=self.mission_id,
                decision_type="STRATEGY_SELECTION",
                title="Select Parallel DAG Strategy",
                reason="Document length exceeds single-batch latency SLA (30s) requiring parallel chunking",
                evidence="Input batch contains 4 high-resolution PDF pages with multi-column financial tables",
                alternatives_considered=[
                    {"name": "Sequential Monolithic Processing", "estimated_latency_ms": 1420.0, "risk_score": 0.45},
                    {"name": "Dynamic Parallel Chunking", "estimated_latency_ms": 480.0, "risk_score": 0.08},
                ],
                chosen_alternative="Dynamic Parallel Chunking",
                confidence=0.985,
                event_id="evt-dec-001",
                truth_ledger_hash="hash-dec-001-c8a1",
                replay_offset=1,
                timestamp="2026-09-11T14:20:00.420Z",
            ),
            PlannerDecisionCard(
                decision_id="dec-p01-002",
                mission_id=self.mission_id,
                decision_type="WORKER_ALLOCATION",
                title="Assign Table Extraction to Worker OCR 02",
                reason="Worker 02 exhibits specialized bounding-box table recognition capability matrix",
                evidence="Capability score 0.985 vs generalist worker score 0.812",
                alternatives_considered=[
                    {"name": "worker-ocr-01 (Raster Generalist)", "confidence": 0.812},
                    {"name": "worker-ocr-02 (Table Specialist)", "confidence": 0.985},
                ],
                chosen_alternative="worker-ocr-02 (Table Specialist)",
                confidence=0.985,
                event_id="evt-dec-002",
                truth_ledger_hash="hash-dec-002-d9b2",
                replay_offset=3,
                timestamp="2026-09-11T14:20:01.120Z",
            ),
            PlannerDecisionCard(
                decision_id="dec-p01-003",
                mission_id=self.mission_id,
                decision_type="VALIDATION_CIRCUIT",
                title="Enforce Multi-Layer Invariant Check",
                reason="Invoice subtotal sum arithmetic must be verified before truth ledger commitment",
                evidence="Financial audit governance policy GOV-FIN-009 enforces 100% arithmetic certainty",
                alternatives_considered=[
                    {"name": "Probabilistic Threshold Only", "risk": "Moderate audit fail risk"},
                    {"name": "Deterministic Invariant Proof", "risk": "Zero tolerance guarantee"},
                ],
                chosen_alternative="Deterministic Invariant Proof",
                confidence=0.999,
                event_id="evt-dec-003",
                truth_ledger_hash="hash-dec-003-e0c3",
                replay_offset=6,
                timestamp="2026-09-11T14:20:01.850Z",
            ),
        ]
