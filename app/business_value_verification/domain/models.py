"""
Domain models and schemas for Phase V11 Enterprise Business Value, ROI Intelligence & Operational Impact Verification Program (EBV-OIVP).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Any


class IndustryVertical(str, Enum):
    FINANCE = "FINANCE"
    LEGAL = "LEGAL"
    HR = "HR"
    HEALTHCARE = "HEALTHCARE"


class ProcessStepType(str, Enum):
    MANUAL = "MANUAL"
    SEMI_AUTOMATED = "SEMI_AUTOMATED"
    AUTONOMOUS_AI = "AUTONOMOUS_AI"


@dataclass
class WorkflowStep:
    name: str
    step_type: ProcessStepType
    duration_seconds: float
    human_involvement_pct: float
    error_probability_pct: float
    cost_usd: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "step_type": self.step_type.value,
            "duration_seconds": round(self.duration_seconds, 1),
            "human_involvement_pct": round(self.human_involvement_pct, 1),
            "error_probability_pct": round(self.error_probability_pct, 2),
            "cost_usd": round(self.cost_usd, 4),
        }


@dataclass
class ProcessModel:
    name: str
    vertical: IndustryVertical
    is_ai_system: bool
    steps: List[WorkflowStep]
    total_duration_minutes: float
    total_cost_usd: float
    accuracy_pct: float
    human_hours_per_1k_docs: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "vertical": self.vertical.value,
            "is_ai_system": self.is_ai_system,
            "steps": [s.to_dict() for s in self.steps],
            "total_duration_minutes": round(self.total_duration_minutes, 2),
            "total_cost_usd": round(self.total_cost_usd, 4),
            "accuracy_pct": round(self.accuracy_pct, 2),
            "human_hours_per_1k_docs": round(self.human_hours_per_1k_docs, 1),
        }


@dataclass
class WorkflowComparison:
    workflow_name: str
    vertical: IndustryVertical
    baseline: ProcessModel
    ai_system: ProcessModel
    time_reduction_pct: float
    cost_reduction_pct: float
    human_effort_reduction_pct: float
    accuracy_improvement_pct: float
    speedup_multiplier: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_name": self.workflow_name,
            "vertical": self.vertical.value,
            "baseline": self.baseline.to_dict(),
            "ai_system": self.ai_system.to_dict(),
            "time_reduction_pct": round(self.time_reduction_pct, 2),
            "cost_reduction_pct": round(self.cost_reduction_pct, 2),
            "human_effort_reduction_pct": round(self.human_effort_reduction_pct, 2),
            "accuracy_improvement_pct": round(self.accuracy_improvement_pct, 2),
            "speedup_multiplier": round(self.speedup_multiplier, 1),
        }


@dataclass
class AutomationMetrics:
    total_workflow_tasks: int
    fully_automated_tasks: int
    human_touchpoint_tasks: int
    automation_rate_pct: float
    straight_through_processing_pct: float
    exception_routing_pct: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_workflow_tasks": self.total_workflow_tasks,
            "fully_automated_tasks": self.fully_automated_tasks,
            "human_touchpoint_tasks": self.human_touchpoint_tasks,
            "automation_rate_pct": round(self.automation_rate_pct, 2),
            "straight_through_processing_pct": round(self.straight_through_processing_pct, 2),
            "exception_routing_pct": round(self.exception_routing_pct, 2),
        }


@dataclass
class ProductivityImpact:
    baseline_human_hours_annual: float
    ai_human_hours_annual: float
    hours_liberated_annual: float
    fte_capacity_liberated: float
    throughput_expansion_multiplier: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "baseline_human_hours_annual": round(self.baseline_human_hours_annual, 1),
            "ai_human_hours_annual": round(self.ai_human_hours_annual, 1),
            "hours_liberated_annual": round(self.hours_liberated_annual, 1),
            "fte_capacity_liberated": round(self.fte_capacity_liberated, 2),
            "throughput_expansion_multiplier": round(self.throughput_expansion_multiplier, 1),
        }


@dataclass
class AccuracyComparison:
    human_field_error_rate_pct: float
    ai_field_error_rate_pct: float
    human_missed_anomalies_pct: float
    ai_caught_anomalies_pct: float
    overall_quality_improvement_pct: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "human_field_error_rate_pct": round(self.human_field_error_rate_pct, 2),
            "ai_field_error_rate_pct": round(self.ai_field_error_rate_pct, 2),
            "human_missed_anomalies_pct": round(self.human_missed_anomalies_pct, 2),
            "ai_caught_anomalies_pct": round(self.ai_caught_anomalies_pct, 2),
            "overall_quality_improvement_pct": round(self.overall_quality_improvement_pct, 2),
        }


@dataclass
class ROIAnalysisResult:
    monthly_document_volume: int
    employee_hourly_rate: float
    baseline_monthly_cost: float
    ai_monthly_cost: float
    monthly_net_savings: float
    annual_net_savings: float
    annual_platform_investment: float
    net_annual_roi_pct: float
    roi_multiple: float
    payback_period_months: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "monthly_document_volume": self.monthly_document_volume,
            "employee_hourly_rate": round(self.employee_hourly_rate, 2),
            "baseline_monthly_cost": round(self.baseline_monthly_cost, 2),
            "ai_monthly_cost": round(self.ai_monthly_cost, 2),
            "monthly_net_savings": round(self.monthly_net_savings, 2),
            "annual_net_savings": round(self.annual_net_savings, 2),
            "annual_platform_investment": round(self.annual_platform_investment, 2),
            "net_annual_roi_pct": round(self.net_annual_roi_pct, 2),
            "roi_multiple": round(self.roi_multiple, 1),
            "payback_period_months": round(self.payback_period_months, 2),
        }


@dataclass
class TCOComparison:
    year_1_human_tco: float
    year_1_ai_tco: float
    year_2_human_tco: float
    year_2_ai_tco: float
    year_3_human_tco: float
    year_3_ai_tco: float
    cumulative_3yr_human_tco: float
    cumulative_3yr_ai_tco: float
    cumulative_3yr_net_savings: float
    scaling_elasticity: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "year_1_human_tco": round(self.year_1_human_tco, 2),
            "year_1_ai_tco": round(self.year_1_ai_tco, 2),
            "year_2_human_tco": round(self.year_2_human_tco, 2),
            "year_2_ai_tco": round(self.year_2_ai_tco, 2),
            "year_3_human_tco": round(self.year_3_human_tco, 2),
            "year_3_ai_tco": round(self.year_3_ai_tco, 2),
            "cumulative_3yr_human_tco": round(self.cumulative_3yr_human_tco, 2),
            "cumulative_3yr_ai_tco": round(self.cumulative_3yr_ai_tco, 2),
            "cumulative_3yr_net_savings": round(self.cumulative_3yr_net_savings, 2),
            "scaling_elasticity": self.scaling_elasticity,
        }


@dataclass
class EnterpriseSimulationResult:
    tier_name: str
    monthly_docs: int
    staff_count: int
    baseline_annual_cost: float
    ai_annual_cost: float
    annual_net_savings: float
    ftes_reallocated: float
    cycle_time_compression_pct: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tier_name": self.tier_name,
            "monthly_docs": self.monthly_docs,
            "staff_count": self.staff_count,
            "baseline_annual_cost": round(self.baseline_annual_cost, 2),
            "ai_annual_cost": round(self.ai_annual_cost, 2),
            "annual_net_savings": round(self.annual_net_savings, 2),
            "ftes_reallocated": round(self.ftes_reallocated, 1),
            "cycle_time_compression_pct": round(self.cycle_time_compression_pct, 2),
        }


@dataclass
class AdoptionMetric:
    role: str
    primary_benefit: str
    satisfaction_score: float  # out of 100
    adoption_velocity_days: int
    active_engagement_pct: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "primary_benefit": self.primary_benefit,
            "satisfaction_score": round(self.satisfaction_score, 1),
            "adoption_velocity_days": self.adoption_velocity_days,
            "active_engagement_pct": round(self.active_engagement_pct, 1),
        }


@dataclass
class CaseStudyResult:
    title: str
    client_industry: str
    organization_profile: str
    problem_statement: str
    solution_architecture: str
    quantified_results: Dict[str, Any]
    executive_testimonial: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "client_industry": self.client_industry,
            "organization_profile": self.organization_profile,
            "problem_statement": self.problem_statement,
            "solution_architecture": self.solution_architecture,
            "quantified_results": self.quantified_results,
            "executive_testimonial": self.executive_testimonial,
        }


@dataclass
class MasterBusinessValueScore:
    automation_score: float      # Weight: 25%
    roi_score: float             # Weight: 30%
    efficiency_score: float      # Weight: 25%
    adoption_score: float        # Weight: 20%
    overall_business_score: float
    grade: str
    validation_status: str
    evaluated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "automation_score": round(self.automation_score, 1),
            "roi_score": round(self.roi_score, 1),
            "efficiency_score": round(self.efficiency_score, 1),
            "adoption_score": round(self.adoption_score, 1),
            "overall_business_score": round(self.overall_business_score, 1),
            "grade": self.grade,
            "validation_status": self.validation_status,
            "evaluated_at": self.evaluated_at,
        }
