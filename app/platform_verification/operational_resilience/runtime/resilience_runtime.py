"""
Operational Resilience Runtime Engine (Part 3G.5).
Master orchestrator that executes failure experiments, self-healing audits,
incident automation, runbook verification, dependency resilience checks,
state consistency validation, DR drills, scorecard computation, and evidence export.
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

from app.platform_verification.operational_resilience.domain.models import (
    FailureExperimentResult,
    SelfHealingReport,
    IncidentAutomationReport,
    RunbookValidationReport,
    DependencyResilienceReport,
    StateConsistencyReport,
    DrillResult,
    OperationalResilienceScorecard,
)
from app.platform_verification.operational_resilience.failure_injection.failure_injector import (
    FailureInjector,
)
from app.platform_verification.operational_resilience.self_healing.self_healing_engine import (
    SelfHealingEngine,
)
from app.platform_verification.operational_resilience.orchestrator.recovery_orchestrator import (
    RecoveryOrchestrator,
)
from app.platform_verification.operational_resilience.incident_automation.incident_automation_engine import (
    IncidentAutomationEngine,
)
from app.platform_verification.operational_resilience.runbooks.runbook_engine import (
    RunbookEngine,
)
from app.platform_verification.operational_resilience.dependency_resilience.dependency_resilience_manager import (
    DependencyResilienceManager,
)
from app.platform_verification.operational_resilience.state_consistency.state_consistency_verifier import (
    StateConsistencyVerifier,
)
from app.platform_verification.operational_resilience.drill_system.drill_scheduler import (
    DrillScheduler,
)
from app.platform_verification.operational_resilience.scoring.resilience_score_engine import (
    ResilienceScoreEngine,
)
from app.platform_verification.operational_resilience.exporter.evidence_exporter import (
    EvidenceExporter,
)


@dataclass
class MasterResilienceExecutionResult:
    experiments: List[FailureExperimentResult]
    self_healing: SelfHealingReport
    orchestrator_report: Dict[str, Any]
    incidents: IncidentAutomationReport
    runbooks: RunbookValidationReport
    dependencies: DependencyResilienceReport
    consistency: StateConsistencyReport
    drill: DrillResult
    scorecard: OperationalResilienceScorecard
    export_result: Dict[str, Any]
    passed: bool


class ResilienceRuntime:
    """
    Master runtime for Part 3G.5 Operational Resilience & Recovery Automation.
    """

    def __init__(self, base_dir: str = ".", output_dir_name: str = "resilience_verification"):
        self.base_dir = base_dir
        self.failure_injector = FailureInjector()
        self.self_healing_engine = SelfHealingEngine()
        self.recovery_orchestrator = RecoveryOrchestrator()
        self.incident_engine = IncidentAutomationEngine()
        self.runbook_engine = RunbookEngine()
        self.dependency_manager = DependencyResilienceManager()
        self.consistency_verifier = StateConsistencyVerifier()
        self.drill_scheduler = DrillScheduler()
        self.score_engine = ResilienceScoreEngine()
        self.exporter = EvidenceExporter(base_dir=base_dir, output_dir_name=output_dir_name)

    def execute_resilience_verification(self, export_artifacts: bool = True) -> MasterResilienceExecutionResult:
        """
        Executes the full suite of operational resilience verification components.
        """
        # 1. Failure Experiments (Part 3G.5C)
        experiments = self.failure_injector.run_all_failure_experiments()

        # 2. Self-Healing System (Part 3G.5B)
        self_healing = self.self_healing_engine.verify_self_healing()

        # 3. Recovery Orchestration (Part 3G.5A)
        orchestrator_report = self.recovery_orchestrator.verify_recovery_workflows()

        # 4. Incident Automation (Part 3G.5D)
        incidents = self.incident_engine.verify_incident_automation()

        # 5. Runbook Automation (Part 3G.5E)
        runbooks = self.runbook_engine.validate_runbooks()

        # 6. Dependency Resilience (Part 3G.5F)
        dependencies = self.dependency_manager.verify_dependency_resilience()

        # 7. State Consistency & Idempotency (Part 3G.5G)
        consistency = self.consistency_verifier.verify_state_consistency()

        # 8. DR Drill System (Part 3G.5H)
        drill = self.drill_scheduler.execute_resilience_drill(0)

        # 9. Resilience Scoring (Part 3G.5I)
        scorecard = self.score_engine.calculate_scorecard(
            experiments=experiments,
            self_healing=self_healing,
            incidents=incidents,
            runbooks=runbooks,
            dependencies=dependencies,
            consistency=consistency,
            drill=drill,
        )

        passed = (
            scorecard.passed
            and self_healing.passed
            and orchestrator_report.get("all_workflows_passed", False)
            and incidents.passed
            and runbooks.passed
            and dependencies.passed
            and consistency.passed
            and drill.passed
        )

        # 10. Export Evidence (Part 3G.5J)
        export_result = {}
        if export_artifacts:
            export_result = self.exporter.export_all_evidence(
                experiments=experiments,
                self_healing=self_healing,
                orchestrator_report=orchestrator_report,
                incidents=incidents,
                runbooks=runbooks,
                dependencies=dependencies,
                consistency=consistency,
                drill=drill,
                scorecard=scorecard,
            )

        return MasterResilienceExecutionResult(
            experiments=experiments,
            self_healing=self_healing,
            orchestrator_report=orchestrator_report,
            incidents=incidents,
            runbooks=runbooks,
            dependencies=dependencies,
            consistency=consistency,
            drill=drill,
            scorecard=scorecard,
            export_result=export_result,
            passed=passed,
        )
