"""Environment Promotion Orchestrator."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
import uuid
from ..core.controller import DeploymentController
from ..core.deployment import Deployment, DeploymentStrategyType
from ..core.exceptions import PromotionBlockedException
from .policies import PromotionPolicy
from .validation import EnvironmentValidator


class PromotionStatus(str, Enum):
    """Lifecycle states of a promotion request."""
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    EXECUTED = "EXECUTED"
    REJECTED = "REJECTED"


@dataclass
class PromotionRecord:
    """Audit log entry for an environment promotion."""
    promotion_id: str
    release_id: str
    source_env: Optional[str]
    target_env: str
    requested_by: str
    status: PromotionStatus = PromotionStatus.PENDING_APPROVAL
    approved_roles: List[str] = field(default_factory=list)
    approver_details: List[Dict[str, str]] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    executed_deployment_id: Optional[str] = None
    rejection_reason: Optional[str] = None


class PromotionManager:
    """Manages governed progression of releases across environment tiers."""

    def __init__(
        self,
        policy: Optional[PromotionPolicy] = None,
        validator: Optional[EnvironmentValidator] = None,
    ):
        self.policy = policy or PromotionPolicy()
        self.validator = validator or EnvironmentValidator()
        self._promotions: Dict[str, PromotionRecord] = {}

    def request_promotion(
        self,
        release_id: str,
        target_env: str,
        source_env: Optional[str] = None,
        requested_by: str = "pipeline-agent",
    ) -> PromotionRecord:
        """Submits a new promotion request for review and governance gates."""
        prom_id = f"prom-{uuid.uuid4().hex[:8]}"
        record = PromotionRecord(
            promotion_id=prom_id,
            release_id=release_id,
            source_env=source_env,
            target_env=target_env.lower(),
            requested_by=requested_by,
        )
        self._promotions[prom_id] = record
        return record

    def get_promotion(self, promotion_id: str) -> Optional[PromotionRecord]:
        """Fetches promotion record by ID."""
        return self._promotions.get(promotion_id)

    def list_promotions(self, target_env: Optional[str] = None) -> List[PromotionRecord]:
        """Lists promotion records with optional filtering."""
        proms = list(self._promotions.values())
        if target_env:
            proms = [p for p in proms if p.target_env == target_env.lower()]
        return sorted(proms, key=lambda p: p.created_at, reverse=True)

    def approve_promotion(
        self,
        promotion_id: str,
        role: str,
        approver_identity: str,
    ) -> PromotionRecord:
        """Records an authorized role approval for the promotion."""
        record = self.get_promotion(promotion_id)
        if not record:
            raise PromotionBlockedException(f"Promotion request '{promotion_id}' not found")
        if record.status in {PromotionStatus.EXECUTED, PromotionStatus.REJECTED}:
            raise PromotionBlockedException(f"Cannot approve promotion in status {record.status.value}")

        if role not in record.approved_roles:
            record.approved_roles.append(role)
            record.approver_details.append({
                "role": role,
                "approver": approver_identity,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

        return record

    def reject_promotion(self, promotion_id: str, reason: str) -> PromotionRecord:
        """Rejects the promotion request."""
        record = self.get_promotion(promotion_id)
        if not record:
            raise PromotionBlockedException(f"Promotion request '{promotion_id}' not found")
        record.status = PromotionStatus.REJECTED
        record.rejection_reason = reason
        return record

    def execute_promotion(
        self,
        promotion_id: str,
        controller: DeploymentController,
        soak_time_seconds: int = 15,
        test_pass_rate: float = 1.0,
        strategy: DeploymentStrategyType = DeploymentStrategyType.ROLLING,
        replicas: int = 3,
    ) -> Deployment:
        """Validates all policies and pre-flight health, then triggers deployment via controller."""
        record = self.get_promotion(promotion_id)
        if not record:
            raise PromotionBlockedException(f"Promotion request '{promotion_id}' not found")
        if record.status == PromotionStatus.REJECTED:
            raise PromotionBlockedException(f"Promotion '{promotion_id}' was rejected: {record.rejection_reason}")

        # 1. Validate promotion policy
        self.policy.validate_promotion(
            source_env=record.source_env,
            target_env=record.target_env,
            soak_time_seconds=soak_time_seconds,
            test_pass_rate=test_pass_rate,
            approvals=record.approved_roles,
        )

        # 2. Run target environment pre-flight validation
        report = self.validator.validate_environment(record.target_env)
        if not report.overall_passed:
            raise PromotionBlockedException(
                f"Target environment '{record.target_env}' pre-flight validation failed: {report.checks}"
            )

        # 3. Create and execute deployment
        deployment = controller.create_deployment(
            release_id=record.release_id,
            target_environment=record.target_env,
            strategy=strategy,
            replicas=replicas,
            metadata={"promotion_id": promotion_id, "source_env": record.source_env},
        )
        controller.execute_deployment(deployment.deployment_id)

        record.status = PromotionStatus.EXECUTED
        record.executed_deployment_id = deployment.deployment_id
        return deployment
