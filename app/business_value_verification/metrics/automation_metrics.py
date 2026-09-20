"""
Automation metrics and straight-through processing (STP) calculator.
"""

from typing import Dict, Any
from app.business_value_verification.domain.models import AutomationMetrics


class AutomationMetricsCalculator:
    """Calculates task automation rates, STP %, and human intervention touchpoints."""

    @staticmethod
    def calculate_metrics(
        total_tasks: int = 100,
        automated_tasks: int = 88,
        human_touchpoint_tasks: int = 12,
        stp_volume_pct: float = 91.5,
        exception_routing_pct: float = 8.5,
    ) -> AutomationMetrics:
        automation_rate = (automated_tasks / total_tasks * 100.0) if total_tasks > 0 else 0.0

        return AutomationMetrics(
            total_workflow_tasks=total_tasks,
            fully_automated_tasks=automated_tasks,
            human_touchpoint_tasks=human_touchpoint_tasks,
            automation_rate_pct=automation_rate,
            straight_through_processing_pct=stp_volume_pct,
            exception_routing_pct=exception_routing_pct,
        )
