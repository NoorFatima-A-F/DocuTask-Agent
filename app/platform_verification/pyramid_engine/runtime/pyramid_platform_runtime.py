"""
Unified Enterprise Verification Pyramid Platform Runtime Facade.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.platform_verification.pyramid_engine.domain.models import (
    VerificationLevel,
    TestDefinition,
    ContinuousTrigger,
    PyramidExecutionReport,
    PyramidDashboardSummary,
    DefectRecord,
    RegressionRecord,
    ComponentCoverageItem,
    FailureSeverity,
)
from app.platform_verification.pyramid_engine.core.maturity_engine import MaturityEngine
from app.platform_verification.pyramid_engine.core.dependency_graph import DependencyGate
from app.platform_verification.pyramid_engine.core.failure_manager import FailureManager
from app.platform_verification.pyramid_engine.core.regression_engine import RegressionEngine
from app.platform_verification.pyramid_engine.core.dashboard import PyramidDashboard
from app.platform_verification.pyramid_engine.core.orchestrator import PyramidOrchestrator


class PyramidPlatformRuntime:
    """Unified runtime facade orchestrating maturity models, dependency gates, regressions, and pyramid runs."""

    def __init__(self) -> None:
        self.maturity_engine = MaturityEngine()
        self.dependency_gate = DependencyGate()
        self.failure_manager = FailureManager()
        self.regression_engine = RegressionEngine()
        self.dashboard = PyramidDashboard()
        self.orchestrator = PyramidOrchestrator(
            gate=self.dependency_gate,
            failure_manager=self.failure_manager,
        )
        self._execution_history: List[PyramidExecutionReport] = []

    def run_pyramid_verification(
        self,
        system_version: str,
        trigger: ContinuousTrigger,
        tests: List[TestDefinition],
        context: Optional[Dict[str, Any]] = None,
    ) -> PyramidExecutionReport:
        """Executes verification tests through the pyramid for the specified trigger."""
        report = self.orchestrator.execute_pyramid(
            system_version=system_version,
            trigger=trigger,
            tests=tests,
            context=context,
        )
        self._execution_history.append(report)

        # Update component maturity for successful runs
        if report.overall_status == report.overall_status.PASSED:
            for level, summary in report.level_summaries.items():
                if summary.status == summary.status.PASSED:
                    for r in summary.records:
                        comp_name = r.name.split("_")[0] if "_" in r.name else "platform_core"
                        if comp_name in [c.component_name for c in self.maturity_engine.list_all_components()]:
                            self.maturity_engine.update_component_maturity(comp_name, level, is_verified=True)

        return report

    def get_dashboard_summary(self) -> PyramidDashboardSummary:
        """Computes live verification maturity, defect backlog, and risk metrics."""
        components = self.maturity_engine.list_all_components()
        defects = self.failure_manager.list_defects()
        return self.dashboard.generate_summary(components, defects, self._execution_history)

    def register_fixed_defect_as_regression(self, defect: DefectRecord) -> RegressionRecord:
        """Converts a fixed defect into a permanent regression safeguard."""
        return self.regression_engine.register_defect(defect)
