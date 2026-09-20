# Pydantic Schemas for Runtime Events
from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class RuntimeEventSchema(BaseModel):
    event_id: str
    mission_id: str
    parent_event_id: Optional[str] = None
    timestamp: datetime
    sequence_number: int = 0
    agent_id: Optional[str] = None
    worker_id: Optional[str] = None
    event_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: str
    causation_id: Optional[str] = None
    trace_id: str
    span_id: Optional[str] = None
    duration_ms: Optional[float] = None
    status: str = 'COMPLETED'
    version: str = '1.0.0'

class EventQueryFilter(BaseModel):
    mission_id: Optional[str] = None
    agent_id: Optional[str] = None
    event_types: Optional[List[str]] = None
    since_sequence: Optional[int] = None
    limit: int = 500
    reverse: bool = False

class MissionStartRequest(BaseModel):
    goal: str = Field(..., description='High level goal description')
    mission_id: Optional[str] = None
    scenario_type: Optional[str] = Field('THERMAL_INVOICE_AUDIT', description='Pre-configured realistic scenario')
    parameters: Dict[str, Any] = Field(default_factory=dict)

class ConversationalCommandRequest(BaseModel):
    mission_id: str
    command_text: str
    target_agent: Optional[str] = None

class HumanFeedbackRequest(BaseModel):
    mission_id: str
    document_id: str
    field_name: str
    original_value: str
    corrected_value: str
    distillation_type: str = Field('RULE', description='RULE, MEMORY, or BENCHMARK')
    operator_notes: Optional[str] = None
