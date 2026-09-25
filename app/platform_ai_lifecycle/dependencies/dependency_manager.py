"""
Phase 13.20: Agent Dependency DAG Manager.
Tracks and validates dependencies (Tools, Models, Connectors, Datasets, Policies) and flags breaking changes.
"""

from typing import Dict, List, Any
import uuid
from app.platform_ai_lifecycle.models.schemas import AgentDependency


class AgentDependencyManager:
    def __init__(self):
        self._dependencies: Dict[str, List[AgentDependency]] = {}
        self._seed_default_dependencies()

    def _seed_default_dependencies(self) -> None:
        d1 = AgentDependency(
            dep_id="dep_01",
            agent_id="agt_acme_invoice_reconciler",
            dependency_type="TOOL",
            target_resource_id="tool_erp_lookup",
            target_resource_name="SAP S/4HANA PO Query Tool",
        )
        d2 = AgentDependency(
            dep_id="dep_02",
            agent_id="agt_acme_invoice_reconciler",
            dependency_type="MODEL",
            target_resource_id="model_gemini_flash",
            target_resource_name="Gemini 1.5 Flash High-Throughput",
        )
        d3 = AgentDependency(
            dep_id="dep_03",
            agent_id="agt_acme_invoice_reconciler",
            dependency_type="CONNECTOR",
            target_resource_id="conn_acme_sap",
            target_resource_name="Acme SAP S/4HANA ERP Bridge",
        )
        self._dependencies["agt_acme_invoice_reconciler"] = [d1, d2, d3]

    def add_dependency(
        self,
        agent_id: str,
        dependency_type: str,
        target_resource_id: str,
        target_resource_name: str,
        is_breaking_change: bool = False,
    ) -> AgentDependency:
        dep = AgentDependency(
            dep_id=f"dep_{uuid.uuid4().hex[:8]}",
            agent_id=agent_id,
            dependency_type=dependency_type,
            target_resource_id=target_resource_id,
            target_resource_name=target_resource_name,
            is_breaking_change=is_breaking_change,
        )
        if agent_id not in self._dependencies:
            self._dependencies[agent_id] = []
        self._dependencies[agent_id].append(dep)
        return dep

    def list_dependencies(self, agent_id: str) -> List[AgentDependency]:
        return self._dependencies.get(agent_id, [])

    def validate_dependency_graph(self, agent_id: str) -> Dict[str, Any]:
        deps = self.list_dependencies(agent_id)
        breaking = [d for d in deps if d.is_breaking_change]
        return {
            "agent_id": agent_id,
            "total_dependencies": len(deps),
            "breaking_changes_count": len(breaking),
            "healthy": len(breaking) == 0,
            "status": "VALID" if len(breaking) == 0 else "WARNING_BREAKING_CHANGES",
        }
