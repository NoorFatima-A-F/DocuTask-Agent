"""Part I: 1-Click Interactive Enterprise Demo Engine."""

from datetime import datetime, timezone
import time
from typing import Any, Dict, List
import uuid
from ..domain.interfaces import IDemoEngine
from ..domain.models import (
    DemoRunResult,
    DemoStepEvent,
    SimulationRunStatus,
)


class InteractiveDemoEngine(IDemoEngine):
    """Executes high-fidelity, deterministic 1-click enterprise automation simulations for live demonstrations."""

    SCENARIOS = {
        "invoice_automation": {
            "name": "Enterprise Accounts Payable Autonomous Invoice Processing",
            "document_sample": {
                "file_name": "INV_2026_AcmeSolutions.pdf",
                "vendor": "Acme Global Solutions Inc.",
                "invoice_number": "INV-2026-8891",
                "total_amount": 14500.50,
                "tax_amount": 1160.04,
                "currency": "USD",
                "line_items_count": 8,
                "po_number": "PO-9912",
            },
            "steps": [
                ("STAGE-1", "Ingestion & Security Pre-flight", 45.0, "SecurityGuardAgent", "Validated TLS transmission, verified digital signature, and sanitized malicious macros."),
                ("STAGE-2", "Multimodal Layout OCR Extraction", 82.0, "MultimodalOCRAgent", "Extracted 2D bounding boxes, recognized tables, and normalized character confidence (0.998)."),
                ("STAGE-3", "LLM Reasoning & Schema Grounding", 95.0, "ReasoningExtractionAgent", "Mapped raw fields to canonical AP schema with 99.4% faithfulness and 0% hallucination."),
                ("STAGE-4", "3-Way PO Matching & Policy Verification", 38.0, "PolicyVerificationAgent", "Matched invoice total ($14,500.50) with NetSuite PO #PO-9912. Verified approved vendor list."),
                ("STAGE-5", "Human-in-the-Loop Fast-Track Signoff", 25.0, "SupervisionCoordinator", "Confidence > 95% satisfied. Fast-tracked automated supervisor sign-off with cryptographic audit log."),
                ("STAGE-6", "ERP Synchronization & Telemetry Dispatch", 32.0, "EnterpriseConnectorAgent", "Created Vendor Bill in QuickBooks Online (ID #QB-99812). Dispatched Slack notification."),
            ],
        },
        "resume_screening": {
            "name": "Candidate Resume Screening & Competency Matching",
            "document_sample": {
                "candidate_name": "Alex Rivera",
                "target_role": "Principal AI Automation Engineer",
                "experience_years": 9,
                "top_skills": ["Python", "Multi-Agent Systems", "FastAPI", "Kubernetes", "LLMOps"],
                "match_score": 96.5,
            },
            "steps": [
                ("STAGE-1", "Resume Parsing & Normalization", 40.0, "ResumeParserAgent", "Normalized PDF resume into structured candidate profile schema."),
                ("STAGE-2", "Skill Vector Matching & Ranking", 75.0, "VectorSearchAgent", "Computed semantic cosine similarity against Senior Role competency matrix (0.965)."),
                ("STAGE-3", "Interview Scheduling & Recruiter Alert", 30.0, "WorkflowCoordinatorAgent", "Created candidate profile in Greenhouse and triggered automated calendar invite."),
            ],
        },
    }

    def run_demo_scenario(self, scenario_key: str = "invoice_automation") -> DemoRunResult:
        scenario = self.SCENARIOS.get(scenario_key, self.SCENARIOS["invoice_automation"])
        run_id = f"DEMO-RUN-{uuid.uuid4().hex[:8].upper()}"
        trace_id = f"TRACE-{uuid.uuid4().hex[:12].upper()}"

        events: List[DemoStepEvent] = []
        total_time = 0.0

        for stage_id, stage_name, duration, agent_name, action_desc in scenario["steps"]:
            total_time += duration
            events.append(
                DemoStepEvent(
                    step_id=stage_id,
                    stage_name=stage_name,
                    status="COMPLETED",
                    duration_ms=duration,
                    agent_in_charge=agent_name,
                    action_description=action_desc,
                    artifacts_emitted={
                        "stage": stage_name,
                        "verified": True,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    },
                )
            )

        return DemoRunResult(
            demo_run_id=run_id,
            scenario_name=scenario["name"],
            status=SimulationRunStatus.COMPLETED,
            total_duration_ms=total_time,
            steps=events,
            extracted_fields=scenario["document_sample"],
            confidence_score=0.992,
            roi_summary={
                "processing_time_reduction": "99.5%",
                "unit_cost": "$0.025",
                "manual_cost_avoided": "$35.00",
                "status": "ENTERPRISE_READY",
            },
            audit_trace_id=trace_id,
        )
