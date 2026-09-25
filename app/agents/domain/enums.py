"""
Centralized Agent Domain Enumerations.
Defines strongly typed enums for goals, tasks, workflows, results, artifacts, policies, and capabilities.
"""

from enum import Enum


class GoalType(str, Enum):
    """Supported business and technical goal types."""
    BUSINESS = "BUSINESS"
    DOCUMENT = "DOCUMENT"
    EXTRACTION = "EXTRACTION"
    VALIDATION = "VALIDATION"
    CLASSIFICATION = "CLASSIFICATION"
    STORAGE = "STORAGE"
    NOTIFICATION = "NOTIFICATION"
    ANALYTICS = "ANALYTICS"
    COMPOSITE = "COMPOSITE"


class TaskType(str, Enum):
    """Supported agent task execution types."""
    OCR = "OCR"
    EXTRACTION = "EXTRACTION"
    VALIDATION = "VALIDATION"
    STORAGE = "STORAGE"
    NOTIFICATION = "NOTIFICATION"
    CLASSIFICATION = "CLASSIFICATION"
    SUMMARIZATION = "SUMMARIZATION"
    TRANSFORMATION = "TRANSFORMATION"
    REVIEW = "REVIEW"
    ARCHIVE = "ARCHIVE"
    CUSTOM = "CUSTOM"


class WorkflowType(str, Enum):
    """Workflow graph topology types."""
    LINEAR = "LINEAR"
    CONDITIONAL = "CONDITIONAL"
    PARALLEL = "PARALLEL"
    FAN_OUT = "FAN_OUT"
    FAN_IN = "FAN_IN"
    DAG = "DAG"


class ResultStatus(str, Enum):
    """Execution result outcome status."""
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    CANCELLED = "CANCELLED"
    SKIPPED = "SKIPPED"


class ExecutionStatus(str, Enum):
    """Execution status lifecycle states."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    WAITING = "WAITING"


class PriorityLevel(str, Enum):
    """Priority levels for goals, tasks, and queues."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ArtifactType(str, Enum):
    """Produced execution artifact categories."""
    OCR_OUTPUT = "OCR_OUTPUT"
    EXTRACTED_JSON = "EXTRACTED_JSON"
    VALIDATION_REPORT = "VALIDATION_REPORT"
    SUMMARY = "SUMMARY"
    EMBEDDING = "EMBEDDING"
    CLASSIFICATION = "CLASSIFICATION"
    LOGS = "LOGS"
    METRICS = "METRICS"
    EVIDENCE = "EVIDENCE"
    AUDIT_RECORD = "AUDIT_RECORD"
    TEMPORARY_FILE = "TEMPORARY_FILE"
    FINAL_OUTPUT = "FINAL_OUTPUT"


class RetryStrategy(str, Enum):
    """Retry policy backoff strategies."""
    IMMEDIATE = "IMMEDIATE"
    FIXED_INTERVAL = "FIXED_INTERVAL"
    EXPONENTIAL_BACKOFF = "EXPONENTIAL_BACKOFF"
    EXPONENTIAL_JITTER = "EXPONENTIAL_JITTER"


class DependencyType(str, Enum):
    """Task dependency relation types."""
    HARD = "HARD"
    SOFT = "SOFT"
    OPTIONAL = "OPTIONAL"
    CONDITIONAL = "CONDITIONAL"
    RUNTIME = "RUNTIME"


class ConstraintType(str, Enum):
    """Execution constraint categories."""
    TIME = "TIME"
    BUDGET = "BUDGET"
    TOKEN = "TOKEN"
    SECURITY = "SECURITY"
    DOCUMENT = "DOCUMENT"
    RESOURCE = "RESOURCE"
    LATENCY = "LATENCY"
    COMPLIANCE = "COMPLIANCE"
    QUALITY = "QUALITY"
    CONFIDENCE = "CONFIDENCE"


class CapabilityType(str, Enum):
    """Agent and tool capability classifications."""
    OCR = "OCR"
    EXTRACTION = "EXTRACTION"
    VALIDATION = "VALIDATION"
    SUMMARIZATION = "SUMMARIZATION"
    TRANSLATION = "TRANSLATION"
    CLASSIFICATION = "CLASSIFICATION"
    STORAGE = "STORAGE"
    NOTIFICATION = "NOTIFICATION"
    ANALYTICS = "ANALYTICS"
    REASONING = "REASONING"
    PLANNING = "PLANNING"
    REFLECTION = "REFLECTION"
    RECOVERY = "RECOVERY"
    TOOL_SELECTION = "TOOL_SELECTION"
