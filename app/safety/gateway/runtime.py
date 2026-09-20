"""Safety Gateway & Runtime Execution Facade."""

from typing import Optional, Dict, Any, List
from .context import SafetyContext, ToolContext
from .decision import SafetyDecision, SafetyStatus, ViolationSeverity, SafetyCategory
from .pipeline import SafetyPipeline
from ..incidents.manager import SafetyIncidentManager
from ..events.publisher import (
    SafetyEventPublisher,
    SafetyGatewayDecisionEvent,
    PromptInjectionDetectedEvent,
    JailbreakAttemptEvent,
    PIILeakageBlockedEvent,
    ToolSafetyViolationEvent,
    HallucinationDetectedEvent,
    SafetyIncidentCreatedEvent,
)
from ..policies.integration import SafetyPolicyBridge, TenantSafetyPolicy


class SafetyGateway:
    """Enterprise AI Safety Gateway orchestrating all runtime defenses, incident creation, and telemetry events."""

    def __init__(
        self,
        pipeline: Optional[SafetyPipeline] = None,
        incident_manager: Optional[SafetyIncidentManager] = None,
        event_publisher: Optional[SafetyEventPublisher] = None,
        policy_bridge: Optional[SafetyPolicyBridge] = None,
    ):
        self.pipeline = pipeline or SafetyPipeline()
        self.incident_manager = incident_manager or SafetyIncidentManager()
        self.event_publisher = event_publisher or SafetyEventPublisher()
        self.policy_bridge = policy_bridge or SafetyPolicyBridge()

    def inspect_input(self, context: SafetyContext) -> SafetyDecision:
        """Inspects and guards user/document input before model inference."""
        policy = self.policy_bridge.get_policy(context.tenant_id)
        decision = self.pipeline.guard_input(context, policy)

        # Publish decision event
        self.event_publisher.publish(
            SafetyGatewayDecisionEvent(
                tenant_id=context.tenant_id,
                payload={
                    "stage": "INPUT",
                    "status": decision.status.value,
                    "risk_score": decision.composite_risk_score,
                    "violations_count": len(decision.violations),
                },
            )
        )

        # Handle incidents & specific events
        self._handle_violations(context, decision, stage="INPUT")
        return decision

    def inspect_tool(
        self,
        context: SafetyContext,
        tool_name: str,
        parameters: dict,
        user_role: str = "user",
        is_dry_run: bool = False,
    ) -> SafetyDecision:
        """Inspects and guards tool invocation before execution."""
        decision = self.pipeline.guard_tool(
            tool_name=tool_name,
            parameters=parameters,
            user_role=user_role,
            is_dry_run=is_dry_run,
        )

        self.event_publisher.publish(
            SafetyGatewayDecisionEvent(
                tenant_id=context.tenant_id,
                payload={
                    "stage": "TOOL",
                    "tool_name": tool_name,
                    "status": decision.status.value,
                },
            )
        )

        if not decision.is_allowed:
            self.event_publisher.publish(
                ToolSafetyViolationEvent(
                    tenant_id=context.tenant_id,
                    payload={"tool_name": tool_name, "violations": [v.model_dump() for v in decision.violations]},
                )
            )

        return decision

    def inspect_output(self, context: SafetyContext) -> SafetyDecision:
        """Inspects and sanitizes model output before delivery to user."""
        policy = self.policy_bridge.get_policy(context.tenant_id)
        decision = self.pipeline.guard_output(context, policy)

        self.event_publisher.publish(
            SafetyGatewayDecisionEvent(
                tenant_id=context.tenant_id,
                payload={
                    "stage": "OUTPUT",
                    "status": decision.status.value,
                    "risk_score": decision.composite_risk_score,
                    "violations_count": len(decision.violations),
                },
            )
        )

        self._handle_violations(context, decision, stage="OUTPUT")
        return decision

    def _handle_violations(self, context: SafetyContext, decision: SafetyDecision, stage: str):
        for v in decision.violations:
            if v.category == SafetyCategory.PROMPT_INJECTION:
                self.event_publisher.publish(
                    PromptInjectionDetectedEvent(
                        tenant_id=context.tenant_id,
                        payload={"evidence": v.evidence, "severity": v.severity.value, "stage": stage},
                    )
                )
            elif v.category == SafetyCategory.JAILBREAK:
                self.event_publisher.publish(
                    JailbreakAttemptEvent(
                        tenant_id=context.tenant_id,
                        payload={"evidence": v.evidence, "severity": v.severity.value, "stage": stage},
                    )
                )
            elif v.category in [SafetyCategory.PII_LEAKAGE, SafetyCategory.SECRET_LEAKAGE]:
                self.event_publisher.publish(
                    PIILeakageBlockedEvent(
                        tenant_id=context.tenant_id,
                        payload={"message": v.message, "severity": v.severity.value, "stage": stage},
                    )
                )
            elif v.category in [SafetyCategory.HALLUCINATION, SafetyCategory.GROUNDING_FAILURE]:
                self.event_publisher.publish(
                    HallucinationDetectedEvent(
                        tenant_id=context.tenant_id,
                        payload={"message": v.message, "severity": v.severity.value, "stage": stage},
                    )
                )

        # Create incident if critical or multiple high violations
        if decision.has_critical_violations or len([v for v in decision.violations if v.severity == ViolationSeverity.HIGH]) >= 2:
            incident = self.incident_manager.create_incident(
                tenant_id=context.tenant_id,
                title=f"AI Safety Violation in {stage} Phase",
                description=f"Automated safety barrier triggered with {len(decision.violations)} violations",
                category=decision.violations[0].category if decision.violations else SafetyCategory.POLICY_VIOLATION,
                severity=decision.highest_severity or ViolationSeverity.HIGH,
                context_id=context.context_id,
                user_id=context.user_id,
                agent_id=context.agent_id,
                violations=decision.violations,
            )
            self.event_publisher.publish(
                SafetyIncidentCreatedEvent(
                    tenant_id=context.tenant_id,
                    payload={"incident_id": incident.incident_id, "severity": incident.severity.value},
                )
            )


# Alias for SafetyRuntime
SafetyRuntime = SafetyGateway
