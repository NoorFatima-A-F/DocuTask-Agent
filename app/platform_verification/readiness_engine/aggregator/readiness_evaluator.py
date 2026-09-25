"""
Readiness Evaluator & Aggregation Engine (Part 3H.3.2.8).
Aggregates health signals from Database, Redis/Queue, Storage, AI Provider, and Worker Fleet,
applies the dependency policy, and generates deterministic traffic admission decisions.
"""
import time
from datetime import datetime, timezone
from typing import List, Optional
from app.platform_verification.readiness_engine.domain.models import (
    ReadinessState,
    DependencyCriticality,
    TrafficAction,
    ReadinessEvaluationResult,
    DatabaseReadinessReport,
    QueueReadinessReport,
    StorageReadinessReport,
    AIProviderReadinessReport,
    WorkerReadinessReport,
)
from app.platform_verification.readiness_engine.policy.dependency_policy_engine import DependencyPolicyEngine


class ReadinessEvaluator:
    """
    Central aggregation engine deciding overall service readiness state and traffic routing.
    """

    def __init__(self, policy_engine: Optional[DependencyPolicyEngine] = None):
        self.policy_engine = policy_engine or DependencyPolicyEngine()

    def evaluate_readiness(
        self,
        db_report: DatabaseReadinessReport,
        queue_report: QueueReadinessReport,
        storage_report: StorageReadinessReport,
        ai_report: AIProviderReadinessReport,
        worker_report: WorkerReadinessReport,
    ) -> ReadinessEvaluationResult:
        start_time = time.perf_counter()

        failed_deps: List[str] = []
        degraded_deps: List[str] = []
        healthy_deps: List[str] = []

        # 1. Database Evaluation (Critical)
        if not db_report.passed:
            failed_deps.append("postgres")
        else:
            healthy_deps.append("postgres")

        # 2. Redis/Queue Evaluation (Critical)
        if not queue_report.ping_pong_ok:
            failed_deps.append("redis")
        elif queue_report.status == "DEGRADED":
            degraded_deps.append("redis")
        else:
            healthy_deps.append("redis")

        # 3. Storage Evaluation (Critical)
        if not storage_report.passed:
            failed_deps.append("storage")
        else:
            healthy_deps.append("storage")

        # 4. Worker Evaluation (Critical)
        if not worker_report.passed:
            failed_deps.append("workers")
        elif worker_report.status == "OVERLOADED":
            degraded_deps.append("workers")
        else:
            healthy_deps.append("workers")

        # 5. Gemini AI Evaluation (Important)
        if not ai_report.passed or ai_report.fallback_mode_active:
            degraded_deps.append("gemini")
        else:
            healthy_deps.append("gemini")

        # Compute Final State & Action
        # Any critical failure -> NOT_READY, REJECT_TRAFFIC
        has_critical_failure = any(
            self.policy_engine.get_criticality(dep) == DependencyCriticality.CRITICAL
            for dep in failed_deps
        )

        if has_critical_failure or len(failed_deps) > 0:
            state = ReadinessState.NOT_READY
            traffic_action = TrafficAction.REJECT_TRAFFIC
            traffic_allowed = False
            reason = f"Critical dependencies unavailable: {', '.join(failed_deps)}"
        elif len(degraded_deps) > 0:
            state = ReadinessState.DEGRADED
            traffic_action = TrafficAction.THROTTLE_TRAFFIC
            traffic_allowed = True
            reason = f"Operating in degraded mode. Elevated latency/fallback active for: {', '.join(degraded_deps)}"
        else:
            state = ReadinessState.READY
            traffic_action = TrafficAction.ALLOW_TRAFFIC
            traffic_allowed = True
            reason = "All critical and important dependencies verified healthy"

        duration_ms = (time.perf_counter() - start_time) * 1000.0

        checks = {
            "database": {
                "status": db_report.status,
                "latency_ms": db_report.latency_ms,
                "connections_available": db_report.connections_available,
            },
            "queue": {
                "status": queue_report.status,
                "latency_ms": queue_report.latency_ms,
                "queue_depth": queue_report.queue_depth,
            },
            "storage": {
                "status": storage_report.status,
                "latency_ms": storage_report.latency_ms,
                "integrity": "verified" if storage_report.integrity_verified else "failed",
            },
            "ai_provider": {
                "status": ai_report.status,
                "latency_ms": ai_report.latency_ms,
                "quota_remaining_pct": ai_report.quota_remaining_pct,
                "fallback_mode": ai_report.fallback_mode_active,
            },
            "workers": {
                "status": worker_report.status,
                "worker_id": worker_report.worker_id,
                "active_jobs": worker_report.active_jobs,
                "capacity": worker_report.capacity,
            },
        }

        return ReadinessEvaluationResult(
            service="docutask-api",
            state=state,
            traffic_action=traffic_action,
            traffic_allowed=traffic_allowed,
            reason=reason,
            failed_dependencies=failed_deps,
            degraded_dependencies=degraded_deps,
            healthy_dependencies=healthy_deps,
            checks=checks,
            evaluation_duration_ms=round(duration_ms, 2),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
