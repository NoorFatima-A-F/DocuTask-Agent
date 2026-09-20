"""
AMAEOP Pillar 1 - Organizational Graph & Reporting Hierarchy
Represents the organization as a directed graph with management, reporting, and cross-team coordination edges.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from app.runtime.organization.department import CANONICAL_DEPARTMENTS, Department


@dataclass
class OrgNode:
    id: str
    label: str
    head_agent: str
    level: int  # 0=Executive, 1=Core Operations, 2=Governance/Quality
    active_workers: int
    queue_depth: int
    health_score: float
    status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OrgEdge:
    source: str
    target: str
    relationship: str  # SUPERVISES | DELEGATES_TO | COORDINATES_WITH | AUDITS | FEEDS_DATA_TO

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class OrganizationGraphBuilder:
    """Constructs the full organizational hierarchy graph and inter-department coordination topology."""

    @classmethod
    def get_organization_graph(cls) -> Dict[str, Any]:
        nodes: List[OrgNode] = []
        for d_id, dept in CANONICAL_DEPARTMENTS.items():
            level = 0 if d_id == "dept_executive" else (2 if d_id in ["dept_governance", "dept_qa"] else 1)
            nodes.append(
                OrgNode(
                    id=dept.department_id,
                    label=dept.name,
                    head_agent=dept.head_agent,
                    level=level,
                    active_workers=dept.active_workers,
                    queue_depth=dept.queue_depth,
                    health_score=dept.health_score,
                    status=dept.status,
                )
            )

        edges: List[OrgEdge] = [
            # Executive Supervisory Hierarchy
            OrgEdge("dept_executive", "dept_ocr", "DELEGATES_TO"),
            OrgEdge("dept_executive", "dept_extraction", "DELEGATES_TO"),
            OrgEdge("dept_executive", "dept_validation", "DELEGATES_TO"),
            OrgEdge("dept_executive", "dept_memory", "DELEGATES_TO"),
            OrgEdge("dept_executive", "dept_research", "DELEGATES_TO"),
            OrgEdge("dept_executive", "dept_governance", "SUPERVISES"),
            OrgEdge("dept_executive", "dept_qa", "SUPERVISES"),
            
            # Operational Pipelines & Data Flows
            OrgEdge("dept_ocr", "dept_extraction", "FEEDS_DATA_TO"),
            OrgEdge("dept_extraction", "dept_validation", "FEEDS_DATA_TO"),
            OrgEdge("dept_extraction", "dept_memory", "COORDINATES_WITH"),
            OrgEdge("dept_validation", "dept_governance", "FEEDS_DATA_TO"),
            OrgEdge("dept_research", "dept_extraction", "COORDINATES_WITH"),
            OrgEdge("dept_qa", "dept_validation", "AUDITS"),
            OrgEdge("dept_governance", "dept_executive", "AUDITS"),
        ]

        return {
            "organization_name": "DocuTask Autonomous Enterprise Digital Organization",
            "total_departments": len(nodes),
            "total_active_agents": sum(n.active_workers for n in nodes),
            "nodes": [n.to_dict() for n in nodes],
            "edges": [e.to_dict() for e in edges],
            "reporting_root": "dept_executive",
        }
