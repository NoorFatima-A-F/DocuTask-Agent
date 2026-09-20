"""
Baseline vs Autonomous AI Process Models across core industry verticals.
"""

from typing import List, Dict, Any
from app.business_value_verification.domain.models import (
    IndustryVertical,
    ProcessStepType,
    WorkflowStep,
    ProcessModel,
    WorkflowComparison,
)


class WorkflowModelFactory:
    """Generates detailed baseline human workflows and AI-optimized workflows."""

    @classmethod
    def get_all_comparisons(cls) -> List[WorkflowComparison]:
        return [
            cls.get_invoice_comparison(),
            cls.get_contract_comparison(),
            cls.get_resume_comparison(),
            cls.get_healthcare_comparison(),
        ]

    @classmethod
    def get_invoice_comparison(cls) -> WorkflowComparison:
        baseline_steps = [
            WorkflowStep("Email Ingestion & Download", ProcessStepType.MANUAL, 60.0, 100.0, 1.2, 0.40),
            WorkflowStep("Manual Field & Table Data Entry", ProcessStepType.MANUAL, 480.0, 100.0, 4.5, 3.20),
            WorkflowStep("PO & Line Item Verification", ProcessStepType.MANUAL, 240.0, 100.0, 2.8, 1.60),
            WorkflowStep("Manager Approval Queue Routing", ProcessStepType.MANUAL, 180.0, 100.0, 0.5, 1.20),
            WorkflowStep("ERP Entry (QuickBooks / NetSuite)", ProcessStepType.MANUAL, 120.0, 100.0, 1.5, 0.80),
        ]
        baseline = ProcessModel(
            name="Manual Accounts Payable Processing",
            vertical=IndustryVertical.FINANCE,
            is_ai_system=False,
            steps=baseline_steps,
            total_duration_minutes=18.0,
            total_cost_usd=7.20,
            accuracy_pct=92.0,
            human_hours_per_1k_docs=300.0,
        )

        ai_steps = [
            WorkflowStep("Automated Ingestion & Webhook", ProcessStepType.AUTONOMOUS_AI, 0.5, 0.0, 0.01, 0.0005),
            WorkflowStep("Multimodal OCR & Layout Parsing", ProcessStepType.AUTONOMOUS_AI, 1.5, 0.0, 0.05, 0.0020),
            WorkflowStep("LLM Extraction & Grounding", ProcessStepType.AUTONOMOUS_AI, 1.8, 0.0, 0.10, 0.0040),
            WorkflowStep("Deterministic PO & Rule Matcher", ProcessStepType.AUTONOMOUS_AI, 0.4, 0.0, 0.02, 0.0005),
            WorkflowStep("Autonomous ERP Dispatch / HITL", ProcessStepType.AUTONOMOUS_AI, 0.3, 5.0, 0.05, 0.0010),
        ]
        ai_system = ProcessModel(
            name="DocuTask Autonomous Invoice Platform",
            vertical=IndustryVertical.FINANCE,
            is_ai_system=True,
            steps=ai_steps,
            total_duration_minutes=0.075,  # 4.5 seconds
            total_cost_usd=0.0080,
            accuracy_pct=99.4,
            human_hours_per_1k_docs=2.5,
        )

        return WorkflowComparison(
            workflow_name="Accounts Payable Invoice Processing",
            vertical=IndustryVertical.FINANCE,
            baseline=baseline,
            ai_system=ai_system,
            time_reduction_pct=99.58,
            cost_reduction_pct=99.89,
            human_effort_reduction_pct=99.17,
            accuracy_improvement_pct=8.04,
            speedup_multiplier=240.0,
        )

    @classmethod
    def get_contract_comparison(cls) -> WorkflowComparison:
        baseline = ProcessModel(
            name="Manual Legal Review & Redlining",
            vertical=IndustryVertical.LEGAL,
            is_ai_system=False,
            steps=[
                WorkflowStep("Contract Reading & Formatting", ProcessStepType.MANUAL, 600.0, 100.0, 2.0, 8.00),
                WorkflowStep("Clause Extraction & Risk Review", ProcessStepType.MANUAL, 1500.0, 100.0, 6.5, 20.00),
                WorkflowStep("Compliance Checklist Validation", ProcessStepType.MANUAL, 600.0, 100.0, 3.0, 7.00),
            ],
            total_duration_minutes=45.0,
            total_cost_usd=35.00,
            accuracy_pct=89.0,
            human_hours_per_1k_docs=750.0,
        )

        ai_system = ProcessModel(
            name="DocuTask Legal Contract Analysis Agent",
            vertical=IndustryVertical.LEGAL,
            is_ai_system=True,
            steps=[
                WorkflowStep("Multi-page Layout Parsing", ProcessStepType.AUTONOMOUS_AI, 2.5, 0.0, 0.1, 0.006),
                WorkflowStep("Clause & Entity Extraction", ProcessStepType.AUTONOMOUS_AI, 3.5, 0.0, 0.1, 0.012),
                WorkflowStep("Risk Classification & Redline Agent", ProcessStepType.AUTONOMOUS_AI, 2.0, 10.0, 0.2, 0.005),
            ],
            total_duration_minutes=0.133,  # 8.0 seconds
            total_cost_usd=0.0230,
            accuracy_pct=99.1,
            human_hours_per_1k_docs=8.0,
        )

        return WorkflowComparison(
            workflow_name="Commercial Contract & NDA Risk Analysis",
            vertical=IndustryVertical.LEGAL,
            baseline=baseline,
            ai_system=ai_system,
            time_reduction_pct=99.70,
            cost_reduction_pct=99.93,
            human_effort_reduction_pct=98.93,
            accuracy_improvement_pct=11.35,
            speedup_multiplier=337.5,
        )

    @classmethod
    def get_resume_comparison(cls) -> WorkflowComparison:
        baseline = ProcessModel(
            name="Manual Recruiter Resume Screening",
            vertical=IndustryVertical.HR,
            is_ai_system=False,
            steps=[
                WorkflowStep("Resume Review & Formatting", ProcessStepType.MANUAL, 240.0, 100.0, 3.0, 3.00),
                WorkflowStep("Skills & Experience Evaluation", ProcessStepType.MANUAL, 360.0, 100.0, 5.0, 4.00),
                WorkflowStep("ATS Spreadsheet Logging", ProcessStepType.MANUAL, 120.0, 100.0, 1.5, 1.50),
            ],
            total_duration_minutes=12.0,
            total_cost_usd=8.50,
            accuracy_pct=91.0,
            human_hours_per_1k_docs=200.0,
        )

        ai_system = ProcessModel(
            name="DocuTask TalentPulse Resume Screening Agent",
            vertical=IndustryVertical.HR,
            is_ai_system=True,
            steps=[
                WorkflowStep("Automated ATS Ingestion", ProcessStepType.AUTONOMOUS_AI, 0.5, 0.0, 0.05, 0.0010),
                WorkflowStep("Semantic Skill & Experience Extraction", ProcessStepType.AUTONOMOUS_AI, 1.5, 0.0, 0.05, 0.0025),
                WorkflowStep("Job Fit Scoring & Shortlist Generation", ProcessStepType.AUTONOMOUS_AI, 0.5, 0.0, 0.05, 0.0010),
            ],
            total_duration_minutes=0.042,  # 2.5 seconds
            total_cost_usd=0.0045,
            accuracy_pct=99.6,
            human_hours_per_1k_docs=1.5,
        )

        return WorkflowComparison(
            workflow_name="HR Candidate Resume Screening & Matching",
            vertical=IndustryVertical.HR,
            baseline=baseline,
            ai_system=ai_system,
            time_reduction_pct=99.65,
            cost_reduction_pct=99.95,
            human_effort_reduction_pct=99.25,
            accuracy_improvement_pct=9.45,
            speedup_multiplier=288.0,
        )

    @classmethod
    def get_healthcare_comparison(cls) -> WorkflowComparison:
        baseline = ProcessModel(
            name="Manual Prior Authorization Clinical Review",
            vertical=IndustryVertical.HEALTHCARE,
            is_ai_system=False,
            steps=[
                WorkflowStep("Medical Fax & EHR Ingestion", ProcessStepType.MANUAL, 300.0, 100.0, 2.0, 3.50),
                WorkflowStep("ICD-10 & Treatment Verification", ProcessStepType.MANUAL, 900.0, 100.0, 6.0, 10.50),
                WorkflowStep("Payer Policy & Formulary Match", ProcessStepType.MANUAL, 300.0, 100.0, 3.0, 4.50),
            ],
            total_duration_minutes=25.0,
            total_cost_usd=18.50,
            accuracy_pct=90.5,
            human_hours_per_1k_docs=416.7,
        )

        ai_system = ProcessModel(
            name="DocuTask BioHealth Prior Authorization Agent",
            vertical=IndustryVertical.HEALTHCARE,
            is_ai_system=True,
            steps=[
                WorkflowStep("Multimodal Clinical OCR", ProcessStepType.AUTONOMOUS_AI, 2.0, 0.0, 0.05, 0.0040),
                WorkflowStep("Medical Entity & ICD-10 Extraction", ProcessStepType.AUTONOMOUS_AI, 2.5, 0.0, 0.05, 0.0080),
                WorkflowStep("Formulary & Clinical Policy Matcher", ProcessStepType.AUTONOMOUS_AI, 1.5, 5.0, 0.05, 0.0040),
            ],
            total_duration_minutes=0.10,  # 6.0 seconds
            total_cost_usd=0.0160,
            accuracy_pct=99.5,
            human_hours_per_1k_docs=4.0,
        )

        return WorkflowComparison(
            workflow_name="Clinical Prior Authorization & Medical Records",
            vertical=IndustryVertical.HEALTHCARE,
            baseline=baseline,
            ai_system=ai_system,
            time_reduction_pct=99.60,
            cost_reduction_pct=99.91,
            human_effort_reduction_pct=99.04,
            accuracy_improvement_pct=9.94,
            speedup_multiplier=250.0,
        )
