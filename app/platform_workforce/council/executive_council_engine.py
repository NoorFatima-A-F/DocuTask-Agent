"""
8. Executive AI Council Subsystem
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.platform_workforce.models.schemas import ExecutiveCouncilProposition

class ExecutiveCouncilEngine:
    def __init__(self):
        self._propositions: Dict[str, Dict[str, ExecutiveCouncilProposition]] = {}
        self._seed_default_propositions()

    def _seed_default_propositions(self):
        tenant = "default-tenant"
        prop = ExecutiveCouncilProposition(
            id="prop-strat-ai-expansion",
            title="Adopt Universal Causal Knowledge Mesh for Cross-Tenant Isolation",
            summary="Constitutional upgrade enabling zero-knowledge proof verification across all digital organizations.",
            category="STRATEGIC",
            council_votes={
                "CEO": "APPROVE",
                "VP_ENG": "APPROVE",
                "SECURITY_DIR": "APPROVE",
                "FINANCE_DIR": "APPROVE"
            },
            quorum_met=True,
            enacted=True,
            impact_assessment={"risk": "VERY_LOW", "roi_expected": "5.2x", "cost_usd": 1200.0}
        )
        self._propositions[tenant] = {prop.id: prop}

    def get_propositions(self, tenant_id: str = "default-tenant") -> List[ExecutiveCouncilProposition]:
        return list(self._propositions.get(tenant_id, {}).values())

    def submit_proposition(self, title: str, summary: str, category: str = "STRATEGIC", impact_assessment: Optional[Dict[str, Any]] = None, tenant_id: str = "default-tenant") -> ExecutiveCouncilProposition:
        prop = ExecutiveCouncilProposition(
            tenant_id=tenant_id,
            title=title,
            summary=summary,
            category=category,
            impact_assessment=impact_assessment or {"risk": "LOW", "roi_expected": "3.5x"}
        )
        if tenant_id not in self._propositions:
            self._propositions[tenant_id] = {}
        self._propositions[tenant_id][prop.id] = prop
        return prop

    def vote_on_proposition(self, proposition_id: str, council_role: str, vote: str, tenant_id: str = "default-tenant") -> Optional[ExecutiveCouncilProposition]:
        prop = self._propositions.get(tenant_id, {}).get(proposition_id)
        if not prop:
            return None
        prop.council_votes[council_role] = vote.upper()
        
        # Check quorum (need at least 3 approval votes)
        approvals = sum(1 for v in prop.council_votes.values() if v == "APPROVE")
        if approvals >= 3:
            prop.quorum_met = True
            prop.enacted = True
        return prop

executive_council_engine = ExecutiveCouncilEngine()
