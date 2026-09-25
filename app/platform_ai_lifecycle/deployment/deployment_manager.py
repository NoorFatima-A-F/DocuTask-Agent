"""
Phase 13.20: AI Deployment Manager.
Orchestrates staging, blue-green, and canary rollouts into the Phase 13.18 Distributed Cloud Runtime.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid
from app.platform_ai_lifecycle.models.schemas import (
    AgentDeployment,
    DeploymentEnvironment,
    DeploymentStrategy,
    DeploymentStatus,
)


class AIDeploymentManager:
    def __init__(self):
        self._deployments: Dict[str, List[AgentDeployment]] = {}
        self._seed_default_deployments()

    def _seed_default_deployments(self) -> None:
        d1 = AgentDeployment(
            deployment_id="dep_01",
            agent_id="agt_acme_invoice_reconciler",
            version_tag="1.2.0",
            environment=DeploymentEnvironment.PRODUCTION,
            strategy=DeploymentStrategy.CANARY,
            traffic_weight_pct=100,
            status=DeploymentStatus.PRODUCTION,
            distributed_cluster_id="cluster_us_east_primary",
            active_instances_count=8,
        )
        self._deployments["agt_acme_invoice_reconciler"] = [d1]

    def deploy_agent_version(
        self,
        agent_id: str,
        version_tag: str,
        environment: DeploymentEnvironment = DeploymentEnvironment.PRODUCTION,
        strategy: DeploymentStrategy = DeploymentStrategy.CANARY,
        traffic_weight_pct: int = 100,
        cluster_id: str = "cluster_us_east_primary",
    ) -> AgentDeployment:
        dep_id = f"dep_{uuid.uuid4().hex[:8]}"
        dep = AgentDeployment(
            deployment_id=dep_id,
            agent_id=agent_id,
            version_tag=version_tag,
            environment=environment,
            strategy=strategy,
            traffic_weight_pct=traffic_weight_pct,
            status=DeploymentStatus.PRODUCTION,
            distributed_cluster_id=cluster_id,
            active_instances_count=4 if environment == DeploymentEnvironment.PRODUCTION else 1,
            deployed_at=datetime.now(timezone.utc).isoformat(),
        )
        if agent_id not in self._deployments:
            self._deployments[agent_id] = []
        self._deployments[agent_id].append(dep)
        return dep

    def list_deployments(self, agent_id: Optional[str] = None) -> List[AgentDeployment]:
        if agent_id:
            return self._deployments.get(agent_id, [])
        all_deps = []
        for deps in self._deployments.values():
            all_deps.extend(deps)
        return all_deps
