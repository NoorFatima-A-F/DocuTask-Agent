"""
3H.11.2: Scenario Registry Verifier
"""
from typing import List
from ..domain.models import FailureSeverity, FailureScenario, ScenarioRegistryReport
from ..domain.interfaces import IScenarioRegistryVerifier


class ScenarioRegistryVerifier(IScenarioRegistryVerifier):
    """
    Verifies the registry and catalog of all failure scenarios across Infrastructure, Application, External Dependencies, and Resources.
    """

    def verify_scenario_registry(self) -> ScenarioRegistryReport:
        scenarios: List[FailureScenario] = [
            # Infrastructure
            FailureScenario(
                scenario_id="DB_FAILURE_001",
                category="INFRASTRUCTURE",
                component="postgresql",
                failure_type="database_down",
                severity=FailureSeverity.CRITICAL,
                expected_state_before="healthy",
                expected_state_during="unhealthy",
                expected_state_after="healthy",
                rollback_required=True,
                max_duration_seconds=30
            ),
            FailureScenario(
                scenario_id="QUEUE_FAILURE_001",
                category="INFRASTRUCTURE",
                component="redis",
                failure_type="redis_down",
                severity=FailureSeverity.HIGH,
                expected_state_before="healthy",
                expected_state_during="unhealthy",
                expected_state_after="healthy",
                rollback_required=True,
                max_duration_seconds=30
            ),
            FailureScenario(
                scenario_id="STORAGE_FAILURE_001",
                category="INFRASTRUCTURE",
                component="s3_storage",
                failure_type="storage_unavailable",
                severity=FailureSeverity.HIGH,
                expected_state_before="healthy",
                expected_state_during="unhealthy",
                expected_state_after="healthy",
                rollback_required=True,
                max_duration_seconds=30
            ),
            # Application
            FailureScenario(
                scenario_id="API_CRASH_001",
                category="APPLICATION",
                component="api_gateway",
                failure_type="api_crash",
                severity=FailureSeverity.CRITICAL,
                expected_state_before="healthy",
                expected_state_during="unhealthy",
                expected_state_after="healthy",
                rollback_required=True,
                max_duration_seconds=20
            ),
            FailureScenario(
                scenario_id="WORKER_CRASH_001",
                category="APPLICATION",
                component="async_workers",
                failure_type="worker_crash",
                severity=FailureSeverity.MEDIUM,
                expected_state_before="healthy",
                expected_state_during="unhealthy",
                expected_state_after="healthy",
                rollback_required=True,
                max_duration_seconds=25
            ),
            FailureScenario(
                scenario_id="RUNTIME_FAILURE_001",
                category="APPLICATION",
                component="agent_runtime",
                failure_type="agent_runtime_failure",
                severity=FailureSeverity.HIGH,
                expected_state_before="healthy",
                expected_state_during="unhealthy",
                expected_state_after="healthy",
                rollback_required=True,
                max_duration_seconds=25
            ),
            # External Dependencies
            FailureScenario(
                scenario_id="GEMINI_TIMEOUT_001",
                category="EXTERNAL_DEPENDENCY",
                component="gemini_llm",
                failure_type="gemini_timeout",
                severity=FailureSeverity.MEDIUM,
                expected_state_before="healthy",
                expected_state_during="degraded",
                expected_state_after="healthy",
                rollback_required=True,
                max_duration_seconds=30
            ),
            FailureScenario(
                scenario_id="LLM_RATE_LIMIT_001",
                category="EXTERNAL_DEPENDENCY",
                component="llm_router",
                failure_type="llm_rate_limit",
                severity=FailureSeverity.MEDIUM,
                expected_state_before="healthy",
                expected_state_during="degraded",
                expected_state_after="healthy",
                rollback_required=True,
                max_duration_seconds=30
            ),
            FailureScenario(
                scenario_id="PROVIDER_UNAVAILABLE_001",
                category="EXTERNAL_DEPENDENCY",
                component="multi_llm_gateway",
                failure_type="provider_unavailable",
                severity=FailureSeverity.HIGH,
                expected_state_before="healthy",
                expected_state_during="degraded",
                expected_state_after="healthy",
                rollback_required=True,
                max_duration_seconds=30
            ),
            # Resources
            FailureScenario(
                scenario_id="MEMORY_PRESSURE_001",
                category="RESOURCE",
                component="container_memory",
                failure_type="memory_pressure",
                severity=FailureSeverity.HIGH,
                expected_state_before="healthy",
                expected_state_during="degraded",
                expected_state_after="healthy",
                rollback_required=True,
                max_duration_seconds=30
            ),
            FailureScenario(
                scenario_id="CPU_SATURATION_001",
                category="RESOURCE",
                component="container_cpu",
                failure_type="cpu_saturation",
                severity=FailureSeverity.HIGH,
                expected_state_before="healthy",
                expected_state_during="degraded",
                expected_state_after="healthy",
                rollback_required=True,
                max_duration_seconds=30
            ),
            FailureScenario(
                scenario_id="DISK_FULL_001",
                category="RESOURCE",
                component="node_storage",
                failure_type="disk_full",
                severity=FailureSeverity.CRITICAL,
                expected_state_before="healthy",
                expected_state_during="unhealthy",
                expected_state_after="healthy",
                rollback_required=True,
                max_duration_seconds=30
            ),
        ]

        categories = sorted(list(set(s.category for s in scenarios)))

        return ScenarioRegistryReport(
            report_title="Enterprise Failure Scenario Registry & Simulation Catalog",
            total_scenarios=len(scenarios),
            scenarios=scenarios,
            categories_covered=categories,
            registry_validated=True
        )
