"""
Composable Business & Decision Rules Engine Models.
Defines BusinessRule, DecisionRule, ValidationRule, SecurityRule, ComplianceRule,
CostRule, RoutingRule, WorkflowRule, PlannerRule, ToolRule, ExecutionRule, and RuleGroup.
Supports AND/OR/NOT rule composition, nested groups, priority ranking, dependencies,
versioning, activation windows, and feature flags.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class BusinessRule(BaseModel):
    """Composable Base Business Rule specification."""

    rule_id: str
    name: str
    rule_type: str = Field(default="BUSINESS")  # BUSINESS, SECURITY, COMPLIANCE, COST, VALIDATION, ROUTING, WORKFLOW, PLANNER, TOOL, EXECUTION
    priority: int = Field(default=100, ge=1)
    is_active: bool = Field(default=True)
    version: str = Field(default="v1.0")
    condition_expression: str = Field(default="True")
    action_type: str = Field(default="ALLOW")  # ALLOW, DENY, REQUIRE_APPROVAL, RE_ROUTE
    dependencies: List[str] = Field(default_factory=list)
    feature_flag: Optional[str] = Field(default=None)
    activation_start: Optional[datetime] = Field(default=None)
    activation_end: Optional[datetime] = Field(default=None)
    parameters: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class DecisionRule(BusinessRule):
    """Decision Evaluation Rule."""
    rule_type: str = Field(default="DECISION")


class ValidationRule(BusinessRule):
    """Data and Context Validation Rule."""
    rule_type: str = Field(default="VALIDATION")


class SecurityRule(BusinessRule):
    """Access Control and Zero-Trust Security Rule."""
    rule_type: str = Field(default="SECURITY")


class ComplianceRule(BusinessRule):
    """Regulatory and Data Residency Compliance Rule."""
    rule_type: str = Field(default="COMPLIANCE")


class CostRule(BusinessRule):
    """Financial and Budget Enforcement Rule."""
    rule_type: str = Field(default="COST")


class RoutingRule(BusinessRule):
    """Agent and Task Routing Rule."""
    rule_type: str = Field(default="ROUTING")


class WorkflowRule(BusinessRule):
    """DAG and Orchestration Workflow Rule."""
    rule_type: str = Field(default="WORKFLOW")


class PlannerRule(BusinessRule):
    """Planning Constraint and Decomposition Rule."""
    rule_type: str = Field(default="PLANNER")


class ToolRule(BusinessRule):
    """Tool Selection and Execution Quota Rule."""
    rule_type: str = Field(default="TOOL")


class ExecutionRule(BusinessRule):
    """Task Dispatch and Execution Safety Rule."""
    rule_type: str = Field(default="EXECUTION")


class RuleGroup(BaseModel):
    """Composable group of rules evaluating via logical operator."""

    group_id: str
    operator: str = Field(default="AND")  # AND, OR, NOT
    rules: List[BusinessRule] = Field(default_factory=list)
    nested_groups: List["RuleGroup"] = Field(default_factory=list)

    model_config = {"frozen": True}
