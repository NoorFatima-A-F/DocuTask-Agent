"""Task Decomposer for Autonomous Agent Operating System.

Recursively breaks high-level GoalSpecifications into atomic/composite
subtasks with clear dependencies, inputs, outputs, and validation steps.
"""

from __future__ import annotations

import uuid
from typing import List

from app.agents.intelligence.goal.goal_specification import GoalSpecification
from app.agents.intelligence.goal.intent_classifier import IntentType
from app.agents.planning.execution_plan import PlannedTask


class TaskDecomposer:
    """Decomposes GoalSpecifications into topologically sound subtasks."""

    def decompose(self, goal: GoalSpecification) -> List[PlannedTask]:
        intent = goal.intent
        tasks: List[PlannedTask] = []

        if intent in (IntentType.INVOICE_PROCESSING.value, IntentType.RECEIPT_ANALYSIS.value):
            tasks = self._decompose_financial_document(goal)
        elif intent == IntentType.COMPLIANCE_AUDIT.value:
            tasks = self._decompose_compliance_audit(goal)
        elif intent == IntentType.CONTRACT_REVIEW.value:
            tasks = self._decompose_contract_review(goal)
        elif intent == IntentType.FRAUD_DETECTION.value:
            tasks = self._decompose_fraud_detection(goal)
        else:
            tasks = self._decompose_generic_extraction(goal)

        # Check if human review is strictly required by constraints
        if goal.constraints.get("require_human_review", False):
            last_task = tasks[-1]
            human_task = PlannedTask(
                task_id=f"task_human_approval_{uuid.uuid4().hex[:6]}",
                name="Human In The Loop Review",
                action="human_review",
                assigned_agent="agent_human_supervisor",
                required_tools=["tool_interactive_approval"],
                dependencies=[last_task.task_id],
                input_parameters={"review_reason": "Constraint requirement"},
                output_key="human_approval",
                timeout_seconds=300.0,
            )
            tasks.append(human_task)

        return tasks

    def _decompose_financial_document(self, goal: GoalSpecification) -> List[PlannedTask]:
        t1_id = f"task_ocr_{uuid.uuid4().hex[:6]}"
        t2_id = f"task_extract_{uuid.uuid4().hex[:6]}"
        t3_id = f"task_math_validate_{uuid.uuid4().hex[:6]}"
        t4_id = f"task_compliance_{uuid.uuid4().hex[:6]}"

        t1 = PlannedTask(
            task_id=t1_id,
            name="Optical Character & Layout Recognition",
            action="ocr",
            dependencies=[],
            input_parameters={"document_path": goal.input_requirements.get("document_path")},
            output_key="raw_text_and_boxes",
            is_critical=True,
        )

        t2 = PlannedTask(
            task_id=t2_id,
            name="Structured Entity Extraction",
            action="entity_extraction",
            dependencies=[t1_id],
            input_parameters={"target_fields": goal.expected_output.get("fields", [])},
            output_key="extracted_entities",
            is_critical=True,
        )

        t3 = PlannedTask(
            task_id=t3_id,
            name="Mathematical & Currency Validation",
            action="arithmetic_verification",
            dependencies=[t2_id],
            input_parameters={"expected_currency": goal.input_requirements.get("expected_currency", "USD")},
            output_key="validation_result",
            is_critical=True,
        )

        t4 = PlannedTask(
            task_id=t4_id,
            name="Policy & Compliance Verification",
            action="regulatory_audit",
            dependencies=[t3_id],
            input_parameters={"frameworks": goal.constraints.get("compliance_frameworks", [])},
            output_key="compliance_report",
            is_critical=False,
        )

        return [t1, t2, t3, t4]

    def _decompose_compliance_audit(self, goal: GoalSpecification) -> List[PlannedTask]:
        t1_id = f"task_ocr_{uuid.uuid4().hex[:6]}"
        t2_id = f"task_clause_extract_{uuid.uuid4().hex[:6]}"
        t3_id = f"task_compliance_eval_{uuid.uuid4().hex[:6]}"

        t1 = PlannedTask(task_id=t1_id, name="Document Ingestion & OCR", action="ocr", dependencies=[])
        t2 = PlannedTask(task_id=t2_id, name="Legal Clause Extraction", action="clause_extraction", dependencies=[t1_id])
        t3 = PlannedTask(task_id=t3_id, name="Regulatory Compliance Evaluation", action="regulatory_audit", dependencies=[t2_id])
        return [t1, t2, t3]

    def _decompose_contract_review(self, goal: GoalSpecification) -> List[PlannedTask]:
        t1_id = f"task_ocr_{uuid.uuid4().hex[:6]}"
        t2_id = f"task_clause_extract_{uuid.uuid4().hex[:6]}"
        t3_id = f"task_risk_assessment_{uuid.uuid4().hex[:6]}"

        t1 = PlannedTask(task_id=t1_id, name="Contract Ingestion & OCR", action="ocr", dependencies=[])
        t2 = PlannedTask(task_id=t2_id, name="Contract Clause Extraction", action="clause_extraction", dependencies=[t1_id])
        t3 = PlannedTask(task_id=t3_id, name="Legal Risk Assessment", action="risk_assessment", dependencies=[t2_id])
        return [t1, t2, t3]

    def _decompose_fraud_detection(self, goal: GoalSpecification) -> List[PlannedTask]:
        t1_id = f"task_ocr_{uuid.uuid4().hex[:6]}"
        t2_id = f"task_tamper_analysis_{uuid.uuid4().hex[:6]}"
        t3_id = f"task_anomaly_score_{uuid.uuid4().hex[:6]}"

        t1 = PlannedTask(task_id=t1_id, name="High-Res Image Acquisition", action="ocr", dependencies=[])
        t2 = PlannedTask(task_id=t2_id, name="Visual & Font Tamper Analysis", action="tamper_analysis", dependencies=[t1_id])
        t3 = PlannedTask(task_id=t3_id, name="Fraud & Anomaly Scoring", action="fraud_scoring", dependencies=[t2_id])
        return [t1, t2, t3]

    def _decompose_generic_extraction(self, goal: GoalSpecification) -> List[PlannedTask]:
        t1_id = f"task_ocr_{uuid.uuid4().hex[:6]}"
        t2_id = f"task_extract_{uuid.uuid4().hex[:6]}"

        t1 = PlannedTask(task_id=t1_id, name="Document OCR", action="ocr", dependencies=[])
        t2 = PlannedTask(task_id=t2_id, name="Data Extraction", action="entity_extraction", dependencies=[t1_id])
        return [t1, t2]
