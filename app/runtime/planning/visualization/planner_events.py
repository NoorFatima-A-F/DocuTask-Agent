"""
Strongly Typed Planner Telemetry Events.

Defines fine-grained planner events (PlannerStarted, GoalParsed, TaskCreated, NodeAdded,
NodeRemoved, DependencyResolved, WorkerAssigned, GraphMutated, RecoveryStarted)
fully integrated into AROL EventStore and EventBus.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional
from pydantic import Field
from app.runtime.observability.schemas import EventCategory, EventPriority, PlannerEvent


class PlannerStartedEvent(PlannerEvent):
    event_type: str = "PLANNER_STARTED"
    stage: str = "planning"


class GoalParsedEvent(PlannerEvent):
    event_type: str = "GOAL_PARSED"
    stage: str = "goal_decomposition"


class TaskCreatedEvent(PlannerEvent):
    event_type: str = "TASK_CREATED"
    stage: str = "dag_synthesis"


class NodeAddedEvent(PlannerEvent):
    event_type: str = "NODE_ADDED"
    stage: str = "dag_synthesis"


class EdgeCreatedEvent(PlannerEvent):
    event_type: str = "EDGE_CREATED"
    stage: str = "dependency_wiring"


class DependencyResolvedEvent(PlannerEvent):
    event_type: str = "DEPENDENCY_RESOLVED"
    stage: str = "scheduling"


class WorkerAssignedEvent(PlannerEvent):
    event_type: str = "WORKER_ASSIGNED"
    stage: str = "worker_allocation"


class GraphMutatedEvent(PlannerEvent):
    event_type: str = "GRAPH_MUTATED"
    stage: str = "adaptive_replanning"
    priority: EventPriority = EventPriority.HIGH


class RecoveryStartedEvent(PlannerEvent):
    event_type: str = "RECOVERY_STARTED"
    stage: str = "fault_recovery"
    priority: EventPriority = EventPriority.HIGH
