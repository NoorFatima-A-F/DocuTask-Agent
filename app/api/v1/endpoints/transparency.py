"""
FastAPI Endpoints for Autonomous Runtime Transparency, Execution Intelligence & Enterprise Credibility (ARTEICP).
Exposes real-time event-sourced timelines, live DAGs with CPM critical path, granular cost/energy accounting,
mathematical confidence proofs, worker scheduling, chaos recovery, and multi-corpus benchmarks.
"""

from typing import Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

# 1. Observability
from app.runtime.observability import (
    TimelineBuilder,
    execution_state_manager,
    worker_monitor,
    live_runtime_metrics,
)

# 2. Dynamic DAG & Critical Path
from app.runtime.dag_visualizer import (
    DAGRuntimeExtractor,
    CriticalPathAnalyzer,
    FlameGraphGenerator,
)

# 3. Cost & Energy Intelligence
from app.runtime.cost_intelligence import (
    CostAggregator,
    BudgetGovernor,
)

# 4. Mathematical Confidence
from app.runtime.mathematical_confidence import (
    MathematicalConfidenceEngine,
    CalibrationCurveBuilder,
)

# 5. Feedback Pipeline
from app.runtime.feedback_pipeline import (
    FeedbackProcessor,
    ReflectionOrchestrator,
    knowledge_versioner,
)

# 6. Resource Scheduler
from app.runtime.resource_scheduler import (
    priority_scheduler,
)

# 7. Failure Recovery & Chaos
from app.runtime.failure_recovery import (
    chaos_injector,
    recovery_orchestrator,
)

# 8. Benchmark Platform
from app.runtime.benchmark_platform import (
    benchmark_runner,
    BenchmarkReportGenerator,
)

# 9. Audit Intelligence & Provenance
from app.runtime.audit_intelligence import (
    FieldProvenanceTracer,
    audit_query_engine,
)

# 10. Demo Engine
from app.runtime.demo_engine import (
    demo_engine,
)

router = APIRouter()
feedback_processor = FeedbackProcessor()


# -------------------------------------------------------------
# Request Schemas
# -------------------------------------------------------------
class DeriveConfidenceRequest(BaseModel):
    ocr_confidence: float = Field(default=0.96, ge=0.0, le=1.0)
    schema_validation: float = Field(default=0.98, ge=0.0, le=1.0)
    cross_doc_agreement: float = Field(default=0.95, ge=0.0, le=1.0)
    memory_similarity: float = Field(default=0.92, ge=0.0, le=1.0)
    multi_agent_consensus: float = Field(default=1.0, ge=0.0, le=1.0)


class SubmitCorrectionRequest(BaseModel):
    document_id: str = "DOC-INV-2026"
    field_name: str = "total_tax_amount"
    extracted_value: str = "$120.00"
    corrected_value: str = "$142.50"
    confidence_was: float = 0.88
    model_was: str = "gemini-2.5-flash"
    submitted_by: str = "human-reviewer@enterprise.internal"


class InjectFaultRequest(BaseModel):
    fault_id: str = "fault_ocr_crash"


class RunBenchmarkRequest(BaseModel):
    corpus_id: str = "corp_invoices_100"


# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------

# 1. Observability & Live State
@router.get("/timeline", summary="Get live chronological mission timeline")
async def get_mission_timeline(mission_id: str = Query(default="mission_live_001")):
    # Sample real events for timeline
    events = [
        {"timestamp": 100.0, "event_type": "MISSION_DISPATCHED", "actor": "TaskOrchestrator", "summary": "Mission initiated"},
        {"timestamp": 100.12, "event_type": "OCR_INGEST_COMPLETED", "actor": "Worker-OCR-1", "payload": {"duration_ms": 120.0, "confidence": 0.98}},
        {"timestamp": 100.45, "event_type": "LLM_INFERENCE_DONE", "actor": "Worker-LLM-1", "payload": {"duration_ms": 330.0, "cost_usd": 0.0018, "confidence": 0.965}},
        {"timestamp": 100.75, "event_type": "VALIDATION_INVARIANT_PASSED", "actor": "Worker-Val-1", "payload": {"duration_ms": 50.0, "confidence": 0.985}},
        {"timestamp": 100.82, "event_type": "CRYPTO_AUDIT_SIGNED", "actor": "Worker-Sec-1", "payload": {"signature": "ED25519_SIG_8F3A"}},
    ]
    timeline = TimelineBuilder.build_timeline_from_events(mission_id, events)
    return {
        "mission_id": mission_id,
        "timeline_count": len(timeline),
        "timeline": [t.to_dict() for t in timeline],
    }


@router.get("/execution-state", summary="Get active mission and task state")
async def get_execution_state(mission_id: str = Query(default="mission_live_001")):
    snapshot = execution_state_manager.get_mission_snapshot(mission_id)
    return snapshot or {"error": "Mission not found"}


@router.get("/workers", summary="Get worker telemetry and cluster health")
async def get_worker_status():
    return worker_monitor.get_cluster_summary()


@router.get("/metrics", summary="Get live operational throughput metrics")
async def get_live_metrics():
    return live_runtime_metrics.get_live_metrics_summary()


# 2. Dynamic DAG & Critical Path
@router.get("/dag", summary="Get live dynamic DAG with CPM critical path")
async def get_live_dag(mission_id: str = Query(default="mission_live_001")):
    graph = DAGRuntimeExtractor.get_canonical_active_dag(mission_id)
    cpm = CriticalPathAnalyzer.analyze_dag(graph.nodes, graph.edges)
    return {
        "graph": graph.to_dict(),
        "cpm_analysis": cpm,
    }


@router.get("/flamegraph", summary="Get hierarchical execution flame graph")
async def get_flamegraph(mission_id: str = Query(default="mission_live_001")):
    return FlameGraphGenerator.generate_mission_flamegraph(mission_id)


# 3. Cost & Energy Intelligence
@router.get("/cost", summary="Get granular cost and carbon footprint telemetry")
async def get_cost_telemetry(mission_id: str = Query(default="mission_live_001")):
    cost_report = CostAggregator.get_canonical_mission_cost(mission_id)
    budget = BudgetGovernor.evaluate_budget(
        mission_id=mission_id,
        accumulated_cost_usd=cost_report.total_net_cost_usd,
        projected_cost_usd=cost_report.total_net_cost_usd * 1.2,
    )
    return {
        "cost_report": cost_report.to_dict(),
        "budget_compliance": budget.to_dict(),
    }


# 4. Mathematical Confidence
@router.post("/confidence/prove", summary="Derive confidence with explicit mathematical proof")
async def derive_confidence_proof(req: DeriveConfidenceRequest):
    proof = MathematicalConfidenceEngine.derive_confidence_with_proof(
        ocr_confidence=req.ocr_confidence,
        schema_validation=req.schema_validation,
        cross_doc_agreement=req.cross_doc_agreement,
        memory_similarity=req.memory_similarity,
        multi_agent_consensus=req.multi_agent_consensus,
    )
    return proof.to_dict()


@router.get("/confidence/calibration", summary="Get empirical calibration diagram")
async def get_calibration_diagram():
    return CalibrationCurveBuilder.get_canonical_calibration_curve()


# 5. Feedback Pipeline
@router.get("/feedback/rules", summary="Get versioned knowledge rules derived from feedback")
async def get_feedback_rules():
    return {
        "rules": knowledge_versioner.list_rules(),
        "feedbacks": feedback_processor.list_feedbacks(),
    }


@router.post("/feedback/submit", summary="Submit a human correction and trigger reflection")
async def submit_human_feedback(req: SubmitCorrectionRequest):
    fb = feedback_processor.ingest_correction(
        document_id=req.document_id,
        field_name=req.field_name,
        extracted_value=req.extracted_value,
        corrected_value=req.corrected_value,
        confidence_was=req.confidence_was,
        model_was=req.model_was,
        submitted_by=req.submitted_by,
    )
    insight = ReflectionOrchestrator.reflect_on_correction(fb)
    rule = knowledge_versioner.commit_rule(
        rule_statement=insight.hypothesized_rule,
        origin_feedback_id=fb.feedback_id,
    )
    fb.status = "COMMITTED_TO_MEMORY"
    return {
        "feedback": fb.to_dict(),
        "reflection": insight.to_dict(),
        "committed_rule": rule.to_dict(),
    }


# 6. Resource Scheduler
@router.get("/scheduler/status", summary="Get priority queue and scheduler telemetry")
async def get_scheduler_status():
    return priority_scheduler.get_scheduler_telemetry()


# 7. Failure Recovery & Chaos
@router.get("/chaos/faults", summary="List injectable chaos faults")
async def list_chaos_faults():
    return chaos_injector.list_faults()


@router.post("/chaos/inject", summary="Inject a fault and trigger autonomous recovery")
async def inject_fault(req: InjectFaultRequest):
    fault = chaos_injector.trigger_fault(req.fault_id)
    recovery = recovery_orchestrator.handle_task_failure(
        mission_id="mission_live_001",
        failed_task_id="task_live_ocr",
        failure_type=fault.fault_type,
    )
    return {
        "injected_fault": fault.to_dict(),
        "autonomous_recovery": recovery.to_dict(),
    }


# 8. Benchmark Platform
@router.get("/benchmark/corpora", summary="List benchmark corpora")
async def list_benchmark_corpora():
    return {
        "corpora": benchmark_runner.list_corpora(),
        "summary": BenchmarkReportGenerator.generate_full_dossier(),
    }


@router.post("/benchmark/run", summary="Run benchmark corpus")
async def run_benchmark(req: RunBenchmarkRequest):
    return benchmark_runner.run_benchmark(req.corpus_id)


# 9. Audit Intelligence & Provenance
@router.get("/provenance/trace", summary="Get end-to-end field lineage trace")
async def get_field_provenance(
    document_id: str = Query(default="DOC-INV-2026"),
    field_key: str = Query(default="invoice_total_amount"),
):
    return FieldProvenanceTracer.trace_field(document_id, field_key)


@router.get("/audit/search", summary="Search immutable decision audit trails")
async def search_audit_trails(
    query: Optional[str] = Query(default=None),
    decision_type: Optional[str] = Query(default=None),
):
    return audit_query_engine.query_audit_trail(decision_type=decision_type, search_query=query)


# 10. Demo Engine
@router.get("/demo/steps", summary="Get hackathon demonstration steps")
async def get_demo_steps():
    return {
        "demo_title": "DocuTask Autonomous Optimization & Enterprise Credibility Demo",
        "steps": demo_engine.get_canonical_demo_steps(),
    }
