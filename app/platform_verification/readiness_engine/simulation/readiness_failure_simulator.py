"""
Readiness Failure Simulator (Part 3H.3.2.9).
Executes 4 controlled failure injection scenarios to verify dependency-aware decisions:
- Scenario 1: Database shutdown (docker stop postgres) -> NOT_READY, traffic rejected
- Scenario 2: Redis broker failure -> Queue readiness failed -> NOT_READY, traffic rejected
- Scenario 3: Gemini AI API timeout -> Graceful degradation -> DEGRADED, traffic throttled (not hard failure)
- Scenario 4: Storage permission failure -> NOT_READY, traffic rejected
"""
from typing import Dict, Any, List
from app.platform_verification.readiness_engine.domain.models import (
    ReadinessState,
    TrafficAction,
    FailureScenarioResult,
    FailureSimulationReport,
)
from app.platform_verification.readiness_engine.checkers.database_readiness_checker import DatabaseReadinessChecker
from app.platform_verification.readiness_engine.checkers.queue_readiness_checker import QueueReadinessChecker
from app.platform_verification.readiness_engine.checkers.storage_readiness_checker import StorageReadinessChecker
from app.platform_verification.readiness_engine.checkers.ai_readiness_checker import AIProviderReadinessChecker
from app.platform_verification.readiness_engine.checkers.worker_readiness_checker import WorkerReadinessChecker
from app.platform_verification.readiness_engine.aggregator.readiness_evaluator import ReadinessEvaluator


class ReadinessFailureSimulator:
    """
    Executes controlled dependency failure injections and records decision responses.
    """

    def __init__(self):
        self.db_checker = DatabaseReadinessChecker()
        self.queue_checker = QueueReadinessChecker()
        self.storage_checker = StorageReadinessChecker()
        self.ai_checker = AIProviderReadinessChecker()
        self.worker_checker = WorkerReadinessChecker()
        self.evaluator = ReadinessEvaluator()

    def run_all_simulations(self) -> FailureSimulationReport:
        scenarios: List[FailureScenarioResult] = []

        # -------------------------------------------------------------
        # Scenario 1: Database Shutdown
        # -------------------------------------------------------------
        db_down = self.db_checker.check_readiness(override_connected=False)
        q_ok = self.queue_checker.check_readiness()
        st_ok = self.storage_checker.check_readiness()
        ai_ok = self.ai_checker.check_readiness()
        w_ok = self.worker_checker.check_readiness()

        res1 = self.evaluator.evaluate_readiness(db_down, q_ok, st_ok, ai_ok, w_ok)
        sc1_passed = (res1.state == ReadinessState.NOT_READY) and (res1.traffic_action == TrafficAction.REJECT_TRAFFIC)

        scenarios.append(
            FailureScenarioResult(
                scenario_id="SCENARIO-01",
                scenario_name="Database Shutdown Simulation",
                injected_failure="Simulate PostgreSQL connection pool failure / database shutdown",
                expected_state=ReadinessState.NOT_READY,
                actual_state=res1.state,
                expected_traffic_action=TrafficAction.REJECT_TRAFFIC,
                actual_traffic_action=res1.traffic_action,
                passed=sc1_passed,
                details={
                    "service_ready": res1.traffic_allowed,
                    "failed_dependencies": res1.failed_dependencies,
                    "verdict": "BLOCKED_TRAFFIC_CORRECTLY" if sc1_passed else "FALSE_READINESS",
                },
            )
        )

        # -------------------------------------------------------------
        # Scenario 2: Redis Broker Failure
        # -------------------------------------------------------------
        db_ok = self.db_checker.check_readiness()
        q_down = self.queue_checker.check_readiness(override_ping=False)
        res2 = self.evaluator.evaluate_readiness(db_ok, q_down, st_ok, ai_ok, w_ok)
        sc2_passed = (res2.state == ReadinessState.NOT_READY) and (res2.traffic_action == TrafficAction.REJECT_TRAFFIC)

        scenarios.append(
            FailureScenarioResult(
                scenario_id="SCENARIO-02",
                scenario_name="Redis Broker Failure Simulation",
                injected_failure="Simulate Redis broker timeout and queue unreachable",
                expected_state=ReadinessState.NOT_READY,
                actual_state=res2.state,
                expected_traffic_action=TrafficAction.REJECT_TRAFFIC,
                actual_traffic_action=res2.traffic_action,
                passed=sc2_passed,
                details={
                    "service_ready": res2.traffic_allowed,
                    "failed_dependencies": res2.failed_dependencies,
                    "verdict": "QUEUE_READINESS_FAILED_CORRECTLY" if sc2_passed else "FALSE_READINESS",
                },
            )
        )

        # -------------------------------------------------------------
        # Scenario 3: Gemini AI Timeout (Degraded Mode)
        # -------------------------------------------------------------
        ai_down = self.ai_checker.check_readiness(override_latency_ms=4500.0, override_response_valid=False)
        res3 = self.evaluator.evaluate_readiness(db_ok, q_ok, st_ok, ai_down, w_ok)
        sc3_passed = (res3.state == ReadinessState.DEGRADED) and (res3.traffic_action == TrafficAction.THROTTLE_TRAFFIC)

        scenarios.append(
            FailureScenarioResult(
                scenario_id="SCENARIO-03",
                scenario_name="Gemini AI Timeout & Rate Limit Simulation",
                injected_failure="Simulate Gemini API response timeout and 429 quota exhaustion",
                expected_state=ReadinessState.DEGRADED,
                actual_state=res3.state,
                expected_traffic_action=TrafficAction.THROTTLE_TRAFFIC,
                actual_traffic_action=res3.traffic_action,
                passed=sc3_passed,
                details={
                    "service_ready": res3.traffic_allowed,
                    "degraded_dependencies": res3.degraded_dependencies,
                    "verdict": "DEGRADED_MODE_ACTIVATED_SAFELY" if sc3_passed else "HARMFUL_HARD_CRASH",
                },
            )
        )

        # -------------------------------------------------------------
        # Scenario 4: Storage Permission Failure
        # -------------------------------------------------------------
        st_down = self.storage_checker.check_readiness(override_write=False)
        res4 = self.evaluator.evaluate_readiness(db_ok, q_ok, st_down, ai_ok, w_ok)
        sc4_passed = (res4.state == ReadinessState.NOT_READY) and (res4.traffic_action == TrafficAction.REJECT_TRAFFIC)

        scenarios.append(
            FailureScenarioResult(
                scenario_id="SCENARIO-04",
                scenario_name="Storage Permission Failure Simulation",
                injected_failure="Simulate filesystem / S3 bucket write permission denial",
                expected_state=ReadinessState.NOT_READY,
                actual_state=res4.state,
                expected_traffic_action=TrafficAction.REJECT_TRAFFIC,
                actual_traffic_action=res4.traffic_action,
                passed=sc4_passed,
                details={
                    "service_ready": res4.traffic_allowed,
                    "failed_dependencies": res4.failed_dependencies,
                    "verdict": "STORAGE_FAILURE_HANDLED_CORRECTLY" if sc4_passed else "FALSE_READINESS",
                },
            )
        )

        passed_count = sum(1 for s in scenarios if s.passed)
        all_passed = (passed_count == len(scenarios))

        return FailureSimulationReport(
            total_scenarios=len(scenarios),
            passed_scenarios=passed_count,
            all_scenarios_passed=all_passed,
            scenarios=scenarios,
            details={
                "simulation_engine": "DocuTask Fault Injection Framework",
                "isolation_guarantee": "Failure states isolated per dependency hierarchy",
            },
        )
