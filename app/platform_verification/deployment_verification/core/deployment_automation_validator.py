"""
Deployment Automation & Manual Operation Auditor.
"""
from typing import List, Dict, Any
from app.platform_verification.deployment_verification.domain.models import DeploymentAutomationReport
from app.platform_verification.deployment_verification.domain.interfaces import IDeploymentAutomationValidator


class DeploymentAutomationValidator(IDeploymentAutomationValidator):
    """Verifies 100% automated release steps and rejects manual operational interventions."""

    FORBIDDEN_MANUAL_STEPS = {"manual_ssh", "manual_db_seed", "manual_env_edit", "server_package_install"}

    def validate_automation(self, pipeline_steps: List[Dict[str, Any]]) -> DeploymentAutomationReport:
        manual_detected: List[str] = []
        for step in pipeline_steps:
            action = step.get("action", "")
            if step.get("is_manual", False) or action in self.FORBIDDEN_MANUAL_STEPS:
                manual_detected.append(f"Step '{step.get('name', action)}' requires manual intervention")

        total = len(pipeline_steps)
        auto_count = total - len(manual_detected)
        pct = (auto_count / max(total, 1)) * 100.0
        status = "PASS" if len(manual_detected) == 0 else "FAIL"

        return DeploymentAutomationReport(
            total_steps=total,
            automated_steps=auto_count,
            manual_steps_detected=manual_detected,
            automation_percentage=round(pct, 2),
            status=status,
        )
