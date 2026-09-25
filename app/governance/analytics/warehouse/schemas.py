"""Governance Analytics Warehouse Relational Schemas and Query Filter DTOs."""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class WarehouseQueryFilter(BaseModel):
    tenant_id: str = "*"
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    actor_id: Optional[str] = None
    agent_id: Optional[str] = None
    model_id: Optional[str] = None
    prompt_id: Optional[str] = None
    policy_id: Optional[str] = None
    framework: Optional[str] = None
    category: Optional[str] = None
    limit: int = 1000
    offset: int = 0


class TimeBucketSummary(BaseModel):
    date_key: str
    event_count: int = 0
    avg_risk_score: float = 0.0
    total_cost_usd: float = 0.0
    avg_latency_ms: float = 0.0
    violation_count: int = 0
    approval_count: int = 0
