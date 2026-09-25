"""
Phase 13.20: Agent Version Control System (AVCS).
Git-like semantic version control, configuration snapshots, changelogs, and instant rollbacks.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid
from app.platform_ai_lifecycle.models.schemas import AgentVersion


class AgentVersionControlService:
    def __init__(self):
        self._versions: Dict[str, List[AgentVersion]] = {}
        self._seed_default_versions()

    def _seed_default_versions(self) -> None:
        v1 = AgentVersion(
            version_id="ver_01",
            agent_id="agt_acme_invoice_reconciler",
            version_tag="1.0.0",
            model_family="gemini-pro",
            system_prompt="You are an autonomous invoice reconciliation agent. Match lines with POs.",
            tools=["tool_erp_lookup", "tool_ocr_extract"],
            connectors=["conn_acme_sap"],
            changelog="Initial release with 2-way matching",
            accuracy_score=0.91,
            cost_per_execution_usd=0.005,
        )
        v2 = AgentVersion(
            version_id="ver_02",
            agent_id="agt_acme_invoice_reconciler",
            version_tag="1.1.0",
            model_family="gemini-pro",
            system_prompt="You are an advanced autonomous 3-way invoice reconciliation agent.",
            tools=["tool_erp_lookup", "tool_ocr_extract", "tool_bank_statement_verify"],
            connectors=["conn_acme_sap", "conn_acme_gdrive"],
            changelog="Added bank statement 3-way matching and improved precision",
            accuracy_score=0.96,
            cost_per_execution_usd=0.0042,
        )
        v3 = AgentVersion(
            version_id="ver_03",
            agent_id="agt_acme_invoice_reconciler",
            version_tag="1.2.0",
            model_family="gemini-flash",
            system_prompt="Optimized prompt for high-throughput invoice reconciliation.",
            tools=["tool_erp_lookup", "tool_ocr_extract", "tool_bank_statement_verify"],
            connectors=["conn_acme_sap", "conn_acme_gdrive"],
            changelog="Model routing to flash, 35% cost reduction",
            accuracy_score=0.97,
            cost_per_execution_usd=0.0028,
        )
        self._versions["agt_acme_invoice_reconciler"] = [v1, v2, v3]

    def create_version(
        self,
        agent_id: str,
        version_tag: str,
        system_prompt: str,
        tools: List[str],
        connectors: List[str],
        model_family: str = "gemini-pro",
        changelog: str = "",
        accuracy_score: float = 0.95,
        cost_per_execution_usd: float = 0.004,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> AgentVersion:
        version_id = f"ver_{uuid.uuid4().hex[:8]}"
        ver = AgentVersion(
            version_id=version_id,
            agent_id=agent_id,
            version_tag=version_tag,
            model_family=model_family,
            system_prompt=system_prompt,
            tools=tools,
            connectors=connectors,
            parameters=parameters or {},
            changelog=changelog,
            accuracy_score=accuracy_score,
            cost_per_execution_usd=cost_per_execution_usd,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        if agent_id not in self._versions:
            self._versions[agent_id] = []
        self._versions[agent_id].append(ver)
        return ver

    def get_version(self, agent_id: str, version_tag: str) -> Optional[AgentVersion]:
        for ver in self._versions.get(agent_id, []):
            if ver.version_tag == version_tag:
                return ver
        return None

    def list_versions(self, agent_id: str) -> List[AgentVersion]:
        return self._versions.get(agent_id, [])

    def rollback_to_version(self, agent_id: str, target_version_tag: str) -> AgentVersion:
        target = self.get_version(agent_id, target_version_tag)
        if not target:
            raise ValueError(f"Version {target_version_tag} not found for agent {agent_id}")
        return target
