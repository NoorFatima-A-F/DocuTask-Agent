"""Part B: Customer Onboarding Experience Engine."""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid
from ..domain.interfaces import IOnboardingEngine
from ..domain.models import (
    IndustrySector,
    OnboardingJourney,
    OnboardingStep,
    OnboardingStepStatus,
)


class CustomerOnboardingEngine(IOnboardingEngine):
    """Manages the 7-step rapid enterprise onboarding wizard."""

    STEP_DEFINITIONS = [
        (1, "Create Organization Profile", "Set up enterprise tenant, primary domain, and admin credentials"),
        (2, "Select Industry & Department", "Tailor regulatory compliance frameworks and baseline departmental taxonomy"),
        (3, "Choose Automation Template", "Select turnkey pre-configured workflow from AI Automation Marketplace"),
        (4, "Connect Data Sources & Storage", "Authenticate Gmail/Outlook, Slack, and cloud storage providers (S3/Drive)"),
        (5, "Configure AI Agents & Guardrails", "Set hallucination thresholds, prompt versions, and model tier allocation"),
        (6, "Set Approval & Escalation Rules", "Establish confidence thresholds for human-in-the-loop exception routing"),
        (7, "Run Test Workflow & Live Activation", "Execute synthetic dry-run verification and enable production queue processing"),
    ]

    def __init__(self):
        self._journeys: Dict[str, OnboardingJourney] = {}

    def start_onboarding(self, company_name: str, industry: str) -> OnboardingJourney:
        journey_id = f"ONBOARD-{uuid.uuid4().hex[:8].upper()}"
        tenant_id = f"TENANT-{uuid.uuid4().hex[:6].upper()}"

        try:
            sector = IndustrySector(industry)
        except ValueError:
            sector = IndustrySector.FINANCE

        steps = [
            OnboardingStep(
                step_number=num,
                title=title,
                description=desc,
                status=OnboardingStepStatus.IN_PROGRESS if num == 1 else OnboardingStepStatus.PENDING,
            )
            for num, title, desc in self.STEP_DEFINITIONS
        ]

        journey = OnboardingJourney(
            journey_id=journey_id,
            tenant_id=tenant_id,
            company_name=company_name,
            industry=sector,
            current_step=1,
            total_steps=len(self.STEP_DEFINITIONS),
            steps=steps,
            is_completed=False,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        self._journeys[journey_id] = journey
        return journey

    def advance_step(self, journey_id: str, step_data: Dict[str, Any]) -> OnboardingJourney:
        journey = self._journeys.get(journey_id)
        if not journey:
            raise KeyError(f"Onboarding journey '{journey_id}' not found")

        current_idx = journey.current_step - 1
        if current_idx < len(journey.steps):
            journey.steps[current_idx].status = OnboardingStepStatus.COMPLETED
            journey.steps[current_idx].completed_at = datetime.now(timezone.utc).isoformat()
            journey.steps[current_idx].output_data = step_data

        if journey.current_step < journey.total_steps:
            journey.current_step += 1
            journey.steps[journey.current_step - 1].status = OnboardingStepStatus.IN_PROGRESS
        else:
            journey.is_completed = True
            journey.completed_at = datetime.now(timezone.utc).isoformat()

        return journey

    def get_journey(self, journey_id: str) -> Optional[OnboardingJourney]:
        return self._journeys.get(journey_id)
