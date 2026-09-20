"""
Tests for Budget Manager, Agent Scheduler, and Analytics Engine.
"""

from app.agents.analytics.agent_analytics import AgentAnalytics
from app.agents.budgeting.budget_manager import BudgetAction, BudgetManager
from app.agents.scheduling.agent_scheduler import AgentScheduler, TaskPriority


def test_budget_manager_progressive_actions():
    budget_mgr = BudgetManager()
    agent_id = "agent-budget-test"

    spec = {"max_cost_usd": 1.0, "max_tokens": 10000, "max_execution_time_seconds": 60}

    # Normal usage (< 60%)
    budget_mgr.record_consumption(agent_id, tokens=2000, cost_usd=0.20, execution_time_seconds=10)
    action1 = budget_mgr.evaluate_budget(agent_id, spec)
    assert action1 == BudgetAction.CONTINUE

    # Warning threshold (60% - 79%)
    budget_mgr.record_consumption(agent_id, tokens=4500, cost_usd=0.45, execution_time_seconds=20)
    action2 = budget_mgr.evaluate_budget(agent_id, spec)
    assert action2 == BudgetAction.WARN

    # Approval threshold (80% - 99%)
    budget_mgr.record_consumption(agent_id, tokens=2000, cost_usd=0.20, execution_time_seconds=15)
    action3 = budget_mgr.evaluate_budget(agent_id, spec)
    assert action3 == BudgetAction.REQUIRE_APPROVAL

    # Hard limit breach (>= 100%)
    budget_mgr.record_consumption(agent_id, tokens=5000, cost_usd=0.50, execution_time_seconds=30)
    action4 = budget_mgr.evaluate_budget(agent_id, spec)
    assert action4 == BudgetAction.TERMINATE


def test_agent_scheduler_priority_queuing_and_concurrency():
    scheduler = AgentScheduler(max_concurrent_tasks=2)

    t_low = scheduler.schedule("task-low", "ExecutionAgent", priority=TaskPriority.LOW)
    t_crit = scheduler.schedule("task-crit", "SecurityAgent", priority=TaskPriority.CRITICAL)
    t_high = scheduler.schedule("task-high", "ValidationAgent", priority=TaskPriority.HIGH)

    assert scheduler.queue_size == 3

    # First popped should be CRITICAL
    first = scheduler.pop_next()
    assert first is not None
    assert first.task_id == "task-crit"

    # Second popped should be HIGH
    second = scheduler.pop_next()
    assert second is not None
    assert second.task_id == "task-high"

    # Concurrency limit reached (2/2 active)
    third = scheduler.pop_next()
    assert third is None
    assert scheduler.active_count == 2

    # Complete one task and pull LOW
    scheduler.complete_task("task-crit")
    assert scheduler.active_count == 1

    pulled_low = scheduler.pop_next()
    assert pulled_low is not None
    assert pulled_low.task_id == "task-low"


def test_agent_analytics_aggregation():
    analytics = AgentAnalytics()
    analytics.record_goal()
    analytics.record_goal()
    analytics.record_task_completion(latency_ms=100.0, cost_usd=0.01, confidence=0.95)
    analytics.record_task_completion(latency_ms=150.0, cost_usd=0.02, confidence=0.90)
    analytics.record_task_failure(recovered=True)
    analytics.record_reflection()
    analytics.record_memory_hit()

    summary = analytics.get_summary(registered_agents_count=5)
    assert summary.total_agents_registered == 5
    assert summary.total_goals_created == 2
    assert summary.total_tasks_completed == 2
    assert summary.total_tasks_failed == 1
    assert summary.recovery_rate == 1.0
    assert summary.total_cost_usd == 0.03
    assert summary.average_latency_ms == 125.0
    assert summary.memory_hits == 1
