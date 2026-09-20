from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
import uuid

class VerificationType(str, Enum):
    FUNCTIONAL = "FUNCTIONAL"
    PERFORMANCE = "PERFORMANCE"
    SECURITY = "SECURITY"
    RELIABILITY = "RELIABILITY"
    AI_QUALITY = "AI_QUALITY"
    COMPLIANCE = "COMPLIANCE"
    CHAOS = "CHAOS"
    REGRESSION = "REGRESSION"
    BUSINESS_ACCEPTANCE = "BUSINESS_ACCEPTANCE"

@dataclass(frozen=True)
class QualityGateRuleDefinition:
    metric_name: str
    operator: str
    threshold: float
    is_hard_blocker: bool = True

@dataclass(frozen=True)
class VerificationSpecification:
    specification_id: str
    name: str
    verification_type: VerificationType
    objective: str
    target_subsystem: str
    target_version: str
    dataset_class: str = "HAPPY_PATH"
    environment_tier: str = "staging"
    required_metrics: List[str] = field(default_factory=list)
    quality_gate_rules: List[QualityGateRuleDefinition] = field(default_factory=list)
    owner: str = "verification-squad"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @classmethod
    def create(
        cls,
        name: str,
        verification_type: VerificationType,
        objective: str,
        target_subsystem: str,
        target_version: str,
        dataset_class: str = "HAPPY_PATH",
        environment_tier: str = "staging",
        required_metrics: Optional[List[str]] = None,
        quality_gate_rules: Optional[List[QualityGateRuleDefinition]] = None,
        owner: str = "verification-squad"
    ) -> "VerificationSpecification":
        return cls(
            specification_id=f"vspec_{uuid.uuid4().hex[:12]}",
            name=name,
            verification_type=verification_type,
            objective=objective,
            target_subsystem=target_subsystem,
            target_version=target_version,
            dataset_class=dataset_class,
            environment_tier=environment_tier,
            required_metrics=required_metrics or ["accuracy", "p99_latency_ms"],
            quality_gate_rules=quality_gate_rules or [
                QualityGateRuleDefinition("accuracy", ">=", 0.95, is_hard_blocker=True),
                QualityGateRuleDefinition("p99_latency_ms", "<=", 100.0, is_hard_blocker=False)
            ],
            owner=owner
        )
