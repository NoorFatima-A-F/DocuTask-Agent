"""
Domain Events representing verification milestones across bounded contexts.
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional
from datetime import datetime, timezone


@dataclass(frozen=True)
class VerificationCreatedEvent:
    definition_id: str
    name: str
    category: str
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class PlanCreatedEvent:
    plan_id: str
    definition_id: str
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class DatasetRegisteredEvent:
    dataset_id: str
    version: str
    checksum: str
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ExecutionStartedEvent:
    execution_id: str
    plan_id: str
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ExecutionCompletedEvent:
    execution_id: str
    status: str
    duration_ms: float
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class EvidenceStoredEvent:
    evidence_id: str
    execution_id: str
    content_hash: str
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class MetricsCalculatedEvent:
    execution_id: str
    metrics_count: int
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class QualityGateEvaluatedEvent:
    execution_id: str
    gate_id: str
    outcome: str
    timestamp: str = datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class CertificationIssuedEvent:
    certification_id: str
    execution_id: str
    level: str
    score: float
    timestamp: str = datetime.now(timezone.utc).isoformat()
