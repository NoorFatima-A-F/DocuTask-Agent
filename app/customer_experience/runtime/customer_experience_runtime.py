"""Master Synchronous Runtime for Phase 7 Customer Experience Simulation."""

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
import uuid

from app.core.security import resolve_safe_path, validate_safe_filename_segment
from ..analytics.customer_analytics_engine import CustomerAnalyticsEngine
from ..approvals.approval_center_engine import ApprovalCenterEngine
from ..connectors.connector_manager import ConnectorManager
from ..demo_engine.interactive_demo_engine import InteractiveDemoEngine
from ..domain.interfaces import ICustomerExperienceRuntime
from ..onboarding.customer_onboarding_engine import CustomerOnboardingEngine
from ..portfolio_generator.portfolio_presentation_generator import PortfolioPresentationGenerator
from ..templates.template_marketplace import TemplateMarketplace
from ..tenant_demo.tenant_simulation_engine import TenantSimulationEngine
from ..trust_center.trust_center_engine import TrustCenterEngine
from ..workflow_builder.workflow_builder_engine import WorkflowBuilderEngine


class CustomerExperienceRuntime(ICustomerExperienceRuntime):
    """Coordinates all enterprise customer simulation engines and produces publication-ready evidence."""

    DEFAULT_OUTPUT_DIR = "customer_experience_evidence"

    def __init__(self):
        self.tenant_engine = TenantSimulationEngine()
        self.onboarding_engine = CustomerOnboardingEngine()
        self.template_marketplace = TemplateMarketplace()
        self.workflow_builder = WorkflowBuilderEngine()
        self.connector_manager = ConnectorManager()
        self.approval_engine = ApprovalCenterEngine()
        self.analytics_engine = CustomerAnalyticsEngine()
        self.trust_center = TrustCenterEngine()
        self.demo_engine = InteractiveDemoEngine()
        self.portfolio_generator = PortfolioPresentationGenerator()

    def run_full_simulation(self, output_dir: Optional[str] = None) -> Dict[str, Any]:
        target_dir = resolve_safe_path(Path.cwd(), output_dir or self.DEFAULT_OUTPUT_DIR)
        target_dir.mkdir(parents=True, exist_ok=True)

        simulation_id = f"SIM-RUN-{uuid.uuid4().hex[:8].upper()}"

        # 1. Tenants
        tenants = self.tenant_engine.list_tenants()
        isolation_ok = self.tenant_engine.verify_tenant_isolation("TENANT-FIN-01", "TENANT-HLT-02")

        # 2. Onboarding Simulation
        journey = self.onboarding_engine.start_onboarding("Acme Logistics Corp", "Finance & Banking")
        for i in range(1, 8):
            self.onboarding_engine.advance_step(journey.journey_id, {"step_completed": i, "verified": True})
        completed_journey = self.onboarding_engine.get_journey(journey.journey_id)

        # 3. Templates
        templates = self.template_marketplace.list_templates()

        # 4. Workflow execution
        wf_result = self.workflow_builder.execute_workflow("WF-DEFAULT-INVOICE", {"tenant_id": "TENANT-FIN-01"})

        # 5. Connectors
        connectors = self.connector_manager.list_connectors()
        conn_pings = {c.connector_id: self.connector_manager.test_connection(c.connector_id) for c in connectors[:3]}

        # 6. Approvals & Exceptions
        approvals = self.approval_engine.get_pending_approvals()
        decided = self.approval_engine.submit_decision("APP-2026-001", "APPROVE", "Fast-tracked by AI supervisor")
        exceptions = self.approval_engine.list_exceptions()

        # 7. Analytics
        analytics = self.analytics_engine.generate_analytics_report("TENANT-FIN-01")

        # 8. Trust Center
        trust_report = self.trust_center.get_trust_report()

        # 9. Interactive Demo Run
        demo_run = self.demo_engine.run_demo_scenario("invoice_automation")

        # 10. Portfolio Artifacts Generation
        portfolio_artifacts = self.portfolio_generator.generate_portfolio_artifacts(output_dir=target_dir)

        # Build Full Report
        summary_payload = {
            "simulation_id": simulation_id,
            "project_name": "DocuTask Agent",
            "phase": "Phase 7 - Enterprise AI Automation Experience & Customer Simulation Platform",
            "status": "ENTERPRISE_DEMO_READY",
            "tenant_simulation": {
                "total_tenants": len(tenants),
                "isolation_verified": isolation_ok,
                "tenants": [t.model_dump() for t in tenants],
            },
            "onboarding_simulation": completed_journey.model_dump() if completed_journey else {},
            "template_marketplace": {
                "total_templates": len(templates),
                "templates": [t.model_dump() for t in templates],
            },
            "workflow_execution": wf_result.model_dump(),
            "connectors": {
                "total_connectors": len(connectors),
                "active_connections": len([c for c in connectors if c.status.value == "CONNECTED"]),
                "diagnostic_pings": conn_pings,
            },
            "human_in_the_loop": {
                "pending_approvals_count": len(approvals),
                "sample_approval": decided.model_dump(),
                "exceptions_count": len(exceptions),
            },
            "customer_analytics": analytics.model_dump(),
            "trust_center": trust_report.model_dump(),
            "interactive_demo_result": demo_run.model_dump(),
            "portfolio_artifacts_count": len(portfolio_artifacts.case_studies) + len(portfolio_artifacts.demo_scripts) + 1,
        }

        # Export JSON files
        showcase_path = resolve_safe_path(target_dir, "customer_simulation_showcase.json")
        with open(showcase_path, "w", encoding="utf-8") as f:
            json.dump(summary_payload, f, indent=2, default=str)

        # Export SHA-256 manifest
        manifest = {}
        for fname in os.listdir(target_dir):
            safe_fname = validate_safe_filename_segment(fname)
            fpath = resolve_safe_path(target_dir, safe_fname)
            if fpath.is_file():
                with open(fpath, "rb") as f:
                    manifest[safe_fname] = {
                        "sha256": hashlib.sha256(f.read()).hexdigest(),
                        "size_bytes": fpath.stat().st_size,
                    }

        manifest_path = resolve_safe_path(target_dir, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return summary_payload
