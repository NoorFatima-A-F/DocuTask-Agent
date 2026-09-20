"""
Phase 13.20: Enterprise Agent Registry Service.
Maintains the centralized enterprise inventory of AI applications, metadata, and lifecycle states.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid
from app.platform_ai_lifecycle.models.schemas import (
    AgentApplication,
    AgentCategory,
    AgentLifecycleState,
)


class AgentRegistryService:
    def __init__(self):
        self._agents: Dict[str, AgentApplication] = {}
        self._seed_default_agents()

    def _seed_default_agents(self) -> None:
        a1 = AgentApplication(
            agent_id="agt_acme_invoice_reconciler",
            tenant_id="tenant_acme_corp",
            organization_id="org_acme_americas",
            workspace_id="ws_acme_invoicing",
            name="Autonomous Invoice Reconciler",
            slug="invoice-reconciler",
            category=AgentCategory.FINANCIAL_AUDIT,
            owner_id="usr_acme_analyst",
            owner_email="analyst@acmecorp.com",
            description="3-way automated matching of invoices, purchase orders, and goods receipts with ERP sync.",
            lifecycle_state=AgentLifecycleState.DEPLOYED,
            current_version="1.2.0",
            tags=["finance", "invoicing", "sap", "audit"],
        )
        a2 = AgentApplication(
            agent_id="agt_globex_hipaa_scrubber",
            tenant_id="tenant_globex_health",
            organization_id="org_globex_clinical",
            workspace_id="ws_globex_records",
            name="HIPAA PII/PHI Medical Scrubber",
            slug="hipaa-scrubber",
            category=AgentCategory.COMPLIANCE,
            owner_id="usr_globex_lead",
            owner_email="compliance@globexhealth.com",
            description="High-precision automated redaction of 18 HIPAA identifier types in medical clinical notes.",
            lifecycle_state=AgentLifecycleState.DEPLOYED,
            current_version="2.0.1",
            tags=["healthcare", "hipaa", "redaction", "ehr"],
        )
        a3 = AgentApplication(
            agent_id="agt_acme_legal_contract_auditor",
            tenant_id="tenant_acme_corp",
            organization_id="org_acme_emea",
            workspace_id="ws_acme_claims",
            name="Legal Contract Clause & Risk Auditor",
            slug="legal-auditor",
            category=AgentCategory.LEGAL_ANALYSIS,
            owner_id="usr_acme_admin",
            owner_email="admin@acmecorp.com",
            description="Extracts indemnification clauses, governing law, and unapproved liability deviations.",
            lifecycle_state=AgentLifecycleState.SECURITY_REVIEW,
            current_version="1.0.0-rc1",
            tags=["legal", "contracts", "nda", "risk"],
        )

        for agt in [a1, a2, a3]:
            self._agents[agt.agent_id] = agt

    def register_agent(
        self,
        tenant_id: str,
        organization_id: str,
        workspace_id: str,
        name: str,
        slug: str,
        category: AgentCategory,
        owner_id: str,
        owner_email: str,
        description: str,
        tags: Optional[List[str]] = None,
    ) -> AgentApplication:
        agent_id = f"agt_{uuid.uuid4().hex[:8]}"
        agent = AgentApplication(
            agent_id=agent_id,
            tenant_id=tenant_id,
            organization_id=organization_id,
            workspace_id=workspace_id,
            name=name,
            slug=slug,
            category=category,
            owner_id=owner_id,
            owner_email=owner_email,
            description=description,
            lifecycle_state=AgentLifecycleState.DRAFT,
            current_version="1.0.0",
            tags=tags or [],
        )
        self._agents[agent_id] = agent
        return agent

    def get_agent(self, agent_id: str) -> Optional[AgentApplication]:
        return self._agents.get(agent_id)

    def list_agents(
        self,
        tenant_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        category: Optional[AgentCategory] = None,
        state: Optional[AgentLifecycleState] = None,
    ) -> List[AgentApplication]:
        items = list(self._agents.values())
        if tenant_id:
            items = [a for a in items if a.tenant_id == tenant_id]
        if workspace_id:
            items = [a for a in items if a.workspace_id == workspace_id]
        if category:
            items = [a for a in items if a.category == category]
        if state:
            items = [a for a in items if a.lifecycle_state == state]
        return items

    def update_lifecycle_state(self, agent_id: str, new_state: AgentLifecycleState) -> AgentApplication:
        agent = self._agents.get(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found")
        agent.lifecycle_state = new_state
        agent.updated_at = datetime.now(timezone.utc).isoformat()
        return agent
