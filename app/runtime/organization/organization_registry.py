"""
AMAEOP Pillar 1 - Organization Registry
Central registry mapping organizational department capabilities, roles, and agent rosters.
"""

from typing import Dict, List, Any, Optional
from app.runtime.organization.department import CANONICAL_DEPARTMENTS, Department


class OrganizationRegistry:
    """Central registry of departments, agent roles, and organizational capabilities."""

    @classmethod
    def get_all_capabilities(cls) -> Dict[str, List[str]]:
        capabilities = {}
        for d_id, dept in CANONICAL_DEPARTMENTS.items():
            capabilities[d_id] = dept.responsibilities
        return capabilities

    @classmethod
    def find_department_for_capability(cls, capability_keyword: str) -> Optional[str]:
        kw = capability_keyword.lower()
        for d_id, dept in CANONICAL_DEPARTMENTS.items():
            for resp in dept.responsibilities:
                if kw in resp.lower():
                    return d_id
        return None

    @classmethod
    def get_agent_roster(cls) -> List[Dict[str, Any]]:
        roster = []
        for dept in CANONICAL_DEPARTMENTS.values():
            roster.append({
                "agent_title": dept.head_agent,
                "department_id": dept.department_id,
                "department_name": dept.name,
                "active_workers": dept.active_workers,
                "concurrency_limit": dept.concurrency_limit,
                "status": dept.status,
            })
        return roster
