"""
AMCN-SIP Phase 13.8 - Swarm Governance & Authority Control
Tiered authority hierarchy, delegation contracts, anti-usurpation invariants, and policy enforcement.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum


class AuthorityTier(str, Enum):
    TIER_1_EXECUTIVE = "TIER_1_EXECUTIVE"
    TIER_2_ORCHESTRATOR = "TIER_2_ORCHESTRATOR"
    TIER_3_GOVERNOR = "TIER_3_GOVERNOR"
    TIER_4_OPERATOR = "TIER_4_OPERATOR"
    TIER_5_AUDITOR = "TIER_5_AUDITOR"


ROLE_TIER_MAPPING: Dict[str, AuthorityTier] = {
    "EXECUTIVE": AuthorityTier.TIER_1_EXECUTIVE,
    "PLANNER": AuthorityTier.TIER_2_ORCHESTRATOR,
    "COORDINATOR": AuthorityTier.TIER_2_ORCHESTRATOR,
    "NEGOTIATOR": AuthorityTier.TIER_3_GOVERNOR,
    "RESOURCE": AuthorityTier.TIER_3_GOVERNOR,
    "SECURITY": AuthorityTier.TIER_3_GOVERNOR,
    "SPECIALIST": AuthorityTier.TIER_4_OPERATOR,
    "VALIDATOR": AuthorityTier.TIER_4_OPERATOR,
    "REVIEWER": AuthorityTier.TIER_4_OPERATOR,
    "RECOVERY": AuthorityTier.TIER_4_OPERATOR,
    "OBSERVER": AuthorityTier.TIER_5_AUDITOR,
}


@dataclass
class DelegationPolicy:
    policy_id: str
    name: str
    max_delegation_depth: int = 3
    allow_cross_tier_escalation: bool = False
    required_quorum_for_override: float = 0.67
    active: bool = True


@dataclass
class DelegationGrant:
    grant_id: str
    delegator_id: str
    delegator_role: str
    delegatee_id: str
    delegatee_role: str
    scope: str
    depth: int = 1
    granted_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    grant_signature: str = ""

    def compute_signature(self) -> str:
        payload = f"{self.grant_id}:{self.delegator_id}:{self.delegatee_id}:{self.scope}:{self.depth}"
        return hashlib.sha256(payload.encode()).hexdigest()


class DelegationValidator:
    """
    Validates delegation requests and verifies anti-usurpation constraints.
    """

    def validate_delegation(
        self,
        delegator_role: str,
        delegatee_role: str,
        policy: DelegationPolicy,
        current_depth: int,
    ) -> Tuple[bool, str]:
        if current_depth > policy.max_delegation_depth:
            return False, f"Delegation depth {current_depth} exceeds policy maximum {policy.max_delegation_depth}."

        del_tier = ROLE_TIER_MAPPING.get(delegator_role, AuthorityTier.TIER_5_AUDITOR)
        rec_tier = ROLE_TIER_MAPPING.get(delegatee_role, AuthorityTier.TIER_5_AUDITOR)

        # Lower tier values mean higher authority
        del_level = list(AuthorityTier).index(del_tier)
        rec_level = list(AuthorityTier).index(rec_tier)

        if rec_level < del_level and not policy.allow_cross_tier_escalation:
            return False, f"Anti-usurpation violation: {delegator_role} cannot delegate to superior tier {delegatee_role}."

        return True, "Delegation authorization verified."


class SwarmGovernanceEngine:
    """
    Master authority and policy controller for the multi-agent society.
    """

    def __init__(self):
        self.validator = DelegationValidator()
        self.policy = DelegationPolicy(
            policy_id="gov-pol-standard",
            name="Standard Multi-Agent Autonomous Governance Policy",
            max_delegation_depth=3,
            allow_cross_tier_escalation=False,
            required_quorum_for_override=0.67,
            active=True,
        )
        self._grants: Dict[str, DelegationGrant] = {}
        self._audit_log: List[Dict[str, Any]] = []
        self._seed_default_grants()

    def grant_delegation(
        self,
        delegator_id: str,
        delegator_role: str,
        delegatee_id: str,
        delegatee_role: str,
        scope: str,
        depth: int = 1,
    ) -> Tuple[bool, Optional[DelegationGrant], str]:
        valid, msg = self.validator.validate_delegation(delegator_role, delegatee_role, self.policy, depth)
        if not valid:
            self._audit_log.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": "DELEGATION_REJECTED",
                "reason": msg,
                "delegator": delegator_id,
                "delegatee": delegatee_id,
            })
            return False, None, msg

        gid = f"grant_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:18]}"
        grant = DelegationGrant(
            grant_id=gid,
            delegator_id=delegator_id,
            delegator_role=delegator_role,
            delegatee_id=delegatee_id,
            delegatee_role=delegatee_role,
            scope=scope,
            depth=depth,
        )
        grant.grant_signature = grant.compute_signature()
        self._grants[gid] = grant

        self._audit_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "DELEGATION_GRANTED",
            "grant_id": gid,
            "delegator": delegator_id,
            "delegatee": delegatee_id,
            "signature": grant.grant_signature,
        })
        return True, grant, "Delegation granted successfully."

    def list_grants(self) -> List[DelegationGrant]:
        return list(self._grants.values())

    def get_audit_log(self) -> List[Dict[str, Any]]:
        return self._audit_log[-50:]

    def get_governance_summary(self) -> Dict[str, Any]:
        return {
            "policy": self.policy.__dict__,
            "total_active_grants": len(self._grants),
            "tier_hierarchy": {role: tier.value for role, tier in ROLE_TIER_MAPPING.items()},
            "grants": [g.__dict__ for g in self._grants.values()],
            "audit_log": self._audit_log[-20:],
        }

    def _seed_default_grants(self):
        self.grant_delegation(
            delegator_id="agent-exec-01",
            delegator_role="EXECUTIVE",
            delegatee_id="agent-plan-01",
            delegatee_role="PLANNER",
            scope="MISSION_DECOMPOSITION",
            depth=1,
        )
        self.grant_delegation(
            delegator_id="agent-plan-01",
            delegator_role="PLANNER",
            delegatee_id="agent-coord-01",
            delegatee_role="COORDINATOR",
            scope="DAG_TASK_DISPATCH",
            depth=2,
        )
        self.grant_delegation(
            delegator_id="agent-coord-01",
            delegator_role="COORDINATOR",
            delegatee_id="agent-spec-ocr",
            delegatee_role="SPECIALIST",
            scope="IMAGE_PARSE_EXECUTE",
            depth=3,
        )
