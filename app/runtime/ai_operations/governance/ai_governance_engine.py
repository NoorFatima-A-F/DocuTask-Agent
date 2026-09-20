"""
Phase 13.17: AI Governance Engine
Manages immutable audit trails, policy enforcement, and compliance reporting.
"""

from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from app.runtime.ai_operations.models.schemas import GovernanceAuditRecord
from app.runtime.ai_operations.governance.compliance_monitor import ComplianceMonitor


class AIGovernanceEngine:
    """Master governance and audit trail engine."""

    def __init__(self):
        self._audit_logs: List[GovernanceAuditRecord] = []
        self._seed_audit_logs()

    def _seed_audit_logs(self):
        records = [
            {
                "event_type": "PROMPT_EVALUATION",
                "actor": "system",
                "agent_id": "agent_chief_architect",
                "summary": "Completed baseline prompt benchmark evaluation. Compliance score 100%.",
                "pii_detected": False,
                "policy": "ENTERPRISE_AGENT_SAFETY_V2",
            },
            {
                "event_type": "PII_REDACTION_EVENT",
                "actor": "compliance_guardrail",
                "agent_id": "agent_doc_extractor",
                "summary": "Sanitized unmasked email address from incoming OCR payload.",
                "pii_detected": True,
                "pii_types": ["EMAIL"],
                "policy": "DATA_PRIVACY_GDPR_CCPA",
            },
            {
                "event_type": "PROPOSAL_APPROVAL_GATE",
                "actor": "admin_security",
                "agent_id": "agent_chief_architect",
                "summary": "Admin approved candidate prompt v1.1.0 for canary deployment.",
                "pii_detected": False,
                "policy": "HITL_CHANGE_MANAGEMENT",
            },
        ]
        for r in records:
            sig = hashlib.sha256(f"{r['event_type']}_{r['summary']}".encode()).hexdigest()
            rec = GovernanceAuditRecord(
                event_type=r["event_type"],
                actor=r["actor"],
                agent_id=r.get("agent_id"),
                action_summary=r["summary"],
                compliance_passed=True,
                pii_detected=r.get("pii_detected", False),
                pii_types_redacted=r.get("pii_types", []),
                policy_name=r.get("policy"),
                signature_hash=sig,
            )
            self._audit_logs.append(rec)

    def log_event(
        self,
        event_type: str,
        actor: str,
        action_summary: str,
        agent_id: Optional[str] = None,
        compliance_passed: bool = True,
        pii_detected: bool = False,
        pii_types_redacted: Optional[List[str]] = None,
        policy_name: Optional[str] = None,
    ) -> GovernanceAuditRecord:
        raw_str = f"{event_type}:{actor}:{action_summary}:{datetime.now(timezone.utc).isoformat()}"
        sig = hashlib.sha256(raw_str.encode()).hexdigest()

        rec = GovernanceAuditRecord(
            event_type=event_type,
            actor=actor,
            agent_id=agent_id,
            action_summary=action_summary,
            compliance_passed=compliance_passed,
            pii_detected=pii_detected,
            pii_types_redacted=pii_types_redacted or [],
            policy_name=policy_name or "ENTERPRISE_DEFAULT",
            signature_hash=sig,
        )
        self._audit_logs.append(rec)
        return rec

    def get_audit_logs(self, limit: int = 50, agent_id: Optional[str] = None) -> List[GovernanceAuditRecord]:
        logs = self._audit_logs
        if agent_id:
            logs = [l for l in logs if l.agent_id == agent_id]
        return logs[-limit:]
