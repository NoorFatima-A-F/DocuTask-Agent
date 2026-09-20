"""
Structured Log Models & 8-Level Severity.

Defines enterprise log record schemas, 8 log levels (TRACE to FATAL),
stack traces, and sensitive data redaction.
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.observability.telemetry.context import mask_sensitive_data


class LogLevel(str, enum.Enum):
    """Eight enterprise log severity classifications."""
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    NOTICE = "NOTICE"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    FATAL = "FATAL"


class LogRecord(BaseModel):
    """Structured JSON log record capturing ambient context and exceptions."""
    log_id: str = Field(default_factory=lambda: f"log-{uuid.uuid4().hex[:12]}")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    level: LogLevel = LogLevel.INFO
    message: str
    service_name: str = "docutask-service"
    service_version: str = "3.1.0"
    environment: str = "production"
    region: str = "us-east-1"
    cluster: str = "cluster-primary"
    tenant_id: str = "global"
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
    user_id: Optional[str] = None
    exception: Optional[str] = None
    stack_trace: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        """Sanitize message and string attributes for sensitive tokens/PII."""
        self.message = mask_sensitive_data(self.message)
        if self.exception:
            self.exception = mask_sensitive_data(self.exception)
        if self.stack_trace:
            self.stack_trace = mask_sensitive_data(self.stack_trace)
