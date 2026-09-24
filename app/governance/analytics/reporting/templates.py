"""Governance Report Templates and Types."""

from enum import Enum
from typing import Dict, Any, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid


class ReportType(str, Enum):
    DAILY_OPERATIONAL = "DAILY_OPERATIONAL"
    WEEKLY_SUMMARY = "WEEKLY_SUMMARY"
    MONTHLY_EXECUTIVE = "MONTHLY_EXECUTIVE"
    COMPLIANCE_AUDIT = "COMPLIANCE_AUDIT"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"


class ReportFormat(str, Enum):
    JSON = "JSON"
    CSV = "CSV"
    PDF = "PDF"
    EXCEL = "EXCEL"


class GovernanceReportSection(BaseModel):
    title: str
    summary_text: str
    metrics: Dict[str, Any] = Field(default_factory=dict)
    key_findings: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class GovernanceReport(BaseModel):
    report_id: str = Field(default_factory=lambda: f"rep_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    report_type: ReportType
    title: str
    executive_summary: str
    governance_score: float = 100.0
    sections: List[GovernanceReportSection] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
