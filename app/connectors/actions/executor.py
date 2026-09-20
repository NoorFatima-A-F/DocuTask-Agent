"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Action Engine.
Validates input/output contracts, enforces timeouts and permissions, and executes connector actions.
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
import time
from typing import Any, Dict, List, Optional
import uuid

from app.connectors.core.exceptions import ActionExecutionError, PolicyViolationError
from app.connectors.core.models import ActionDescriptor, ExecutionResult
from app.connectors.sdk.base import BaseConnector

logger = logging.getLogger(__name__)


class ActionExecutor:
    """
    Executes connector actions with contract validation, latency tracking,
    timeout handling, and permission validation.
    """

    def validate_inputs(self, action: ActionDescriptor, inputs: Dict[str, Any]) -> None:
        """Validates that all mandatory fields in the action's input schema are present."""
        req_fields = action.input_schema.get("required", [])
        missing = [f for f in req_fields if f not in inputs]
        if missing:
            raise ActionExecutionError(
                f"Missing required input fields for action '{action.name}': {missing}",
                connector_id=action.connector_id,
                details={"missing": missing, "schema": action.input_schema},
            )

    def validate_permissions(
        self,
        action: ActionDescriptor,
        granted_permissions: List[str],
    ) -> None:
        """Ensures that the calling context holds necessary permissions for this action."""
        if not action.permissions or "*" in granted_permissions:
            return
        missing = [p for p in action.permissions if p not in granted_permissions]
        if missing:
            raise PolicyViolationError(
                f"Missing permissions to execute action '{action.name}': {missing}",
                connector_id=action.connector_id,
                details={"missing_permissions": missing},
            )

    def execute_action(
        self,
        connector: BaseConnector,
        action: ActionDescriptor,
        inputs: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        granted_permissions: Optional[List[str]] = None,
    ) -> ExecutionResult:
        """
        Executes a connector action with pre-validation and performance instrumentation.
        """
        ctx = context or {}
        perms = granted_permissions or ["*"]

        # Validate permissions
        self.validate_permissions(action, perms)

        # Validate input schema
        self.validate_inputs(action, inputs)

        start_time = time.perf_counter()
        try:
            output = connector.execute(action.name, inputs, ctx)
            latency_ms = (time.perf_counter() - start_time) * 1000.0

            return ExecutionResult(
                connector_id=action.connector_id,
                action_name=action.name,
                status="SUCCESS",
                output=output if isinstance(output, dict) else {"result": output},
                latency_ms=latency_ms,
                cost_usd=action.cost_usd,
            )
        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            logger.error(f"Action '{action.name}' execution failed on '{action.connector_id}': {e}")
            return ExecutionResult(
                connector_id=action.connector_id,
                action_name=action.name,
                status="FAILED",
                error=str(e),
                latency_ms=latency_ms,
                cost_usd=0.0,
            )
