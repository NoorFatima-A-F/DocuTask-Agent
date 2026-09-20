"""
End-to-End Autonomous Invoice Processing Workflow Demonstration.
Demonstrates the full autonomous agent runtime lifecycle:
User Goal -> Runtime Kernel -> Agent Session -> Task Planning (DAG) -> Multi-Agent Execution
  -> Tool Simulation -> Memory -> Failure Injection -> Supervisor Recovery -> Reflection Evaluation -> Telemetry.
"""

import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.agents.runtime.runtime_context import RuntimeContext
from app.agents.runtime.context_store import InMemoryContextStore
from app.agents.runtime.scheduler import MemoryTaskQueue, SchedulerController
from app.agents.runtime.enterprise.fault_injector import FaultInjector, FaultType
from app.agents.runtime.enterprise.audit_log import ImmutableRuntimeAuditLog
from app.agents.runtime.enterprise.audit_event import AuditEventType
from app.agents.runtime.runtime_supervisor import (
    WorkerLifecycleManager,
    CheckpointRecoveryManager,
    AsyncTaskWorker,
    WorkerStatus,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("AutonomousInvoicePipeline")


class AutonomousInvoicePipeline:
    """Enterprise Document Processing Agent Orchestrator with Supervisor Fault Recovery."""

    def __init__(self) -> None:
        self.context_store = InMemoryContextStore()
        self.scheduler_backend = MemoryTaskQueue()
        self.scheduler = SchedulerController(backend=self.scheduler_backend)
        self.fault_injector = FaultInjector()
        self.audit_log = ImmutableRuntimeAuditLog()
        self.checkpoint_mgr = CheckpointRecoveryManager()
        self.worker_mgr = WorkerLifecycleManager(checkpoint_manager=self.checkpoint_mgr)
        self.telemetry: Dict[str, Any] = {}

    async def run(self, invoice_payload: Dict[str, Any]) -> Dict[str, Any]:
        pipeline_start = time.perf_counter()
        runtime_id = str(uuid4())
        ctx = RuntimeContext(
            runtime_id=runtime_id,
            tenant_id="enterprise-corp",
            workspace_id="finance-invoicing",
            workflow_id="wf-invoice-autonomous",
            attributes={"document_id": invoice_payload["document_id"]},
        )

        logger.info(f"=== Starting Autonomous Invoice Pipeline [Runtime ID: {runtime_id}] ===")
        await self.context_store.save_context(ctx)
        self.audit_log.append(
            event_type=AuditEventType.RUNTIME_LIFECYCLE,
            actor="orchestrator",
            details={"action": "START_WORKFLOW", "document_id": invoice_payload["document_id"]},
            tenant_id=ctx.tenant_id,
        )

        # -------------------------------------------------------------
        # Step 1: Goal Decomposition & Planning (DAG Generation)
        # -------------------------------------------------------------
        dag_plan = [
            {"step": "ocr", "agent": "OCRAgent", "dependencies": []},
            {"step": "extraction", "agent": "ExtractionAgent", "dependencies": ["ocr"]},
            {"step": "validation", "agent": "ValidationAgent", "dependencies": ["extraction"]},
            {"step": "storage", "agent": "StorageAgent", "dependencies": ["validation"]},
            {"step": "reflection", "agent": "ReflectionAgent", "dependencies": ["storage"]},
        ]
        logger.info(f"[Step 1: Planner] Generated 5-step DAG Plan: {[s['step'] for s in dag_plan]}")
        await self.context_store.checkpoint_context(runtime_id, {"dag_plan": dag_plan, "stage": "PLANNED"})

        pipeline_state: Dict[str, Any] = {"raw_invoice": invoice_payload}

        # -------------------------------------------------------------
        # Step 2: OCR Agent Execution
        # -------------------------------------------------------------
        logger.info("[Step 2: OCRAgent] Extracting text and layout from scanned invoice image...")
        await asyncio.sleep(0.05)
        pipeline_state["ocr_text"] = (
            f"INVOICE {invoice_payload['invoice_number']}\n"
            f"VENDOR: {invoice_payload['vendor']}\n"
            f"TOTAL: {invoice_payload['amount']}\n"
            f"TAX: {invoice_payload['tax']}\n"
            f"DUE DATE: 2026-10-15"
        )
        pipeline_state["ocr_confidence"] = 0.99
        v1 = await self.context_store.checkpoint_context(runtime_id, {"stage": "OCR_DONE", "state": pipeline_state})
        logger.info(f"[Step 2: OCRAgent] Completed. Checkpoint v{v1} saved.")

        # -------------------------------------------------------------
        # Step 3: Extraction Agent with Failure Injection & Recovery
        # -------------------------------------------------------------
        logger.info("[Step 3: ExtractionAgent] Arming fault injection (WORKER_CRASH on attempt 1)...")
        self.fault_injector.inject_fault("ExtractionWorker", FaultType.WORKER_CRASH, burst_count=1)

        extraction_worker_id = "worker-extraction-01"
        attempt = 0
        extraction_success = False

        while not extraction_success and attempt < 3:
            attempt += 1
            logger.info(f"[Step 3: ExtractionAgent] Attempt {attempt} executing...")
            try:
                # Check for synthetic fault
                await self.fault_injector.maybe_fail("ExtractionWorker")

                # Extraction logic
                pipeline_state["extracted_entities"] = {
                    "invoice_number": invoice_payload["invoice_number"],
                    "vendor": invoice_payload["vendor"],
                    "total_amount": invoice_payload["amount"],
                    "tax_amount": invoice_payload["tax"],
                    "line_items": invoice_payload.get("items", []),
                }
                extraction_success = True
                logger.info(f"[Step 3: ExtractionAgent] Successfully extracted entities on attempt {attempt}!")

            except Exception as ex:
                logger.warning(f"[Supervisor] ExtractionWorker crashed with: {ex}")
                self.audit_log.append(
                    event_type=AuditEventType.SECURITY_VIOLATION,
                    actor="supervisor",
                    details={"error": str(ex), "attempt": attempt, "worker": extraction_worker_id},
                    tenant_id=ctx.tenant_id,
                )
                logger.info("[Supervisor] Restoring checkpoint state from context store...")
                restored_state = await self.context_store.restore_context(runtime_id)
                pipeline_state = restored_state.get("state", pipeline_state)
                logger.info(f"[Supervisor] Worker {extraction_worker_id} recovered from checkpoint v{v1}. Retrying...")
                await asyncio.sleep(0.05)

        v2 = await self.context_store.checkpoint_context(runtime_id, {"stage": "EXTRACTION_DONE", "state": pipeline_state})

        # -------------------------------------------------------------
        # Step 4: Validation Agent Execution
        # -------------------------------------------------------------
        logger.info("[Step 4: ValidationAgent] Performing cross-field validation & 3-way matching...")
        await asyncio.sleep(0.03)
        entities = pipeline_state["extracted_entities"]
        math_valid = float(entities["total_amount"]) > float(entities["tax_amount"])
        pipeline_state["validation_result"] = {
            "status": "VALID",
            "mathematical_consistency": math_valid,
            "vendor_verified": True,
            "po_match": True,
        }
        v3 = await self.context_store.checkpoint_context(runtime_id, {"stage": "VALIDATION_DONE", "state": pipeline_state})
        logger.info(f"[Step 4: ValidationAgent] Validation complete. Checkpoint v{v3} saved.")

        # -------------------------------------------------------------
        # Step 5: Storage Agent Execution
        # -------------------------------------------------------------
        logger.info("[Step 5: StorageAgent] Persisting invoice record to database and audit ledger...")
        await asyncio.sleep(0.03)
        pipeline_state["stored_record_id"] = f"DB-REC-{uuid4().hex[:8].upper()}"
        self.audit_log.append(
            event_type=AuditEventType.TENANT_ACTION,
            actor="StorageAgent",
            details={"record_id": pipeline_state["stored_record_id"], "amount": entities["total_amount"]},
            tenant_id=ctx.tenant_id,
        )
        v4 = await self.context_store.checkpoint_context(runtime_id, {"stage": "STORAGE_DONE", "state": pipeline_state})

        # -------------------------------------------------------------
        # Step 6: Reflection & Self-Critique Agent
        # -------------------------------------------------------------
        logger.info("[Step 6: ReflectionAgent] Evaluating workflow output quality and resilience...")
        await asyncio.sleep(0.04)
        reflection_score = 0.985
        reflection_critique = {
            "quality_score": reflection_score,
            "precision": 1.0,
            "resilience_recovery_verified": True,
            "failures_handled": 1,
            "checkpoints_created": v4,
            "recommendation": "APPROVE_FOR_POSTING",
        }
        pipeline_state["reflection_critique"] = reflection_critique
        v5 = await self.context_store.checkpoint_context(runtime_id, {"stage": "COMPLETED", "state": pipeline_state})
        logger.info(f"[Step 6: ReflectionAgent] Quality Score: {reflection_score} -> {reflection_critique['recommendation']}")

        # -------------------------------------------------------------
        # Final Telemetry & Summary
        # -------------------------------------------------------------
        total_time_ms = (time.perf_counter() - pipeline_start) * 1000.0
        self.audit_log.append(
            event_type=AuditEventType.RUNTIME_LIFECYCLE,
            actor="orchestrator",
            details={"action": "COMPLETE_WORKFLOW", "duration_ms": total_time_ms},
            tenant_id=ctx.tenant_id,
        )

        audit_integrity = self.audit_log.verify_integrity()
        all_checkpoints = await self.context_store.list_checkpoints(runtime_id)

        result_summary = {
            "status": "SUCCESS",
            "runtime_id": runtime_id,
            "document_id": invoice_payload["document_id"],
            "invoice_number": invoice_payload["invoice_number"],
            "duration_ms": round(total_time_ms, 2),
            "checkpoints_count": len(all_checkpoints),
            "checkpoints_versions": all_checkpoints,
            "failure_recovered": True,
            "reflection_score": reflection_score,
            "audit_chain_valid": audit_integrity,
            "stored_record_id": pipeline_state["stored_record_id"],
            "extracted_data": pipeline_state["extracted_entities"],
        }
        logger.info("=== Autonomous Invoice Processing Pipeline Completed Successfully! ===")
        return result_summary


async def main() -> None:
    sample_invoice = {
        "document_id": "doc-inv-9921",
        "invoice_number": "INV-2026-X892",
        "vendor": "Acme Industrial Systems Ltd",
        "amount": "14850.00",
        "tax": "1350.00",
        "items": [
            {"description": "Server Blade Compute Unit", "qty": 2, "price": "6000.00"},
            {"description": "Enterprise Support License", "qty": 1, "price": "1500.00"},
        ],
    }

    pipeline = AutonomousInvoicePipeline()
    result = await pipeline.run(sample_invoice)
    print("\n--- FINAL PIPELINE RUN REPORT ---")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
