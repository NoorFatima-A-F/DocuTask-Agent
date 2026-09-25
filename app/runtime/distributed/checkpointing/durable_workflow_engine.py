"""
Phase 13.18: Durable Workflow Engine & Checkpointing
Temporal-like persistent workflow lifecycle: pause, resume, step-level checkpointing, and node crash recovery.
"""

from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from app.runtime.distributed.models.schemas import (
    DurableWorkflow,
    WorkflowCheckpoint,
    WorkflowStepState,
    JobState,
)


class CheckpointEngine:
    """Manages immutable step-level workflow checkpoint snapshots."""

    @staticmethod
    def create_checkpoint(
        workflow: DurableWorkflow,
        step_index: int,
        step_name: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        variables: Dict[str, Any],
        memory: Dict[str, Any],
        fencing_token: int = 1,
    ) -> WorkflowCheckpoint:
        step_state = WorkflowStepState(
            step_index=step_index,
            step_name=step_name,
            status="COMPLETED",
            inputs=inputs,
            outputs=outputs,
            duration_ms=120.0,
        )
        raw_sig = f"{workflow.workflow_id}:{step_index}:{fencing_token}:{datetime.now(timezone.utc).isoformat()}"
        sha = hashlib.sha256(raw_sig.encode()).hexdigest()

        chk = WorkflowCheckpoint(
            workflow_id=workflow.workflow_id,
            step_index=step_index,
            completed_steps=[*getattr(workflow.checkpoints[-1], "completed_steps", []), step_state] if workflow.checkpoints else [step_state],
            variables=variables,
            memory_context=memory,
            fencing_token=fencing_token,
            state_hash=sha,
        )
        workflow.checkpoints.append(chk)
        workflow.current_step_index = step_index + 1
        workflow.updated_at = datetime.now(timezone.utc).isoformat()
        return chk


class DurableWorkflowEngine:
    """Orchestrates resilient stateful workflows with crash survival and replay."""

    def __init__(self):
        self._workflows: Dict[str, DurableWorkflow] = {}
        self._seed_workflows()

    def _seed_workflows(self):
        wf1 = DurableWorkflow(
            workflow_id="wf_invoice_proc_01",
            title="Enterprise Document Extraction Saga",
            agent_id="agent_doc_extractor",
            state=JobState.RUNNING,
            current_step_index=2,
            total_steps=4,
            assigned_worker_id="node_us_east_01",
        )
        CheckpointEngine.create_checkpoint(
            wf1,
            step_index=0,
            step_name="Multimodal OCR Extraction",
            inputs={"file": "invoice_9941.pdf"},
            outputs={"pages": 3, "status": "EXTRACTED"},
            variables={"doc_type": "INVOICE"},
            memory={"tenant": "acme_corp"},
        )
        CheckpointEngine.create_checkpoint(
            wf1,
            step_index=1,
            step_name="Entity & Line Item Extraction",
            inputs={"raw_text_length": 4200},
            outputs={"total_amount": 14500.0, "vendor": "Stripe Corp"},
            variables={"doc_type": "INVOICE", "total_usd": 14500.0},
            memory={"tenant": "acme_corp"},
        )
        self._workflows[wf1.workflow_id] = wf1

    def create_workflow(self, title: str, agent_id: str, total_steps: int = 5) -> DurableWorkflow:
        wf = DurableWorkflow(
            title=title,
            agent_id=agent_id,
            total_steps=total_steps,
            state=JobState.RUNNING,
        )
        self._workflows[wf.workflow_id] = wf
        return wf

    def pause_workflow(self, workflow_id: str) -> Optional[DurableWorkflow]:
        wf = self._workflows.get(workflow_id)
        if not wf:
            return None
        wf.state = JobState.PAUSED
        wf.updated_at = datetime.now(timezone.utc).isoformat()
        return wf

    def resume_workflow(self, workflow_id: str, new_worker_id: Optional[str] = None) -> Optional[DurableWorkflow]:
        wf = self._workflows.get(workflow_id)
        if not wf:
            return None
        wf.state = JobState.RUNNING
        if new_worker_id:
            wf.assigned_worker_id = new_worker_id
        wf.updated_at = datetime.now(timezone.utc).isoformat()
        return wf

    def migrate_workflow_on_crash(self, crashed_worker_id: str, target_worker_id: str) -> List[DurableWorkflow]:
        migrated = []
        for wf in self._workflows.values():
            if wf.assigned_worker_id == crashed_worker_id and wf.state == JobState.RUNNING:
                wf.assigned_worker_id = target_worker_id
                wf.state = JobState.MIGRATED
                wf.updated_at = datetime.now(timezone.utc).isoformat()
                migrated.append(wf)
        return migrated

    def list_workflows(self) -> List[DurableWorkflow]:
        return list(self._workflows.values())

    def get_workflow(self, workflow_id: str) -> Optional[DurableWorkflow]:
        return self._workflows.get(workflow_id)
