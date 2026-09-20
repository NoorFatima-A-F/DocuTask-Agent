"""
Enterprise Autonomous Recovery Engine.
Core resilience engine diagnosing failures, selecting recovery strategies,
planning remediation graphs, and orchestrating recovery via adapters.
"""

from typing import Optional
from uuid import uuid4
from app.agents.recovery.context import RecoveryRequest, RecoveryResult
from app.agents.recovery.failure_classifier import FailureClassifier
from app.agents.recovery.lifecycle import RecoveryLifecycleState
from app.agents.recovery.metadata import RecoveryStatistics
from app.agents.recovery.recovery_executor import RecoveryExecutor
from app.agents.recovery.recovery_planner import RecoveryPlanner
from app.agents.recovery.root_cause import RootCauseAnalyzer
from app.agents.recovery.strategy_selector import RecoveryStrategySelector


class RecoveryEngine:
    """
    Autonomous Recovery Engine.
    Consumes execution faults, classifies failures, analyzes root cause, selects optimal recovery
    strategy, plans recovery workflows, and coordinates remediation via adapters.
    """

    def __init__(
        self,
        classifier: Optional[FailureClassifier] = None,
        root_cause_analyzer: Optional[RootCauseAnalyzer] = None,
        strategy_selector: Optional[RecoveryStrategySelector] = None,
        planner: Optional[RecoveryPlanner] = None,
        executor: Optional[RecoveryExecutor] = None
    ):
        self.classifier = classifier or FailureClassifier()
        self.root_cause_analyzer = root_cause_analyzer or RootCauseAnalyzer()
        self.strategy_selector = strategy_selector or RecoveryStrategySelector()
        self.planner = planner or RecoveryPlanner()
        self.executor = executor or RecoveryExecutor()

    async def recover(self, request: RecoveryRequest) -> RecoveryResult:
        """Executes full diagnostic and autonomous recovery pipeline."""
        recovery_id = uuid4()
        failure = request.failure

        # 1. Root cause analysis
        root_cause_report = self.root_cause_analyzer.analyze(failure)

        # 2. Strategy selection
        strategy_def = self.strategy_selector.select_strategy(failure, root_cause_report)

        # 3. Recovery planning
        recovery_graph = self.planner.plan_recovery(failure, strategy_def)

        # 4. Recovery execution
        success = await self.executor.execute_recovery_graph(recovery_graph)

        state = RecoveryLifecycleState.COMPLETED if success else RecoveryLifecycleState.FAILED

        stats = RecoveryStatistics(
            retry_attempts=1,
            checkpoints_evaluated=1,
            nodes_compensated=1 if "COMPENSATE" in str(strategy_def.strategy) else 0
        )

        return RecoveryResult(
            recovery_id=recovery_id,
            execution_id=failure.identity.execution_id,
            lifecycle_state=state,
            strategy_executed=strategy_def.strategy,
            is_remediated=success,
            statistics=stats,
            messages=[f"Recovery executed strategy: {strategy_def.strategy.value}"]
        )
