"""
Universal Tool Registry Engine for Phase 13.15.
Manages tool definitions, JSON schemas, rate limits, health checks, and capability taxonomy.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import re
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.execution.events.execution_events import (
    ExecutionEvent,
    ExecutionEventType,
    RiskLevel,
    ToolStatus,
    ToolType,
    execution_event_bus,
)


@dataclass
class ToolParameter:
    name: str
    param_type: str  # string, integer, float, boolean, object, array
    description: str
    required: bool = True
    default: Optional[Any] = None
    enum_values: Optional[List[str]] = None
    validation_regex: Optional[str] = None

    def validate(self, value: Any) -> tuple[bool, Optional[str]]:
        if value is None:
            if self.required:
                return False, f"Parameter '{self.name}' is required."
            return True, None

        # Type checks
        if self.param_type == "string" and not isinstance(value, str):
            return False, f"Parameter '{self.name}' must be a string."
        elif self.param_type == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
            return False, f"Parameter '{self.name}' must be an integer."
        elif self.param_type == "float" and not isinstance(value, (int, float)):
            return False, f"Parameter '{self.name}' must be a number."
        elif self.param_type == "boolean" and not isinstance(value, bool):
            return False, f"Parameter '{self.name}' must be a boolean."
        elif self.param_type == "object" and not isinstance(value, dict):
            return False, f"Parameter '{self.name}' must be a JSON object."
        elif self.param_type == "array" and not isinstance(value, list):
            return False, f"Parameter '{self.name}' must be a list."

        # Enum checks
        if self.enum_values and value not in self.enum_values:
            return False, f"Parameter '{self.name}' value '{value}' not in allowed options: {self.enum_values}"

        # Regex checks
        if self.validation_regex and isinstance(value, str):
            if not re.match(self.validation_regex, value):
                return False, f"Parameter '{self.name}' does not match pattern {self.validation_regex}"

        return True, None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "param_type": self.param_type,
            "description": self.description,
            "required": self.required,
            "default": self.default,
            "enum_values": self.enum_values,
            "validation_regex": self.validation_regex,
        }


@dataclass
class ToolDefinition:
    tool_id: str
    name: str
    version: str
    description: str
    tool_type: ToolType
    category: str
    parameters: List[ToolParameter] = field(default_factory=list)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    rate_limit_per_min: int = 60
    timeout_seconds: int = 30
    concurrency_limit: int = 10
    risk_level: RiskLevel = RiskLevel.LOW
    requires_approval: bool = False
    is_idempotent: bool = True
    supports_compensation: bool = True
    compensation_tool_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    status: ToolStatus = ToolStatus.ACTIVE
    health_score: float = 1.0  # 0.0 to 1.0
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    average_latency_ms: float = 45.0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def validate_inputs(self, inputs: Dict[str, Any]) -> tuple[bool, List[str]]:
        errors = []
        for param in self.parameters:
            val = inputs.get(param.name, param.default)
            valid, err = param.validate(val)
            if not valid and err:
                errors.append(err)
        return len(errors) == 0, errors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tool_id": self.tool_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "tool_type": self.tool_type.value if isinstance(self.tool_type, ToolType) else str(self.tool_type),
            "category": self.category,
            "parameters": [p.to_dict() for p in self.parameters],
            "output_schema": self.output_schema,
            "rate_limit_per_min": self.rate_limit_per_min,
            "timeout_seconds": self.timeout_seconds,
            "concurrency_limit": self.concurrency_limit,
            "risk_level": self.risk_level.value if isinstance(self.risk_level, RiskLevel) else str(self.risk_level),
            "requires_approval": self.requires_approval,
            "is_idempotent": self.is_idempotent,
            "supports_compensation": self.supports_compensation,
            "compensation_tool_id": self.compensation_tool_id,
            "tags": self.tags,
            "status": self.status.value if isinstance(self.status, ToolStatus) else str(self.status),
            "health_score": round(self.health_score, 3),
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "failed_calls": self.failed_calls,
            "average_latency_ms": round(self.average_latency_ms, 2),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class ToolRegistryEngine:
    """Manages full lifecycle of real-world tools."""

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}
        self._initialize_default_tools()

    def _initialize_default_tools(self) -> None:
        """Seed a rich suite of built-in real world tools."""
        seed_tools = [
            ToolDefinition(
                tool_id="github_create_pull_request",
                name="GitHub Create Pull Request",
                version="1.2.0",
                description="Creates an automated pull request with code diffs, branches, and review labels on GitHub.",
                tool_type=ToolType.SAAS,
                category="code_repository",
                risk_level=RiskLevel.MEDIUM,
                is_idempotent=False,
                supports_compensation=True,
                compensation_tool_id="github_close_pull_request",
                tags=["github", "git", "ci_cd", "code"],
                parameters=[
                    ToolParameter("repo", "string", "Repository in 'owner/repo' format", True),
                    ToolParameter("title", "string", "Title of the pull request", True),
                    ToolParameter("head", "string", "Branch containing changes", True),
                    ToolParameter("base", "string", "Target branch", True, default="main"),
                    ToolParameter("body", "string", "Markdown description of changes", False, default=""),
                ],
                output_schema={"pr_number": "integer", "pr_url": "string", "state": "string"},
            ),
            ToolDefinition(
                tool_id="github_close_pull_request",
                name="GitHub Close Pull Request",
                version="1.0.0",
                description="Closes an existing GitHub PR without merging as part of a rollback.",
                tool_type=ToolType.SAAS,
                category="code_repository",
                risk_level=RiskLevel.LOW,
                is_idempotent=True,
                supports_compensation=False,
                tags=["github", "git", "compensation"],
                parameters=[
                    ToolParameter("repo", "string", "Repository in 'owner/repo' format", True),
                    ToolParameter("pr_number", "integer", "Pull request number to close", True),
                ],
                output_schema={"status": "string", "closed": "boolean"},
            ),
            ToolDefinition(
                tool_id="slack_send_channel_message",
                name="Slack Post Message",
                version="2.0.0",
                description="Dispatches formatted executive alerts or operational notifications to Slack channels.",
                tool_type=ToolType.SAAS,
                category="communication",
                risk_level=RiskLevel.LOW,
                is_idempotent=False,
                supports_compensation=True,
                compensation_tool_id="slack_delete_channel_message",
                tags=["slack", "chat", "messaging", "alert"],
                parameters=[
                    ToolParameter("channel", "string", "Target Slack channel (e.g. #ops-war-room)", True),
                    ToolParameter("message", "string", "Message markdown payload", True),
                    ToolParameter("priority", "string", "Urgency level", False, default="normal", enum_values=["low", "normal", "high", "urgent"]),
                ],
                output_schema={"message_ts": "string", "channel_id": "string", "delivered": "boolean"},
            ),
            ToolDefinition(
                tool_id="k8s_scale_deployment",
                name="Kubernetes Scale Deployment",
                version="1.5.0",
                description="Scales replica count for target microservices in a Kubernetes namespace.",
                tool_type=ToolType.KUBERNETES,
                category="infrastructure",
                risk_level=RiskLevel.HIGH,
                requires_approval=True,
                is_idempotent=True,
                supports_compensation=True,
                compensation_tool_id="k8s_scale_deployment",
                tags=["kubernetes", "k8s", "scaling", "devops", "cloud"],
                parameters=[
                    ToolParameter("namespace", "string", "Kubernetes namespace", True, default="production"),
                    ToolParameter("deployment_name", "string", "Name of the deployment", True),
                    ToolParameter("replicas", "integer", "Desired replica count", True),
                ],
                output_schema={"namespace": "string", "deployment": "string", "previous_replicas": "integer", "new_replicas": "integer"},
            ),
            ToolDefinition(
                tool_id="playwright_web_scraper",
                name="Playwright Browser Navigator",
                version="3.1.0",
                description="Launches headless browser, navigates to target URL, evaluates DOM selectors, extracts dynamic data, and captures page screenshot.",
                tool_type=ToolType.BROWSER,
                category="browser_vision",
                risk_level=RiskLevel.LOW,
                is_idempotent=True,
                supports_compensation=False,
                tags=["browser", "playwright", "scraping", "automation", "dom"],
                parameters=[
                    ToolParameter("url", "string", "Full HTTPS URL to navigate", True),
                    ToolParameter("extract_selector", "string", "CSS selector to extract", False, default="body"),
                    ToolParameter("capture_screenshot", "boolean", "Capture visual base64 snapshot", False, default=True),
                    ToolParameter("wait_until", "string", "Navigation wait state", False, default="networkidle", enum_values=["load", "domcontentloaded", "networkidle"]),
                ],
                output_schema={"title": "string", "extracted_text": "string", "status_code": "integer", "screenshot_base64": "string"},
            ),
            ToolDefinition(
                tool_id="postgres_execute_query",
                name="PostgreSQL Query Executor",
                version="1.4.0",
                description="Executes parametrized read or transactional SQL queries against production / warehouse Postgres databases.",
                tool_type=ToolType.DATABASE,
                category="database",
                risk_level=RiskLevel.MEDIUM,
                is_idempotent=False,
                supports_compensation=True,
                tags=["postgres", "sql", "database", "analytics"],
                parameters=[
                    ToolParameter("connection_id", "string", "Connector identifier for database", True),
                    ToolParameter("query", "string", "SQL query text (SELECT / INSERT / UPDATE)", True),
                    ToolParameter("params", "object", "Query parameters dictionary", False, default={}),
                ],
                output_schema={"rows_affected": "integer", "data": "array", "execution_time_ms": "float"},
            ),
            ToolDefinition(
                tool_id="aws_s3_upload_artifact",
                name="AWS S3 Artifact Publisher",
                version="2.1.0",
                description="Uploads generated documents, models, and execution evidence to secure AWS S3 bucket.",
                tool_type=ToolType.CLOUD_SDK,
                category="cloud",
                risk_level=RiskLevel.LOW,
                is_idempotent=True,
                supports_compensation=True,
                compensation_tool_id="aws_s3_delete_artifact",
                tags=["aws", "s3", "storage", "cloud"],
                parameters=[
                    ToolParameter("bucket", "string", "Target S3 bucket name", True),
                    ToolParameter("key", "string", "Target object key path", True),
                    ToolParameter("content_type", "string", "MIME type", False, default="application/json"),
                    ToolParameter("payload", "string", "Content payload to store", True),
                ],
                output_schema={"etag": "string", "s3_uri": "string", "size_bytes": "integer"},
            ),
            ToolDefinition(
                tool_id="stripe_create_customer_invoice",
                name="Stripe Create Customer Invoice",
                version="1.1.0",
                description="Generates an enterprise itemized customer invoice through the Stripe Billing API.",
                tool_type=ToolType.SAAS,
                category="payment_finance",
                risk_level=RiskLevel.HIGH,
                requires_approval=True,
                is_idempotent=False,
                supports_compensation=True,
                tags=["stripe", "billing", "finance", "invoice"],
                parameters=[
                    ToolParameter("customer_id", "string", "Stripe customer identifier (cus_*)", True),
                    ToolParameter("amount_cents", "integer", "Invoice total amount in cents", True),
                    ToolParameter("currency", "string", "ISO currency code (usd, eur, gbp)", False, default="usd"),
                    ToolParameter("description", "string", "Service rendered summary", True),
                ],
                output_schema={"invoice_id": "string", "hosted_invoice_url": "string", "status": "string", "total_cents": "integer"},
            ),
            ToolDefinition(
                tool_id="rest_api_universal_caller",
                name="Universal REST API Client",
                version="2.0.0",
                description="Dispatches authenticated HTTP/REST requests (GET, POST, PUT, DELETE, PATCH) to any remote endpoint.",
                tool_type=ToolType.REST_API,
                category="custom_api",
                risk_level=RiskLevel.MEDIUM,
                is_idempotent=False,
                supports_compensation=False,
                tags=["rest", "http", "api", "universal"],
                parameters=[
                    ToolParameter("url", "string", "Target HTTP URL", True),
                    ToolParameter("method", "string", "HTTP Method", True, default="POST", enum_values=["GET", "POST", "PUT", "PATCH", "DELETE"]),
                    ToolParameter("headers", "object", "HTTP headers dictionary", False, default={}),
                    ToolParameter("body", "object", "JSON body payload", False, default={}),
                ],
                output_schema={"status_code": "integer", "response_body": "object", "headers": "object"},
            ),
        ]

        for t in seed_tools:
            self._tools[t.tool_id] = t

    def register_tool(self, tool_def: ToolDefinition) -> ToolDefinition:
        """Register or update a tool definition."""
        self._tools[tool_def.tool_id] = tool_def
        execution_event_bus.publish(
            ExecutionEvent(
                event_type=ExecutionEventType.TOOL_REGISTERED,
                source="tool_registry",
                payload={"tool_id": tool_def.tool_id, "name": tool_def.name, "category": tool_def.category},
                risk_level=tool_def.risk_level,
            )
        )
        return tool_def

    def get_tool(self, tool_id: str) -> Optional[ToolDefinition]:
        return self._tools.get(tool_id)

    def list_tools(
        self,
        category: Optional[str] = None,
        tool_type: Optional[str] = None,
        risk_level: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[ToolDefinition]:
        results = list(self._tools.values())
        if category:
            results = [t for t in results if t.category.lower() == category.lower()]
        if tool_type:
            results = [t for t in results if (t.tool_type.value if isinstance(t.tool_type, ToolType) else str(t.tool_type)).lower() == tool_type.lower()]
        if risk_level:
            results = [t for t in results if (t.risk_level.value if isinstance(t.risk_level, RiskLevel) else str(t.risk_level)).lower() == risk_level.lower()]
        if search:
            query = search.lower()
            results = [
                t for t in results
                if query in t.name.lower() or query in t.description.lower() or any(query in tag.lower() for tag in t.tags)
            ]
        return results

    def record_tool_call(self, tool_id: str, success: bool, latency_ms: float) -> None:
        tool = self.get_tool(tool_id)
        if not tool:
            return
        tool.total_calls += 1
        if success:
            tool.successful_calls += 1
        else:
            tool.failed_calls += 1

        # Exponential moving average for latency
        tool.average_latency_ms = (tool.average_latency_ms * 0.8) + (latency_ms * 0.2)
        # Recalculate health score
        if tool.total_calls > 0:
            success_rate = tool.successful_calls / tool.total_calls
            tool.health_score = max(0.0, min(1.0, success_rate * (1.0 if tool.average_latency_ms < 500 else 0.9)))
        tool.updated_at = datetime.now(timezone.utc).isoformat()

    def get_stats(self) -> Dict[str, Any]:
        tools = list(self._tools.values())
        total = len(tools)
        active = sum(1 for t in tools if t.status == ToolStatus.ACTIVE)
        categories = {}
        for t in tools:
            categories[t.category] = categories.get(t.category, 0) + 1
        total_calls = sum(t.total_calls for t in tools)
        avg_health = sum(t.health_score for t in tools) / total if total > 0 else 1.0

        return {
            "total_tools": total,
            "active_tools": active,
            "categories_breakdown": categories,
            "total_executions": total_calls,
            "average_health_score": round(avg_health, 3),
        }


# Global Singleton
tool_registry_engine = ToolRegistryEngine()
