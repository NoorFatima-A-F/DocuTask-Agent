"""SRE Automation Framework for Closed-Loop Self-Healing."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from .actions import AutoActionType, AutomationExecutionResult, SREActionExecutor
from ..alerts.engine import ActiveAlert


@dataclass
class SelfHealingRule:
    rule_id: str
    alert_name_pattern: str
    action_type: AutoActionType
    target_extractor: Callable[[ActiveAlert], str]
    cooldown_seconds: float = 300.0
    auto_execute: bool = True
    last_executed: float = 0.0


class SREAutomationFramework:
    """Orchestrates diagnostic evaluation, safe automated action execution, and verification loops."""

    def __init__(self, executor: Optional[SREActionExecutor] = None):
        self.executor = executor or SREActionExecutor()
        self._rules: Dict[str, SelfHealingRule] = {}
        self._execution_history: List[AutomationExecutionResult] = []
        self._initialize_default_rules()

    def _initialize_default_rules(self) -> None:
        # 1. Rule: High Queue Backlog -> Scale Workers
        self.register_rule(
            SelfHealingRule(
                rule_id="sh-scale-on-queue-high",
                alert_name_pattern="*queue.depth*",
                action_type=AutoActionType.SCALE_WORKERS,
                target_extractor=lambda a: a.labels.get("cluster_id", "cluster-primary"),
            )
        )
        # 2. Rule: Worker Node Crash -> Restart Service
        self.register_rule(
            SelfHealingRule(
                rule_id="sh-restart-on-worker-crash",
                alert_name_pattern="*worker.crash*",
                action_type=AutoActionType.RESTART_SERVICE,
                target_extractor=lambda a: a.labels.get("service_name", "doc-worker"),
            )
        )

    def register_rule(self, rule: SelfHealingRule) -> None:
        self._rules[rule.rule_id] = rule

    def handle_alert(self, alert: ActiveAlert) -> Optional[AutomationExecutionResult]:
        """Evaluate if firing alert matches any self-healing rule and trigger remediation."""
        now = time.time()
        for rule in self._rules.values():
            import fnmatch
            if fnmatch.fnmatch(alert.name, rule.alert_name_pattern) or fnmatch.fnmatch(alert.rule_id, rule.alert_name_pattern):
                if (now - rule.last_executed) < rule.cooldown_seconds:
                    # In cooldown
                    continue

                target = rule.target_extractor(alert)
                rule.last_executed = now

                res: Optional[AutomationExecutionResult] = None
                if rule.action_type == AutoActionType.SCALE_WORKERS:
                    res = self.executor.scale_workers(cluster_id=target, target_worker_count=10)
                elif rule.action_type == AutoActionType.RESTART_SERVICE:
                    res = self.executor.restart_service(service_name=target)
                elif rule.action_type == AutoActionType.CLEAR_QUEUE:
                    res = self.executor.clear_stuck_queue(queue_name=target)

                if res:
                    self._execution_history.append(res)
                    return res

        return None

    def get_history(self) -> List[AutomationExecutionResult]:
        return list(self._execution_history)
