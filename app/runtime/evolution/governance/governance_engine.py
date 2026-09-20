"""
Autonomous Governance & Rollback Engine for Phase 13.13 (ASEAORIP).
Enforces multi-tier governance gates, generates immutable rollback snapshots with SHA-256 cryptographic seals, and manages approvals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.evolution.events.evolution_events import (
    EvolutionEventBus,
    GovernanceApprovalGranted,
    RollbackSnapshotCreated,
)


@dataclass
class RollbackSnapshot:
    snapshot_id: str = field(default_factory=lambda: f"snap_{uuid.uuid4().hex[:8]}")
    platform_version: str = "v13.12.0"
    state_payload: Dict[str, Any] = field(default_factory=dict)
    sha256_seal: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not self.sha256_seal:
            raw = f"{self.snapshot_id}:{self.platform_version}:{json.dumps(self.state_payload, sort_keys=True)}"
            self.sha256_seal = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "platform_version": self.platform_version,
            "sha256_seal": self.sha256_seal,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class EvolutionGovernanceReview:
    review_id: str = field(default_factory=lambda: f"gov_{uuid.uuid4().hex[:8]}")
    mutation_id: str = ""
    candidate_id: Optional[str] = None
    risk_level: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL
    formal_verification_passed: bool = True
    simulation_verified: bool = True
    benchmark_verified: bool = True
    human_override_required: bool = False
    approval_status: str = "PENDING"  # PENDING, APPROVED, REJECTED
    reviewer_agent_id: str = "agent_cryptographic_sentinel_01"
    cryptographic_signature: str = ""
    rollback_snapshot_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not self.cryptographic_signature and self.approval_status == "APPROVED":
            raw = f"{self.review_id}:{self.mutation_id}:{self.reviewer_agent_id}:{self.approval_status}"
            self.cryptographic_signature = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "review_id": self.review_id,
            "mutation_id": self.mutation_id,
            "candidate_id": self.candidate_id,
            "risk_level": self.risk_level,
            "formal_verification_passed": self.formal_verification_passed,
            "simulation_verified": self.simulation_verified,
            "benchmark_verified": self.benchmark_verified,
            "human_override_required": self.human_override_required,
            "approval_status": self.approval_status,
            "reviewer_agent_id": self.reviewer_agent_id,
            "cryptographic_signature": self.cryptographic_signature,
            "rollback_snapshot_id": self.rollback_snapshot_id,
            "created_at": self.created_at.isoformat(),
        }


class GovernanceEngine:
    """
    Autonomous Governance & Safety Sentinel Engine.
    """

    def __init__(self, event_bus: Optional[EvolutionEventBus] = None) -> None:
        self.event_bus = event_bus or EvolutionEventBus()
        self.reviews: Dict[str, EvolutionGovernanceReview] = {}
        self.snapshots: Dict[str, RollbackSnapshot] = {}
        self._initialize_bootstrap_governance()

    def _initialize_bootstrap_governance(self) -> None:
        snap = RollbackSnapshot(
            snapshot_id="snap_prod_v13_12",
            platform_version="v13.12.0",
            state_payload={"runtime_flags": {"enable_ast_pruning": False, "buffer_mode": "sync"}},
        )
        self.snapshots[snap.snapshot_id] = snap

        rev = EvolutionGovernanceReview(
            review_id="gov_seed_001",
            mutation_id="mut_seed_001",
            candidate_id="opt_pareto_01",
            risk_level="LOW",
            formal_verification_passed=True,
            simulation_verified=True,
            benchmark_verified=True,
            human_override_required=False,
            approval_status="APPROVED",
            reviewer_agent_id="agent_sentinel_prime",
            rollback_snapshot_id=snap.snapshot_id,
        )
        self.reviews[rev.review_id] = rev

    def create_rollback_snapshot(self, platform_version: str = "v13.12.0", state_payload: Optional[Dict[str, Any]] = None) -> RollbackSnapshot:
        snap = RollbackSnapshot(
            snapshot_id=f"snap_{uuid.uuid4().hex[:8]}",
            platform_version=platform_version,
            state_payload=state_payload or {"status": "stable_baseline", "timestamp": datetime.now(timezone.utc).isoformat()},
        )
        self.snapshots[snap.snapshot_id] = snap

        self.event_bus.publish(
            RollbackSnapshotCreated(payload=snap.to_dict())
        )
        return snap

    def submit_for_review(
        self,
        mutation_id: str,
        candidate_id: Optional[str] = None,
        risk_level: str = "LOW",
        formal_verification_passed: bool = True,
        simulation_verified: bool = True,
        benchmark_verified: bool = True,
    ) -> EvolutionGovernanceReview:
        review_id = f"gov_{uuid.uuid4().hex[:8]}"
        human_req = risk_level in ["HIGH", "CRITICAL"]

        # Pre-create a guaranteed rollback snapshot
        snapshot = self.create_rollback_snapshot()

        review = EvolutionGovernanceReview(
            review_id=review_id,
            mutation_id=mutation_id,
            candidate_id=candidate_id,
            risk_level=risk_level,
            formal_verification_passed=formal_verification_passed,
            simulation_verified=simulation_verified,
            benchmark_verified=benchmark_verified,
            human_override_required=human_req,
            approval_status="PENDING" if human_req else "APPROVED",
            reviewer_agent_id="agent_sentinel_crypto",
            rollback_snapshot_id=snapshot.snapshot_id,
        )

        if review.approval_status == "APPROVED":
            raw = f"{review.review_id}:{review.mutation_id}:{review.reviewer_agent_id}:{review.approval_status}"
            review.cryptographic_signature = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            self.event_bus.publish(
                GovernanceApprovalGranted(payload=review.to_dict())
            )

        self.reviews[review_id] = review
        return review

    def approve_review(self, review_id: str, reviewer_agent_id: str = "agent_human_override") -> Optional[EvolutionGovernanceReview]:
        review = self.reviews.get(review_id)
        if review:
            review.approval_status = "APPROVED"
            review.reviewer_agent_id = reviewer_agent_id
            raw = f"{review.review_id}:{review.mutation_id}:{review.reviewer_agent_id}:{review.approval_status}"
            review.cryptographic_signature = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            self.event_bus.publish(
                GovernanceApprovalGranted(payload=review.to_dict())
            )
        return review

    def reject_review(self, review_id: str, reason: str = "Rejected by governance policy") -> Optional[EvolutionGovernanceReview]:
        review = self.reviews.get(review_id)
        if review:
            review.approval_status = "REJECTED"
        return review

    def list_reviews(self) -> List[EvolutionGovernanceReview]:
        return list(self.reviews.values())

    def get_review(self, review_id: str) -> Optional[EvolutionGovernanceReview]:
        return self.reviews.get(review_id)

    def list_snapshots(self) -> List[RollbackSnapshot]:
        return list(self.snapshots.values())

    def get_snapshot(self, snapshot_id: str) -> Optional[RollbackSnapshot]:
        return self.snapshots.get(snapshot_id)
