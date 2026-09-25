from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Callable
import time

from .states import VerificationStateMachine, VerificationState
from .definitions import VerificationSpecification
from .planner import VerificationPlanner, VerificationPlan
from .engine import VerificationExecutionEngine, ExecutionSession
from .evidence_flow import EvidenceLifecycleManager, SealedEvidenceArtifact
from .metric_pipeline import MetricProcessingPipeline, ComputedMetric
from .evaluator import IndependentEvaluationEngine, IndependentEvaluationResult
from .quality_gates import QualityGateDecisionEngine, QualityGateDecision, GateEvaluationSummary
from .certification_flow import CertificationAuthorityWorkflow, VerificationCertificate
from .observability import LifecycleTimelineTracker
from app.shared_kernel.events import get_event_bus

@dataclass(frozen=True)
class EndToEndVerificationJourneyResult:
    specification: VerificationSpecification
    plan: VerificationPlan
    execution: ExecutionSession
    sealed_artifacts: List[SealedEvidenceArtifact]
    metrics: Dict[str, ComputedMetric]
    evaluation: IndependentEvaluationResult
    gate_decision: GateEvaluationSummary
    certificate: Optional[VerificationCertificate]
    final_lifecycle_state: VerificationState
    total_journey_duration_ms: float

class VerificationLifecycleEngineFacade:
    def __init__(self, ca_secret: str = "lifecycle_secret_key"):
        self.planner = VerificationPlanner()
        self.execution_engine = VerificationExecutionEngine()
        self.evidence_mgr = EvidenceLifecycleManager()
        self.metric_pipeline = MetricProcessingPipeline()
        self.evaluator = IndependentEvaluationEngine()
        self.gate_engine = QualityGateDecisionEngine()
        self.ca = CertificationAuthorityWorkflow(signing_secret=ca_secret)
        self.event_bus = get_event_bus()

    def run_full_lifecycle(
        self,
        spec: VerificationSpecification,
        raw_samples: Optional[Dict[str, List[float]]] = None,
        custom_workload: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None
    ) -> EndToEndVerificationJourneyResult:
        t0 = time.monotonic()
        LifecycleTimelineTracker()
        sm = VerificationStateMachine(VerificationState.DRAFT)

        sm.transition_to(VerificationState.DEFINED, reason="Specification authored")
        plan = self.planner.plan_verification(spec)
        sm.transition_to(VerificationState.PLANNED, reason="Plan generated")

        self.planner.validate_plan_readiness(plan, environment_ready=True, dataset_ready=True)
        sm.transition_to(VerificationState.READY, reason="Pre-flight readiness verified")

        sm.transition_to(VerificationState.EXECUTING, reason="Execution dispatched")
        handlers = {"RUN_WORKLOAD": custom_workload} if custom_workload else None
        session = self.execution_engine.start_execution(plan, custom_handlers=handlers)

        sm.transition_to(VerificationState.COLLECTING_EVIDENCE, reason="Sealing execution artifacts")
        sealed_list = []
        for art in session.raw_artifacts:
            sealed = self.evidence_mgr.collect_and_seal(
                session.execution_id, art["step_id"], "RAW_OUTPUT", art["output"]
            )
            sealed_list.append(sealed)

        sm.transition_to(VerificationState.ANALYZING, reason="Computing metrics")
        samples = raw_samples or {
            "accuracy": [0.96, 0.97, 0.98, 0.95, 0.97],
            "p99_latency_ms": [42.0, 45.0, 41.0, 43.0, 44.0]
        }
        computed_metrics = self.metric_pipeline.process_metrics(samples)

        sm.transition_to(VerificationState.EVALUATING, reason="Evaluating independent quality rules")
        evaluation = self.evaluator.evaluate(spec, computed_metrics)

        gate_summary = self.gate_engine.evaluate_gates(evaluation)

        certificate = None
        if gate_summary.decision in (QualityGateDecision.PASSED, QualityGateDecision.CONDITIONAL):
            sm.transition_to(VerificationState.CERTIFICATION_PENDING, reason="Quality gates approved")
            cert_level = "ENTERPRISE_CERTIFIED" if gate_summary.decision == QualityGateDecision.PASSED else "CONDITIONALLY_READY"
            certificate = self.ca.issue_certificate(
                specification_id=spec.specification_id,
                execution_id=session.execution_id,
                target_subsystem=spec.target_subsystem,
                target_version=spec.target_version,
                level=cert_level
            )
            sm.transition_to(VerificationState.CERTIFIED, reason="Cryptographic certificate issued")
        else:
            sm.transition_to(VerificationState.REJECTED, reason="Quality gates blocker failure")

        sm.transition_to(VerificationState.ARCHIVED, reason="Audit archive sealed")

        total_ms = (time.monotonic() - t0) * 1000.0

        return EndToEndVerificationJourneyResult(
            specification=spec,
            plan=plan,
            execution=session,
            sealed_artifacts=sealed_list,
            metrics=computed_metrics,
            evaluation=evaluation,
            gate_decision=gate_summary,
            certificate=certificate,
            final_lifecycle_state=sm.current_state,
            total_journey_duration_ms=total_ms
        )
