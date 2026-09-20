"""
Abstract Interfaces for Enterprise Readiness Contract Architecture (Part 3H.3.1).
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.platform_verification.readiness_contract.domain.models import (
    ReadinessContractReport,
    StateMachineReport,
    DependencyPolicyReport,
    StartupValidationReport,
    FailureTransitionReport,
    OrchestrationReport,
    ReadinessScorecard,
)


class IReadinessContractManager(ABC):
    @abstractmethod
    def validate_readiness_contract(self) -> ReadinessContractReport:
        pass


class IReadinessStateMachine(ABC):
    @abstractmethod
    def verify_state_machine(self) -> StateMachineReport:
        pass


class IReadinessPolicyEngine(ABC):
    @abstractmethod
    def evaluate_policy(self) -> DependencyPolicyReport:
        pass


class IStartupReadinessValidator(ABC):
    @abstractmethod
    def validate_startup_sequence(self) -> StartupValidationReport:
        pass


class IFailureTransitionTester(ABC):
    @abstractmethod
    def test_failure_transitions(self) -> FailureTransitionReport:
        pass


class IReadinessOrchestrationVerifier(ABC):
    @abstractmethod
    def verify_orchestration(self) -> OrchestrationReport:
        pass


class IReadinessScoreEngine(ABC):
    @abstractmethod
    def compute_scorecard(
        self,
        contract_report: ReadinessContractReport,
        state_report: StateMachineReport,
        policy_report: DependencyPolicyReport,
        startup_report: StartupValidationReport,
        failure_report: FailureTransitionReport,
        orchestration_report: OrchestrationReport,
        security_passed: bool,
        observability_passed: bool,
    ) -> ReadinessScorecard:
        pass
