"""Risk Trend Analysis and Pattern Detection."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field

from .scoring import RiskCategory
from ..warehouse.repositories import GovernanceDataWarehouseRepository
from ..warehouse.schemas import WarehouseQueryFilter


class RiskTrendSignal(BaseModel):
    signal_type: str  # SUDDEN_RISK_SPIKE, REPEATED_VIOLATIONS, UNCONTROLLED_AGENT, UNSAFE_MODEL
    severity: str     # MEDIUM, HIGH, CRITICAL
    entity_id: str
    description: str
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RiskTrendAnalyzer:
    """Detects emerging risk patterns, spikes, and uncontrolled components."""

    def __init__(self, repository: Optional[GovernanceDataWarehouseRepository] = None):
        self.repo = repository or GovernanceDataWarehouseRepository()

    def detect_trend_signals(self, tenant_id: str = "*") -> List[RiskTrendSignal]:
        signals: List[RiskTrendSignal] = []
        q = WarehouseQueryFilter(tenant_id=tenant_id)
        risk_events = self.repo.query_risk_events(q)
        policy_events = self.repo.query_policy_events(q)
        executions = self.repo.query_ai_executions(q)

        # 1. Check for Repeated Policy Violations by same actor/entity
        actor_violations: Dict[str, int] = {}
        for pe in policy_events:
            actor = pe.actor_id or "unknown_actor"
            actor_violations[actor] = actor_violations.get(actor, 0) + 1

        for actor, count in actor_violations.items():
            if count >= 3:
                signals.append(
                    RiskTrendSignal(
                        signal_type="REPEATED_VIOLATIONS",
                        severity="HIGH" if count >= 5 else "MEDIUM",
                        entity_id=actor,
                        description=f"Actor '{actor}' has triggered {count} policy violations.",
                    )
                )

        # 2. Check for Unsafe Models (high risk score or frequent failures)
        model_risks: Dict[str, List[float]] = {}
        for e in executions:
            if e.model_id:
                if e.model_id not in model_risks:
                    model_risks[e.model_id] = []
                model_risks[e.model_id].append(e.risk_score)

        for mid, scores in model_risks.items():
            avg_m_risk = sum(scores) / len(scores)
            if avg_m_risk >= 0.75 and len(scores) >= 2:
                signals.append(
                    RiskTrendSignal(
                        signal_type="UNSAFE_MODEL",
                        severity="CRITICAL",
                        entity_id=mid,
                        description=f"Model '{mid}' exhibits high average risk score ({avg_m_risk:.2f}) across {len(scores)} invocations.",
                    )
                )

        # 3. Check for Uncontrolled Agents (high failures and high overrides)
        agent_execs: Dict[str, List[bool]] = {}
        for e in executions:
            if e.agent_id:
                if e.agent_id not in agent_execs:
                    agent_execs[e.agent_id] = []
                agent_execs[e.agent_id].append(e.is_success)

        for aid, successes in agent_execs.items():
            fail_count = sum(1 for s in successes if not s)
            if fail_count >= 3:
                signals.append(
                    RiskTrendSignal(
                        signal_type="UNCONTROLLED_AGENT",
                        severity="HIGH",
                        entity_id=aid,
                        description=f"Agent '{aid}' encountered {fail_count} failed executions requiring investigation.",
                    )
                )

        return signals
