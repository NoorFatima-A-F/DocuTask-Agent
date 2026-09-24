import pytest
from app.platform_verification.lifecycle import (
    VerificationState, VerificationStateMachine, VerificationType, QualityGateRuleDefinition, VerificationSpecification,
    VerificationPlanner, VerificationExecutionEngine, EvidenceLifecycleManager, MetricProcessingPipeline,
    IndependentEvaluationEngine,
    QualityGateDecision, QualityGateDecisionEngine,
    CertificationAuthorityWorkflow, VerificationCertificate,
    VerificationLifecycleEngineFacade
)
from app.shared_kernel.exceptions import InvariantViolationError, EnvironmentNotReadyError

class TestVerificationLifecycleStateMachine:
    def test_valid_sequential_lifecycle_transitions(self):
        sm = VerificationStateMachine(VerificationState.DRAFT)
        assert sm.current_state == VerificationState.DRAFT

        # 1. DRAFT -> DEFINED
        sm.transition_to(VerificationState.DEFINED)
        assert sm.current_state == VerificationState.DEFINED

        # 2. DEFINED -> PLANNED
        sm.transition_to(VerificationState.PLANNED)
        assert sm.current_state == VerificationState.PLANNED

        # 3. PLANNED -> READY
        sm.transition_to(VerificationState.READY)
        assert sm.current_state == VerificationState.READY

        # 4. READY -> EXECUTING
        sm.transition_to(VerificationState.EXECUTING)
        assert sm.current_state == VerificationState.EXECUTING

        # 5. EXECUTING -> COLLECTING_EVIDENCE
        sm.transition_to(VerificationState.COLLECTING_EVIDENCE)
        assert sm.current_state == VerificationState.COLLECTING_EVIDENCE

        # 6. COLLECTING_EVIDENCE -> ANALYZING
        sm.transition_to(VerificationState.ANALYZING)
        assert sm.current_state == VerificationState.ANALYZING

        # 7. ANALYZING -> EVALUATING
        sm.transition_to(VerificationState.EVALUATING)
        assert sm.current_state == VerificationState.EVALUATING

        # 8. EVALUATING -> CERTIFICATION_PENDING
        sm.transition_to(VerificationState.CERTIFICATION_PENDING)
        assert sm.current_state == VerificationState.CERTIFICATION_PENDING

        # 9. CERTIFICATION_PENDING -> CERTIFIED
        sm.transition_to(VerificationState.CERTIFIED)
        assert sm.current_state == VerificationState.CERTIFIED

        # 10. CERTIFIED -> ARCHIVED
        sm.transition_to(VerificationState.ARCHIVED)
        assert sm.current_state == VerificationState.ARCHIVED

        assert len(sm.history) == 10

    def test_invalid_transition_prevention(self):
        sm = VerificationStateMachine(VerificationState.DRAFT)
        with pytest.raises(InvariantViolationError):
            sm.transition_to(VerificationState.EXECUTING)

        with pytest.raises(InvariantViolationError):
            sm.transition_to(VerificationState.CERTIFIED)


class TestVerificationPlanningAndReadiness:
    def test_plan_generation_and_dag_steps(self):
        spec = VerificationSpecification.create(
            name="OCR Accuracy Verification",
            verification_type=VerificationType.AI_QUALITY,
            objective="Validate invoice extraction precision >= 98%",
            target_subsystem="ai_extraction",
            target_version="2.1.0"
        )
        plan = VerificationPlanner.plan_verification(spec)
        assert len(plan.steps) == 4
        assert plan.specification_id == spec.specification_id

        assert VerificationPlanner.validate_plan_readiness(plan, environment_ready=True, dataset_ready=True) is True

        with pytest.raises(EnvironmentNotReadyError):
            VerificationPlanner.validate_plan_readiness(plan, environment_ready=False)


class TestExecutionEngineAndEvidence:
    def test_task_execution_and_cas_evidence(self):
        spec = VerificationSpecification.create(
            name="Performance Benchmarking",
            verification_type=VerificationType.PERFORMANCE,
            objective="Ensure P99 latency <= 50ms",
            target_subsystem="ocr_pipeline",
            target_version="1.0.0"
        )
        plan = VerificationPlanner.plan_verification(spec)
        engine = VerificationExecutionEngine()
        session = engine.start_execution(plan)

        assert session.status == "SUCCESS"
        assert len(session.task_results) == 4

        evidence_mgr = EvidenceLifecycleManager()
        artifact = evidence_mgr.collect_and_seal(
            session.execution_id, "step_1", "BENCHMARK_LOG", {"p99_ms": 32.5}
        )
        assert len(artifact.sha256_checksum) == 64
        assert evidence_mgr.verify_artifact_integrity(artifact) is True


class TestEvaluationAndQualityGates:
    def test_metric_processing_and_gate_decisions(self):
        samples = {
            "accuracy": [0.98, 0.99, 0.97, 0.98, 0.98],
            "p99_latency_ms": [40.0, 42.0, 39.0, 41.0, 40.0]
        }
        metrics = MetricProcessingPipeline.process_metrics(samples)
        assert "accuracy" in metrics
        assert metrics["accuracy"].value > 0.95

        spec = VerificationSpecification.create(
            name="Gate Test Spec",
            verification_type=VerificationType.FUNCTIONAL,
            objective="Test Quality Gates",
            target_subsystem="core",
            target_version="1.0.0",
            quality_gate_rules=[
                QualityGateRuleDefinition("accuracy", ">=", 0.95, is_hard_blocker=True),
                QualityGateRuleDefinition("p99_latency_ms", "<=", 50.0, is_hard_blocker=True)
            ]
        )
        evaluation = IndependentEvaluationEngine.evaluate(spec, metrics)
        assert evaluation.overall_passed is True

        gate_summary = QualityGateDecisionEngine.evaluate_gates(evaluation)
        assert gate_summary.decision == QualityGateDecision.PASSED
        assert len(gate_summary.blockers_triggered) == 0


class TestCertificationAndTamperProofSignatures:
    def test_certification_authority_workflow(self):
        ca = CertificationAuthorityWorkflow(signing_secret="super_secret_ca_key")
        cert = ca.issue_certificate(
            specification_id="vspec_123",
            execution_id="exec_456",
            target_subsystem="document_ocr",
            target_version="1.5.0",
            level="ENTERPRISE_CERTIFIED"
        )
        assert ca.verify_certificate(cert) is True

        tampered_cert = VerificationCertificate(
            certificate_id=cert.certificate_id,
            specification_id="vspec_TAMPERED",
            execution_id=cert.execution_id,
            target_subsystem=cert.target_subsystem,
            target_version=cert.target_version,
            digital_signature=cert.digital_signature,
            issued_at=cert.issued_at,
            expires_at=cert.expires_at,
            certification_level=cert.certification_level
        )
        assert ca.verify_certificate(tampered_cert) is False


class TestEndToEndLifecycleFacade:
    def test_full_lifecycle_journey_execution(self):
        facade = VerificationLifecycleEngineFacade()
        spec = VerificationSpecification.create(
            name="End-to-End Invoice Processing Verification",
            verification_type=VerificationType.AI_QUALITY,
            objective="Certify AI extraction fidelity",
            target_subsystem="ai_extraction",
            target_version="3.0.0"
        )
        result = facade.run_full_lifecycle(spec)

        assert result.final_lifecycle_state == VerificationState.ARCHIVED
        assert result.evaluation.overall_passed is True
        assert result.gate_decision.decision == QualityGateDecision.PASSED
        assert result.certificate is not None
        assert result.certificate.certification_level == "ENTERPRISE_CERTIFIED"
        assert len(result.sealed_artifacts) > 0
