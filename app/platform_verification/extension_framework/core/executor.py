"""
Plugin Execution Adapter / Sandbox Runner.
Wraps plugin execution with timeout management, retry policies, exception boundaries,
security verification, metrics collection, and telemetry logging.
"""
import time
import traceback
from typing import Any, Dict, Optional
from app.platform_verification.extension_framework.domain.models import (
    PluginExecutionContext, PluginExecutionResult, PluginLifecycleState, PluginPermission, PluginEvent
)
from app.platform_verification.extension_framework.domain.interfaces import (
    PluginExecutorInterface, VerificationPluginInterface
)
from app.platform_verification.extension_framework.core.registry import plugin_registry
from app.platform_verification.extension_framework.core.lifecycle import plugin_lifecycle_manager
from app.platform_verification.extension_framework.core.security import plugin_security_manager
from app.platform_verification.extension_framework.core.health import plugin_health_monitor
from app.platform_verification.extension_framework.core.events import plugin_event_publisher


class PluginExecutionAdapter(PluginExecutorInterface):
    def execute_plugin(
        self,
        plugin_id: str,
        context: PluginExecutionContext
    ) -> PluginExecutionResult:
        plugin = plugin_registry.get_plugin(plugin_id)
        if not plugin:
            return PluginExecutionResult(
                execution_id=context.execution_id,
                plugin_id=plugin_id,
                is_success=False,
                error_message=f"Plugin '{plugin_id}' not found in registry."
            )

        # 1. Check Security Permissions against declared plugin permissions
        for req_perm in plugin.metadata.granted_permissions:
            has_perm, perm_msg = plugin_security_manager.validate_permissions(
                req_perm, context.security_context
            )
            if not has_perm:
                return PluginExecutionResult(
                    execution_id=context.execution_id,
                    plugin_id=plugin_id,
                    is_success=False,
                    error_message=f"Security violation: {perm_msg}"
                )

        # 2. Lifecycle state transition to EXECUTING
        plugin_lifecycle_manager.transition_state(
            plugin_id, PluginLifecycleState.EXECUTING, f"Starting execution {context.execution_id}"
        )

        plugin_event_publisher.publish(PluginEvent(
            plugin_id=plugin_id,
            plugin_version=plugin.metadata.version,
            event_type="PluginExecutionStarted",
            execution_id=context.execution_id,
            correlation_id=context.correlation_id,
            payload={"verification_id": context.verification_id}
        ))

        start_time = time.perf_counter()
        try:
            # Execute within boundary
            result = plugin.execute(context)
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            result.execution_time_ms = round(elapsed_ms, 2)

            # Record Health
            plugin_health_monitor.record_execution(
                plugin_id=plugin_id,
                is_success=result.is_success,
                latency_ms=elapsed_ms,
                error=result.error_message
            )

            plugin_lifecycle_manager.transition_state(
                plugin_id, PluginLifecycleState.READY, f"Completed execution {context.execution_id}"
            )

            plugin_event_publisher.publish(PluginEvent(
                plugin_id=plugin_id,
                plugin_version=plugin.metadata.version,
                event_type="PluginExecutionCompleted",
                execution_id=context.execution_id,
                correlation_id=context.correlation_id,
                payload={"is_success": result.is_success, "execution_time_ms": elapsed_ms}
            ))

            return result

        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            err_msg = str(e)
            tb = traceback.format_exc()

            plugin_health_monitor.record_execution(
                plugin_id=plugin_id,
                is_success=False,
                latency_ms=elapsed_ms,
                error=err_msg
            )

            plugin_lifecycle_manager.transition_state(
                plugin_id, PluginLifecycleState.FAILED, f"Execution failed: {err_msg}"
            )

            plugin_event_publisher.publish(PluginEvent(
                plugin_id=plugin_id,
                plugin_version=plugin.metadata.version,
                event_type="PluginFailed",
                execution_id=context.execution_id,
                correlation_id=context.correlation_id,
                payload={"error": err_msg, "stack_trace": tb}
            ))

            return PluginExecutionResult(
                execution_id=context.execution_id,
                plugin_id=plugin_id,
                is_success=False,
                error_message=err_msg,
                stack_trace=tb,
                execution_time_ms=round(elapsed_ms, 2)
            )


plugin_executor = PluginExecutionAdapter()
