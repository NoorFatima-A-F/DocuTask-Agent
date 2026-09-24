# Enterprise Event Taxonomy for DocuTask Agent
from __future__ import annotations
from dataclasses import dataclass
from app.runtime.events.base import RuntimeEvent

# Planner
@dataclass(frozen=True)
class MissionCreated(RuntimeEvent): event_type: str = 'MissionCreated'
@dataclass(frozen=True)
class GoalAccepted(RuntimeEvent): event_type: str = 'GoalAccepted'
@dataclass(frozen=True)
class PlannerStarted(RuntimeEvent): event_type: str = 'PlannerStarted'
@dataclass(frozen=True)
class PlannerCompleted(RuntimeEvent): event_type: str = 'PlannerCompleted'
@dataclass(frozen=True)
class TaskGraphGenerated(RuntimeEvent): event_type: str = 'TaskGraphGenerated'
@dataclass(frozen=True)
class TaskGraphUpdated(RuntimeEvent): event_type: str = 'TaskGraphUpdated'
@dataclass(frozen=True)
class TaskSplit(RuntimeEvent): event_type: str = 'TaskSplit'
@dataclass(frozen=True)
class TaskMerged(RuntimeEvent): event_type: str = 'TaskMerged'
@dataclass(frozen=True)
class DependencyResolved(RuntimeEvent): event_type: str = 'DependencyResolved'

# Execution
@dataclass(frozen=True)
class WorkerScheduled(RuntimeEvent): event_type: str = 'WorkerScheduled'
@dataclass(frozen=True)
class WorkerStarted(RuntimeEvent): event_type: str = 'WorkerStarted'
@dataclass(frozen=True)
class WorkerPaused(RuntimeEvent): event_type: str = 'WorkerPaused'
@dataclass(frozen=True)
class WorkerResumed(RuntimeEvent): event_type: str = 'WorkerResumed'
@dataclass(frozen=True)
class WorkerCompleted(RuntimeEvent): event_type: str = 'WorkerCompleted'
@dataclass(frozen=True)
class WorkerFailed(RuntimeEvent): event_type: str = 'WorkerFailed'
@dataclass(frozen=True)
class WorkerCancelled(RuntimeEvent): event_type: str = 'WorkerCancelled'

# Memory
@dataclass(frozen=True)
class MemoryRetrieved(RuntimeEvent): event_type: str = 'MemoryRetrieved'
@dataclass(frozen=True)
class MemoryCreated(RuntimeEvent): event_type: str = 'MemoryCreated'
@dataclass(frozen=True)
class MemoryUpdated(RuntimeEvent): event_type: str = 'MemoryUpdated'
@dataclass(frozen=True)
class InvariantApplied(RuntimeEvent): event_type: str = 'InvariantApplied'
@dataclass(frozen=True)
class ReflectionStored(RuntimeEvent): event_type: str = 'ReflectionStored'

# Reflection
@dataclass(frozen=True)
class ReflectionStarted(RuntimeEvent): event_type: str = 'ReflectionStarted'
@dataclass(frozen=True)
class ReflectionCompleted(RuntimeEvent): event_type: str = 'ReflectionCompleted'
@dataclass(frozen=True)
class HypothesisRejected(RuntimeEvent): event_type: str = 'HypothesisRejected'
@dataclass(frozen=True)
class StrategyChanged(RuntimeEvent): event_type: str = 'StrategyChanged'

# Validation
@dataclass(frozen=True)
class ValidationStarted(RuntimeEvent): event_type: str = 'ValidationStarted'
@dataclass(frozen=True)
class ValidationPassed(RuntimeEvent): event_type: str = 'ValidationPassed'
@dataclass(frozen=True)
class ValidationFailed(RuntimeEvent): event_type: str = 'ValidationFailed'
@dataclass(frozen=True)
class EvidenceMissing(RuntimeEvent): event_type: str = 'EvidenceMissing'

# Human
@dataclass(frozen=True)
class HumanFeedbackRequested(RuntimeEvent): event_type: str = 'HumanFeedbackRequested'
@dataclass(frozen=True)
class HumanFeedbackReceived(RuntimeEvent): event_type: str = 'HumanFeedbackReceived'
@dataclass(frozen=True)
class HumanApproved(RuntimeEvent): event_type: str = 'HumanApproved'
@dataclass(frozen=True)
class HumanRejected(RuntimeEvent): event_type: str = 'HumanRejected'

# System
@dataclass(frozen=True)
class MissionCompleted(RuntimeEvent): event_type: str = 'MissionCompleted'
@dataclass(frozen=True)
class MissionFailed(RuntimeEvent): event_type: str = 'MissionFailed'
@dataclass(frozen=True)
class MissionCancelled(RuntimeEvent): event_type: str = 'MissionCancelled'
@dataclass(frozen=True)
class TelemetryUpdated(RuntimeEvent): event_type: str = 'TelemetryUpdated'
@dataclass(frozen=True)
class ReplayCheckpoint(RuntimeEvent): event_type: str = 'ReplayCheckpoint'

EVENT_TYPE_MAP = {
    'MissionCreated': MissionCreated, 'GoalAccepted': GoalAccepted,
    'PlannerStarted': PlannerStarted, 'PlannerCompleted': PlannerCompleted,
    'TaskGraphGenerated': TaskGraphGenerated, 'TaskGraphUpdated': TaskGraphUpdated,
    'TaskSplit': TaskSplit, 'TaskMerged': TaskMerged, 'DependencyResolved': DependencyResolved,
    'WorkerScheduled': WorkerScheduled, 'WorkerStarted': WorkerStarted,
    'WorkerPaused': WorkerPaused, 'WorkerResumed': WorkerResumed,
    'WorkerCompleted': WorkerCompleted, 'WorkerFailed': WorkerFailed,
    'WorkerCancelled': WorkerCancelled, 'MemoryRetrieved': MemoryRetrieved,
    'MemoryCreated': MemoryCreated, 'MemoryUpdated': MemoryUpdated,
    'InvariantApplied': InvariantApplied, 'ReflectionStored': ReflectionStored,
    'ReflectionStarted': ReflectionStarted, 'ReflectionCompleted': ReflectionCompleted,
    'HypothesisRejected': HypothesisRejected, 'StrategyChanged': StrategyChanged,
    'ValidationStarted': ValidationStarted, 'ValidationPassed': ValidationPassed,
    'ValidationFailed': ValidationFailed, 'EvidenceMissing': EvidenceMissing,
    'HumanFeedbackRequested': HumanFeedbackRequested, 'HumanFeedbackReceived': HumanFeedbackReceived,
    'HumanApproved': HumanApproved, 'HumanRejected': HumanRejected,
    'MissionCompleted': MissionCompleted, 'MissionFailed': MissionFailed,
    'MissionCancelled': MissionCancelled, 'TelemetryUpdated': TelemetryUpdated,
    'ReplayCheckpoint': ReplayCheckpoint, 'RuntimeEvent': RuntimeEvent,
}

def event_from_dict(data):
    etype = data.get('event_type', 'RuntimeEvent')
    cls = EVENT_TYPE_MAP.get(etype, RuntimeEvent)
    return cls.from_dict(data)
