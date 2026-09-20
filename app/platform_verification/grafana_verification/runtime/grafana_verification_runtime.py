"""Grafana Verification Runtime.

Coordinates full end-to-end operational dashboard verification pipeline across all 12 sub-phases.
"""

from typing import Dict, Any, Tuple
from ..domain.models import (
    ConfigurationReport,
    ProvisioningReport,
    DashboardValidationReport,
    UsabilityAuditReport,
    PerformanceBenchmarkReport,
    SecurityAuditReport,
    OperationalDashboardScorecard,
)
from ..verifiers.grafana_configuration_verifier import GrafanaConfigurationVerifier
from ..verifiers.dashboard_provisioning_verifier import DashboardProvisioningVerifier
from ..verifiers.system_health_verifier import SystemHealthDashboardVerifier
from ..verifiers.ai_processing_verifier import AIProcessingDashboardVerifier
from ..verifiers.agent_runtime_verifier import AgentRuntimeDashboardVerifier
from ..verifiers.infrastructure_verifier import InfrastructureDashboardVerifier
from ..verifiers.incident_dashboard_verifier import IncidentDashboardVerifier
from ..usability.dashboard_usability_verifier import DashboardUsabilityVerifier
from ..performance.dashboard_performance_verifier import DashboardPerformanceVerifier
from ..security.dashboard_security_auditor import DashboardSecurityAuditor
from ..scoring.dashboard_quality_scorer import DashboardQualityScorer
from ..exporter.grafana_evidence_exporter import GrafanaEvidenceExporter


class GrafanaVerificationRuntime:
    """Runtime coordinator executing all 12 validation steps."""

    def __init__(self, output_dir: str = "grafana_verification"):
        self.config_verifier = GrafanaConfigurationVerifier()
        self.provisioning_verifier = DashboardProvisioningVerifier()
        self.system_verifier = SystemHealthDashboardVerifier()
        self.ai_verifier = AIProcessingDashboardVerifier()
        self.agent_verifier = AgentRuntimeDashboardVerifier()
        self.infra_verifier = InfrastructureDashboardVerifier()
        self.incident_verifier = IncidentDashboardVerifier()
        self.usability_verifier = DashboardUsabilityVerifier()
        self.performance_verifier = DashboardPerformanceVerifier()
        self.security_auditor = DashboardSecurityAuditor()
        self.scorer = DashboardQualityScorer()
        self.exporter = GrafanaEvidenceExporter(output_dir=output_dir)

    def execute_full_verification(self) -> Tuple[OperationalDashboardScorecard, Dict[str, str]]:
        # 1. Configuration
        config_rep = self.config_verifier.verify_configuration()

        # 2. Provisioning
        prov_rep = self.provisioning_verifier.verify_provisioning()

        # 3. System Health
        sys_rep = self.system_verifier.verify_dashboard()

        # 4. AI Processing
        ai_rep = self.ai_verifier.verify_dashboard()

        # 5. Agent Runtime
        agent_rep = self.agent_verifier.verify_dashboard()

        # 6. Infrastructure
        infra_rep = self.infra_verifier.verify_dashboard()

        # 7. Incident Investigation
        incident_rep = self.incident_verifier.verify_dashboard()

        # 8. Usability Scenarios
        usability_rep = self.usability_verifier.verify_usability()

        # 9. Performance Benchmarks
        perf_rep = self.performance_verifier.verify_performance()

        # 10. Security Audit
        sec_rep = self.security_auditor.audit_security()

        # 11. Scoring
        scorecard = self.scorer.score_dashboards(
            config_rep=config_rep,
            prov_rep=prov_rep,
            system_rep=sys_rep,
            ai_rep=ai_rep,
            agent_rep=agent_rep,
            infra_rep=infra_rep,
            incident_rep=incident_rep,
            usability_rep=usability_rep,
            perf_rep=perf_rep,
            sec_rep=sec_rep,
        )

        # 12. Evidence Export
        exported_manifests = self.exporter.export_all(
            config_rep=config_rep,
            prov_rep=prov_rep,
            system_rep=sys_rep,
            ai_rep=ai_rep,
            agent_rep=agent_rep,
            infra_rep=infra_rep,
            incident_rep=incident_rep,
            usability_rep=usability_rep,
            perf_rep=perf_rep,
            sec_rep=sec_rep,
            scorecard=scorecard,
        )

        return scorecard, exported_manifests
