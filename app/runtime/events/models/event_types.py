"""
DocuTask Agent - Domain Event Types Specification
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from enum import Enum


class DomainEventType(str, Enum):
    # --- Mission Lifecycle ---
    MISSION_CREATED = "MissionCreated"
    MISSION_STARTED = "MissionStarted"
    MISSION_PAUSED = "MissionPaused"
    MISSION_RESUMED = "MissionResumed"
    MISSION_COMPLETED = "MissionCompleted"
    MISSION_FAILED = "MissionFailed"
    MISSION_CANCELLED = "MissionCancelled"

    # --- Planner Lifecycle & Decisions ---
    PLANNER_CREATED = "PlannerCreated"
    PLANNER_STARTED = "PlannerStarted"
    PLANNER_FINISHED = "PlannerFinished"
    PLANNER_FAILED = "PlannerFailed"
    PLANNER_CANCELLED = "PlannerCancelled"
    PLANNER_REPLANNED = "PlannerReplanned"
    PLANNER_OPTIMIZATION_DECIDED = "PlannerOptimizationDecided"
    PLANNER_HEURISTIC_EVALUATED = "PlannerHeuristicEvaluated"

    # --- Task & Execution DAG ---
    TASK_QUEUED = "TaskQueued"
    TASK_ASSIGNED = "TaskAssigned"
    TASK_STARTED = "TaskStarted"
    TASK_PAUSED = "TaskPaused"
    TASK_RESUMED = "TaskResumed"
    TASK_COMPLETED = "TaskCompleted"
    TASK_FAILED = "TaskFailed"
    TASK_RETRIED = "TaskRetried"
    DAG_MUTATED = "DAGMutated"

    # --- Worker Pool & Allocations ---
    WORKER_CREATED = "WorkerCreated"
    WORKER_IDLE = "WorkerIdle"
    WORKER_BUSY = "WorkerBusy"
    WORKER_COMPLETED = "WorkerCompleted"
    WORKER_FAILED = "WorkerFailed"
    WORKER_HEARTBEAT = "WorkerHeartbeat"

    # --- Vision & OCR ---
    OCR_STARTED = "OCRStarted"
    OCR_COMPLETED = "OCRCompleted"
    OCR_FAILED = "OCRFailed"
    OCR_RETRIED = "OCRRetried"

    # --- Memory & Context ---
    MEMORY_RETRIEVED = "MemoryRetrieved"
    MEMORY_MISS = "MemoryMiss"
    MEMORY_STORED = "MemoryStored"
    MEMORY_UPDATED = "MemoryUpdated"

    # --- Reflection & Self-Evolution ---
    REFLECTION_STARTED = "ReflectionStarted"
    REFLECTION_FINISHED = "ReflectionFinished"
    RULE_CANDIDATE_GENERATED = "RuleCandidateGenerated"
    RULE_APPROVED = "RuleApproved"
    RULE_REJECTED = "RuleRejected"

    # --- Scientific Validation ---
    VALIDATION_STARTED = "ValidationStarted"
    VALIDATION_PASSED = "ValidationPassed"
    VALIDATION_FAILED = "ValidationFailed"

    # --- Trust & Truth ---
    TRUST_UPDATED = "TrustUpdated"
    TRUST_RECOVERED = "TrustRecovered"
    TRUST_DECREASED = "TrustDecreased"
    PROOF_COMMITTED = "ProofCommitted"

    # --- Evidence ---
    EVIDENCE_GENERATED = "EvidenceGenerated"
    EVIDENCE_VERIFIED = "EvidenceVerified"
    HASH_VALIDATED = "HashValidated"

    # --- Recovery & Self-Healing ---
    FAILURE_DETECTED = "FailureDetected"
    RECOVERY_STARTED = "RecoveryStarted"
    RECOVERY_COMPLETED = "RecoveryCompleted"
    RECOVERY_FAILED = "RecoveryFailed"

    # --- Chaos Engineering ---
    FAULT_INJECTED = "FaultInjected"
    FAULT_CONTAINED = "FaultContained"
    ROLLBACK_STARTED = "RollbackStarted"
    ROLLBACK_COMPLETED = "RollbackCompleted"


class EventSubsystem(str, Enum):
    MISSION_CONTROL = "MISSION_CONTROL"
    PLANNER = "PLANNER"
    DAG_ENGINE = "DAG_ENGINE"
    WORKER_POOL = "WORKER_POOL"
    OCR_SERVICE = "OCR_SERVICE"
    MEMORY_GRAPH = "MEMORY_GRAPH"
    REFLECTION_ENGINE = "REFLECTION_ENGINE"
    VALIDATION_ENGINE = "VALIDATION_ENGINE"
    TRUTH_LEDGER = "TRUTH_LEDGER"
    EVIDENCE_STORE = "EVIDENCE_STORE"
    RECOVERY_MANAGER = "RECOVERY_MANAGER"
    CHAOS_ORCHESTRATOR = "CHAOS_ORCHESTRATOR"
    DIGITAL_TWIN = "DIGITAL_TWIN"


class EventSeverity(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
