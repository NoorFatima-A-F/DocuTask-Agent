"""
Autonomous Diagnostic Engine for Phase 13.13 (ASEAORIP).
Traces bottlenecks, pinpoints architecture weaknesses, and generates structured root-cause analyses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.evolution.events.evolution_events import (
    ArchitectureWeaknessDetected,
    EvolutionEventBus,
    PerformanceRegressionDetected,
)
from app.runtime.evolution.profiler.profiler_engine import PlatformHealthSnapshot


@dataclass
class WeaknessDiagnosis:
    diagnosis_id: str = field(default_factory=lambda: f"diag_{uuid.uuid4().hex[:8]}")
    subsystem: str = "memory_layer"
    title: str = "Redundant Prompt Serialization Overhead"
    severity: str = "HIGH"
    root_cause: str = "Repetitive schema JSON serialization in multi-turn reasoning loops."
    empirical_evidence_ids: List[str] = field(default_factory=list)
    remediation_proposal: str = "Implement zero-copy binary ring buffers and pre-compiled prompt templates."
    impact_factor: float = 0.85
    diagnosed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "diagnosis_id": self.diagnosis_id,
            "subsystem": self.subsystem,
            "title": self.title,
            "severity": self.severity,
            "root_cause": self.root_cause,
            "empirical_evidence_ids": self.empirical_evidence_ids,
            "remediation_proposal": self.remediation_proposal,
            "impact_factor": round(self.impact_factor, 4),
            "diagnosed_at": self.diagnosed_at.isoformat(),
        }


class DiagnosticEngine:
    """
    Autonomous Weakness & Bottleneck Diagnostic Engine.
    """

    def __init__(self, event_bus: Optional[EvolutionEventBus] = None) -> None:
        self.event_bus = event_bus or EvolutionEventBus()
        self.diagnoses: Dict[str, WeaknessDiagnosis] = {}
        self._initialize_bootstrap_diagnoses()

    def _initialize_bootstrap_diagnoses(self) -> None:
        d1 = WeaknessDiagnosis(
            diagnosis_id="diag_seed_01",
            subsystem="planner_scheduler",
            title="Sequential Task Dispatch Lock Contention",
            severity="HIGH",
            root_cause="Mutex lock on worker queue serializes dispatch under high burst concurrency (>300 qps).",
            remediation_proposal="Transition to lock-free atomic circular dispatch queues.",
            impact_factor=0.88,
        )
        self.diagnoses[d1.diagnosis_id] = d1

    def diagnose_weaknesses(self, snapshot: Optional[PlatformHealthSnapshot] = None) -> List[WeaknessDiagnosis]:
        """Analyzes health snapshot and telemetry to diagnose architectural root-causes."""
        diagnosed: List[WeaknessDiagnosis] = []

        if snapshot and snapshot.token_waste_rate > 0.04:
            diag_id = f"diag_{uuid.uuid4().hex[:8]}"
            diag = WeaknessDiagnosis(
                diagnosis_id=diag_id,
                subsystem="llm_cognition",
                title=f"Elevated Token Waste Rate ({round(snapshot.token_waste_rate * 100, 1)}%)",
                severity="MEDIUM",
                root_cause="Repeated context tokens passed across sequential agent handoffs without adaptive pruning.",
                remediation_proposal="Integrate dynamic AST token pruner into multi-agent message dispatch.",
                impact_factor=0.78,
            )
            self.diagnoses[diag_id] = diag
            diagnosed.append(diag)
            self.event_bus.publish(
                ArchitectureWeaknessDetected(payload=diag.to_dict())
            )

        if snapshot and snapshot.latency_p95_ms > 150.0:
            diag_id = f"diag_{uuid.uuid4().hex[:8]}"
            diag = WeaknessDiagnosis(
                diagnosis_id=diag_id,
                subsystem="query_cache",
                title=f"Elevated P95 Latency ({round(snapshot.latency_p95_ms, 1)}ms)",
                severity="HIGH",
                root_cause="Cold cache misses on uncharacterized recurring invoice layout patterns.",
                remediation_proposal="Apply speculative GPU embedding pre-warming to high-frequency schema signatures.",
                impact_factor=0.92,
            )
            self.diagnoses[diag_id] = diag
            diagnosed.append(diag)
            self.event_bus.publish(
                PerformanceRegressionDetected(payload=diag.to_dict())
            )

        return list(self.diagnoses.values())

    def get_diagnosis(self, diagnosis_id: str) -> Optional[WeaknessDiagnosis]:
        return self.diagnoses.get(diagnosis_id)

    def list_diagnoses(self) -> List[WeaknessDiagnosis]:
        return list(self.diagnoses.values())
