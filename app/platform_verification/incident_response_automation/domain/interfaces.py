"""Domain interfaces for incident response automation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.platform_verification.incident_response_automation.domain.models import (
    CICDPipelineReport,
    IncidentArchitectureReport,
    IncidentClassificationReport,
    IncidentCorrelationReport,
    IncidentDetectionReport,
    IncidentKnowledgeReport,
    IncidentQualityScorecard,
    IncidentSecurityReport,
    PostmortemReport,
    RecoveryPolicyReport,
    RunbookExecutionReport,
    SelfHealingReport,
)


class IIncidentArchVerifier(ABC):
    @abstractmethod
    def verify_architecture(self) -> IncidentArchitectureReport:
        pass


class IIncidentDetector(ABC):
    @abstractmethod
    def detect_incidents(self) -> IncidentDetectionReport:
        pass


class IIncidentClassifier(ABC):
    @abstractmethod
    def classify_incidents(self) -> IncidentClassificationReport:
        pass


class IRunbookEngine(ABC):
    @abstractmethod
    def execute_runbook(self, runbook_name: str) -> RunbookExecutionReport:
        pass


class ISelfHealingEngine(ABC):
    @abstractmethod
    def execute_self_healing_tests(self) -> SelfHealingReport:
        pass


class IRecoveryPolicyEngine(ABC):
    @abstractmethod
    def evaluate_recovery_policies(self) -> RecoveryPolicyReport:
        pass


class IIncidentCorrelationEngine(ABC):
    @abstractmethod
    def correlate_incident(self, incident_id: str) -> IncidentCorrelationReport:
        pass


class IIncidentKnowledgeBase(ABC):
    @abstractmethod
    def get_knowledge_report(self) -> IncidentKnowledgeReport:
        pass


class IPostmortemGenerator(ABC):
    @abstractmethod
    def generate_postmortem(self, incident_id: str) -> PostmortemReport:
        pass


class IIncidentSecurityAuditor(ABC):
    @abstractmethod
    def audit_security(self) -> IncidentSecurityReport:
        pass


class ICICDIncidentVerifier(ABC):
    @abstractmethod
    def verify_pipeline(self) -> CICDPipelineReport:
        pass


class IIncidentQualityScorer(ABC):
    @abstractmethod
    def compute_scorecard(
        self,
        arch_report: IncidentArchitectureReport,
        detect_report: IncidentDetectionReport,
        class_report: IncidentClassificationReport,
        runbook_report: RunbookExecutionReport,
        healing_report: SelfHealingReport,
        policy_report: RecoveryPolicyReport,
        correlation_report: IncidentCorrelationReport,
        knowledge_report: IncidentKnowledgeReport,
        postmortem_report: PostmortemReport,
        security_report: IncidentSecurityReport,
    ) -> IncidentQualityScorecard:
        pass
