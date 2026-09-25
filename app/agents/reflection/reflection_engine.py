"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Reflection Engine.
Generates structured reflection summaries, analyzes success and failure factors,
and recommends memory updates without persisting private chain-of-thought.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
import logging

logger = logging.getLogger(__name__)


@dataclass
class ReflectionReport:
    """Structured output of agent self-reflection."""
    id: str = field(default_factory=lambda: f"refl-{uuid.uuid4().hex[:10]}")
    agent_id: str = ""
    task_id: str = ""
    execution_summary: str = ""
    success_factors: List[str] = field(default_factory=list)
    failure_factors: List[str] = field(default_factory=list)
    improvement_suggestions: List[str] = field(default_factory=list)
    memory_update_recommendations: List[Dict[str, Any]] = field(default_factory=list)
    quality_score: float = 1.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "execution_summary": self.execution_summary,
            "success_factors": self.success_factors,
            "failure_factors": self.failure_factors,
            "improvement_suggestions": self.improvement_suggestions,
            "memory_update_recommendations": self.memory_update_recommendations,
            "quality_score": self.quality_score,
            "timestamp": self.timestamp.isoformat(),
        }


class ReflectionEngine:
    """
    Cognitive reflection service analyzing completed or failed agent actions
    to promote continuous learning and memory consolidation.
    """

    def reflect_on_execution(
        self,
        agent_id: str,
        task_id: str,
        execution_outcome: Dict[str, Any],
        expected_outcome: Optional[Dict[str, Any]] = None,
    ) -> ReflectionReport:
        """
        Analyzes task outcome and generates structured reflection without CoT.
        """
        is_success = execution_outcome.get("status") == "SUCCESS"
        success_factors: List[str] = []
        failure_factors: List[str] = []
        suggestions: List[str] = []
        memory_updates: List[Dict[str, Any]] = []

        if is_success:
            success_factors.append("Completed all assigned task skills within deadline")
            quality_score = 0.95
            memory_updates.append({
                "key": f"proc_{task_id}",
                "tier": "PROCEDURAL",
                "value": f"Successful execution pattern for task {task_id}",
                "importance": 0.7,
            })
        else:
            failure_factors.append(str(execution_outcome.get("error", "Unknown execution error")))
            suggestions.append("Apply retry strategy with exponential backoff")
            suggestions.append("Verify tool input schema parameters before dispatch")
            quality_score = 0.40
            memory_updates.append({
                "key": f"incident_{task_id}",
                "tier": "EPISODIC",
                "value": f"Failure encounter in task {task_id}: {execution_outcome.get('error')}",
                "importance": 0.8,
            })

        summary = f"Execution of task '{task_id}' by agent '{agent_id}' yielded status '{execution_outcome.get('status')}'."

        report = ReflectionReport(
            agent_id=agent_id,
            task_id=task_id,
            execution_summary=summary,
            success_factors=success_factors,
            failure_factors=failure_factors,
            improvement_suggestions=suggestions,
            memory_update_recommendations=memory_updates,
            quality_score=quality_score,
        )

        logger.info(f"Reflection completed for Agent {agent_id} on Task {task_id} [Score: {quality_score}]")
        return report
