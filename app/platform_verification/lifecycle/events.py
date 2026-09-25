from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid

@dataclass
class VerificationLifecycleEvent:
    event_id: str = field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:12]}")
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1

@dataclass
class VerificationCreated(VerificationLifecycleEvent):
    specification_id: str = ""
    name: str = ""

@dataclass
class VerificationPlanned(VerificationLifecycleEvent):
    specification_id: str = ""
    plan_id: str = ""

@dataclass
class ExecutionStarted(VerificationLifecycleEvent):
    execution_id: str = ""
    plan_id: str = ""

@dataclass
class TaskCompleted(VerificationLifecycleEvent):
    execution_id: str = ""
    task_id: str = ""

@dataclass
class EvidenceCollected(VerificationLifecycleEvent):
    execution_id: str = ""
    artifact_id: str = ""

@dataclass
class MetricsGenerated(VerificationLifecycleEvent):
    execution_id: str = ""
    metric_count: int = 0

@dataclass
class EvaluationCompleted(VerificationLifecycleEvent):
    specification_id: str = ""
    overall_passed: bool = False

@dataclass
class QualityGatePassed(VerificationLifecycleEvent):
    specification_id: str = ""
    decision: str = ""

@dataclass
class CertificationIssued(VerificationLifecycleEvent):
    certificate_id: str = ""
    target_subsystem: str = ""

@dataclass
class VerificationArchived(VerificationLifecycleEvent):
    specification_id: str = ""
