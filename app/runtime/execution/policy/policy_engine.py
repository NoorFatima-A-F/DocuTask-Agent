"""
Policy & Governance Engine for Phase 13.15.
Evaluates execution safety invariants, RBAC/ABAC rules, risk thresholds, financial gates, and HITL approvals.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.execution.events.execution_events import (
    ExecutionEvent,
    ExecutionEventType,
    PolicyDecision,
    RiskLevel,
    execution_event_bus,
)


@dataclass
class PolicyRule:
    rule_id: str
    name: str
    description: str
    target_tools: List[str] = field(default_factory=list)  # ["*"] for all
    condition_expression: str = ""
    decision: PolicyDecision = PolicyDecision.ALLOW
    risk_level: RiskLevel = RiskLevel.MEDIUM
    requires_simulation: bool = False
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "description": self.description,
            "target_tools": self.target_tools,
            "condition_expression": self.condition_expression,
            "decision": self.decision.value if isinstance(self.decision, PolicyDecision) else str(self.decision),
            "risk_level": self.risk_level.value if isinstance(self.risk_level, RiskLevel) else str(self.risk_level),
            "requires_simulation": self.requires_simulation,
            "is_active": self.is_active,
        }


@dataclass
class ApprovalRequest:
    approval_id: str
    mission_id: str
    step_id: str
    tool_id: str
    requester: str
    risk_level: RiskLevel
    reason: str
    status: str = "pending"  # pending, approved, rejected
    approver: Optional[str] = None
    decision_timestamp: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "approval_id": self.approval_id,
            "mission_id": self.mission_id,
            "step_id": self.step_id,
            "tool_id": self.tool_id,
            "requester": self.requester,
            "risk_level": self.risk_level.value if isinstance(self.risk_level, RiskLevel) else str(self.risk_level),
            "reason": self.reason,
            "status": self.status,
            "approver": self.approver,
            "decision_timestamp": self.decision_timestamp,
            "created_at": self.created_at,
        }


class PolicyEngine:
    """Evaluates security, financial, and operational policies prior to execution."""

    def __init__(self):
        self._rules: Dict[str, PolicyRule] = {}
        self._approvals: Dict[str, ApprovalRequest] = {}
        self._initialize_seed_rules()

    def _initialize_seed_rules(self) -> None:
        seed_rules = [
            PolicyRule(
                rule_id="rule_require_simulation_for_high_risk",
                name="Enforce Simulation Sandbox for High Risk Operations",
                description="Any tool categorized with HIGH or CRITICAL risk must pass digital twin dry-run simulation first.",
                target_tools=["*"],
                condition_expression="tool.risk_level in ['high', 'critical']",
                decision=PolicyDecision.REQUIRE_SIMULATION,
                risk_level=RiskLevel.HIGH,
                requires_simulation=True,
            ),
            PolicyRule(
                rule_id="rule_financial_invoice_cap",
                name="Financial Invoicing Safety Threshold",
                description="Stripe customer invoices exceeding $1,000.00 (100000 cents) require executive human approval.",
                target_tools=["stripe_create_customer_invoice"],
                condition_expression="inputs.amount_cents > 100000",
                decision=PolicyDecision.REQUIRE_APPROVAL,
                risk_level=RiskLevel.HIGH,
            ),
            PolicyRule(
                rule_id="rule_k8s_production_scale_cap",
                name="Kubernetes Production Replica Gate",
                description="Scaling production deployments to > 10 replicas requires human operator approval.",
                target_tools=["k8s_scale_deployment"],
                condition_expression="inputs.replicas > 10 and inputs.namespace == 'production'",
                decision=PolicyDecision.REQUIRE_APPROVAL,
                risk_level=RiskLevel.HIGH,
            ),
            PolicyRule(
                rule_id="rule_db_destructive_drop_deny",
                name="Prevent Destructive Database Drops",
                description="Unconditionally block DROP TABLE / TRUNCATE queries against production databases.",
                target_tools=["postgres_execute_query"],
                condition_expression="'DROP' in inputs.query.upper() or 'TRUNCATE' in inputs.query.upper()",
                decision=PolicyDecision.DENY,
                risk_level=RiskLevel.CRITICAL,
            ),
        ]
        for r in seed_rules:
            self._rules[r.rule_id] = r

    def add_rule(self, rule: PolicyRule) -> PolicyRule:
        self._rules[rule.rule_id] = rule
        return rule

    def list_rules(self) -> List[PolicyRule]:
        return list(self._rules.values())

    def evaluate_step(
        self,
        tool_id: str,
        inputs: Dict[str, Any],
        tool_risk: RiskLevel,
        actor: str = "autonomous_system",
    ) -> tuple[PolicyDecision, Optional[str]]:
        """Evaluates whether a tool execution is permitted, requires approval, or is denied."""
        # Check explicit rules
        for rule in self._rules.values():
            if not rule.is_active:
                continue

            if "*" in rule.target_tools or tool_id in rule.target_tools:
                # Basic condition checking
                if "DROP" in str(inputs.get("query", "")).upper() or "TRUNCATE" in str(inputs.get("query", "")).upper():
                    if rule.rule_id == "rule_db_destructive_drop_deny":
                        execution_event_bus.publish(
                            ExecutionEvent(
                                event_type=ExecutionEventType.POLICY_EVALUATED,
                                source="policy_engine",
                                payload={"decision": "deny", "rule": rule.name, "tool_id": tool_id},
                                risk_level=RiskLevel.CRITICAL,
                            )
                        )
                        return PolicyDecision.DENY, f"Violated policy '{rule.name}': Destructive SQL queries are strictly denied."

                if tool_id == "stripe_create_customer_invoice":
                    amount = inputs.get("amount_cents", 0)
                    if amount > 100000:
                        return PolicyDecision.REQUIRE_APPROVAL, f"Invoice amount ({amount} cents) exceeds $1,000 threshold. Approval required."

                if tool_id == "k8s_scale_deployment":
                    replicas = inputs.get("replicas", 0)
                    namespace = inputs.get("namespace", "production")
                    if replicas > 10 and namespace == "production":
                        return PolicyDecision.REQUIRE_APPROVAL, f"Scaling replica count to {replicas} in {namespace} requires operator sign-off."

        if tool_risk in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            return PolicyDecision.REQUIRE_SIMULATION, "High-risk tool invocation requires digital twin simulation."

        return PolicyDecision.ALLOW, None

    def request_approval(
        self,
        mission_id: str,
        step_id: str,
        tool_id: str,
        requester: str,
        risk_level: RiskLevel,
        reason: str,
    ) -> ApprovalRequest:
        aid = f"approval_{uuid.uuid4().hex[:8]}"
        req = ApprovalRequest(
            approval_id=aid,
            mission_id=mission_id,
            step_id=step_id,
            tool_id=tool_id,
            requester=requester,
            risk_level=risk_level,
            reason=reason,
        )
        self._approvals[aid] = req
        execution_event_bus.publish(
            ExecutionEvent(
                event_type=ExecutionEventType.APPROVAL_REQUESTED,
                source="policy_engine",
                payload=req.to_dict(),
                risk_level=risk_level,
            )
        )
        return req

    def resolve_approval(self, approval_id: str, approved: bool, approver: str = "executive_lead") -> Optional[ApprovalRequest]:
        req = self._approvals.get(approval_id)
        if not req:
            return None
        req.status = "approved" if approved else "rejected"
        req.approver = approver
        req.decision_timestamp = datetime.now(timezone.utc).isoformat()

        execution_event_bus.publish(
            ExecutionEvent(
                event_type=ExecutionEventType.APPROVAL_GRANTED if approved else ExecutionEventType.APPROVAL_REJECTED,
                source="policy_engine",
                payload=req.to_dict(),
                risk_level=req.risk_level,
            )
        )
        return req

    def list_approvals(self, status: Optional[str] = None) -> List[ApprovalRequest]:
        items = list(self._approvals.values())
        if status:
            items = [a for a in items if a.status.lower() == status.lower()]
        return items


# Global Singleton
policy_engine = PolicyEngine()
