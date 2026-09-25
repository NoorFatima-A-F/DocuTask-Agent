"""
Phase 13.20: Master AI Application Lifecycle Orchestrator.
Coordinates the end-to-end agent development, testing, security, approval, deployment, and retirement lifecycle.
"""

from typing import Dict, List, Any
from app.platform_ai_lifecycle.registry.agent_registry_service import AgentRegistryService
from app.platform_ai_lifecycle.versioning.agent_version_control import AgentVersionControlService
from app.platform_ai_lifecycle.testing.ai_testing_engine import AITestingEngine
from app.platform_ai_lifecycle.security.security_scanner import AgentSecurityScanner
from app.platform_ai_lifecycle.approval.approval_workflow_engine import ApprovalWorkflowEngine
from app.platform_ai_lifecycle.deployment.deployment_manager import AIDeploymentManager
from app.platform_ai_lifecycle.dependencies.dependency_manager import AgentDependencyManager
from app.platform_ai_lifecycle.templates.template_catalog_service import TemplateCatalogService
from app.platform_ai_lifecycle.marketplace.lifecycle_marketplace_service import LifecycleMarketplaceService
from app.platform_ai_lifecycle.analytics.lifecycle_analytics_engine import LifecycleAnalyticsEngine
from app.platform_ai_lifecycle.retirement.agent_retirement_service import AgentRetirementService
from app.platform_ai_lifecycle.governance.lifecycle_governance_service import LifecycleGovernanceService
from app.platform_ai_lifecycle.models.schemas import (
    AgentLifecycleState,
    AgentCategory,
    ApprovalStage,
    ApprovalDecision,
    DeploymentEnvironment,
    DeploymentStrategy,
    LifecycleOverview,
)


class LifecycleMasterOrchestrator:
    def __init__(self):
        self.registry = AgentRegistryService()
        self.versioning = AgentVersionControlService()
        self.testing = AITestingEngine()
        self.security = AgentSecurityScanner()
        self.approvals = ApprovalWorkflowEngine()
        self.deployment = AIDeploymentManager()
        self.dependencies = AgentDependencyManager()
        self.templates = TemplateCatalogService()
        self.marketplace = LifecycleMarketplaceService()
        self.analytics = LifecycleAnalyticsEngine()
        self.retirement = AgentRetirementService()
        self.governance = LifecycleGovernanceService()

    def get_overview(self) -> LifecycleOverview:
        agents = self.registry.list_agents()
        deployed = len([a for a in agents if a.lifecycle_state == AgentLifecycleState.DEPLOYED])
        in_review = len([a for a in agents if a.lifecycle_state in (AgentLifecycleState.TESTING, AgentLifecycleState.SECURITY_REVIEW, AgentLifecycleState.DEVELOPMENT)])
        retired = len([a for a in agents if a.lifecycle_state in (AgentLifecycleState.DEPRECATED, AgentLifecycleState.RETIRED)])
        return self.analytics.compute_overview(
            total_agents=len(agents),
            deployed_agents=deployed,
            in_review=in_review,
            retired=retired,
        )

    def full_lifecycle_release(
        self,
        tenant_id: str,
        organization_id: str,
        workspace_id: str,
        name: str,
        slug: str,
        category: AgentCategory,
        owner_id: str,
        owner_email: str,
        system_prompt: str,
        tools: List[str],
        connectors: List[str],
    ) -> Dict[str, Any]:
        """Executes a complete automated DevSecOps release lifecycle pipeline."""
        # 1. Register agent
        agent = self.registry.register_agent(
            tenant_id=tenant_id,
            organization_id=organization_id,
            workspace_id=workspace_id,
            name=name,
            slug=slug,
            category=category,
            owner_id=owner_id,
            owner_email=owner_email,
            description=f"Automated release for {name}",
        )
        
        # 2. Commit Version v1.0.0
        version = self.versioning.create_version(
            agent_id=agent.agent_id,
            version_tag="1.0.0",
            system_prompt=system_prompt,
            tools=tools,
            connectors=connectors,
            changelog="Automated production release pipeline",
        )
        
        # 3. Run Testing Harness
        self.registry.update_lifecycle_state(agent.agent_id, AgentLifecycleState.TESTING)
        test_res = self.testing.run_comprehensive_test_suite(agent.agent_id, version.version_tag)
        
        # 4. Security Scan
        self.registry.update_lifecycle_state(agent.agent_id, AgentLifecycleState.SECURITY_REVIEW)
        sec_res = self.security.scan_agent_version(agent.agent_id, version.version_tag, system_prompt, tools)
        
        # 5. Submit and auto-approve if test & security pass
        appr = self.approvals.submit_for_approval(agent.agent_id, version.version_tag, owner_id, owner_email)
        if test_res.status == "PASSED" and sec_res.security_score >= 80:
            appr = self.approvals.review_and_decide(
                approval_id=appr.approval_id,
                stage=ApprovalStage.FINAL_RELEASE,
                decision=ApprovalDecision.APPROVED,
                approver_id="usr_system_governor",
                approver_email="governor@aiplatform.internal",
                comments="Automated CI/CD security and quality thresholds satisfied.",
            )
            self.registry.update_lifecycle_state(agent.agent_id, AgentLifecycleState.APPROVED)
        
        # 6. Deploy to Production
        deploy_res = self.deployment.deploy_agent_version(
            agent_id=agent.agent_id,
            version_tag=version.version_tag,
            environment=DeploymentEnvironment.PRODUCTION,
            strategy=DeploymentStrategy.CANARY,
            traffic_weight_pct=100,
        )
        self.registry.update_lifecycle_state(agent.agent_id, AgentLifecycleState.DEPLOYED)
        
        # 7. Audit log
        self.governance.log_lifecycle_audit_event(
            tenant_id=tenant_id,
            agent_id=agent.agent_id,
            action="FULL_LIFECYCLE_RELEASE_SUCCESS",
            actor_id=owner_id,
            actor_email=owner_email,
        )

        return {
            "agent": agent,
            "version": version,
            "test_result": test_res,
            "security_scan": sec_res,
            "approval": appr,
            "deployment": deploy_res,
            "status": "RELEASE_SUCCESSFUL",
        }
