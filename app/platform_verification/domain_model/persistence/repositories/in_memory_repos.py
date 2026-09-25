"""
Repositories for Verification Platform Bounded Contexts.
"""
from typing import Dict, List, Optional
from app.platform_verification.domain_model.domain.verification_management import VerificationDefinition
from app.platform_verification.domain_model.domain.verification_plan import VerificationPlan
from app.platform_verification.domain_model.domain.dataset_management import Dataset, DatasetVersion
from app.platform_verification.domain_model.domain.environment_management import EnvironmentSnapshot
from app.platform_verification.domain_model.domain.configuration_management import ConfigurationSnapshot
from app.platform_verification.domain_model.domain.execution_management import VerificationExecution
from app.platform_verification.domain_model.domain.evidence_management import EvidenceArtifact
from app.platform_verification.domain_model.domain.metrics_management import MetricResult
from app.platform_verification.domain_model.domain.quality_management import QualityDecision
from app.platform_verification.domain_model.domain.certification_management import Certification
from app.platform_verification.domain_model.domain.audit_management import AuditRecord


class VerificationDomainRepository:
    def __init__(self):
        self.definitions: Dict[str, VerificationDefinition] = {}
        self.plans: Dict[str, VerificationPlan] = {}
        self.datasets: Dict[str, Dataset] = {}
        self.dataset_versions: Dict[str, DatasetVersion] = {}
        self.environment_snapshots: Dict[str, EnvironmentSnapshot] = {}
        self.configuration_snapshots: Dict[str, ConfigurationSnapshot] = {}
        self.executions: Dict[str, VerificationExecution] = {}
        self.evidence: Dict[str, List[EvidenceArtifact]] = {}
        self.metrics: Dict[str, List[MetricResult]] = {}
        self.quality_decisions: Dict[str, List[QualityDecision]] = {}
        self.certifications: Dict[str, Certification] = {}
        self.audit_records: List[AuditRecord] = []
        self._last_audit_hash: str = "0" * 64

    # Definitions
    def save_definition(self, definition: VerificationDefinition) -> VerificationDefinition:
        self.definitions[definition.definition_id] = definition
        return definition

    def get_definition(self, definition_id: str) -> Optional[VerificationDefinition]:
        return self.definitions.get(definition_id)

    def list_definitions(self) -> List[VerificationDefinition]:
        return list(self.definitions.values())

    # Plans
    def save_plan(self, plan: VerificationPlan) -> VerificationPlan:
        self.plans[plan.plan_id] = plan
        return plan

    def get_plan(self, plan_id: str) -> Optional[VerificationPlan]:
        return self.plans.get(plan_id)

    # Datasets
    def save_dataset(self, dataset: Dataset) -> Dataset:
        self.datasets[dataset.dataset_id] = dataset
        return dataset

    def save_dataset_version(self, dver: DatasetVersion) -> DatasetVersion:
        self.dataset_versions[dver.dataset_version_id] = dver
        return dver

    def get_dataset_version(self, dver_id: str) -> Optional[DatasetVersion]:
        return self.dataset_versions.get(dver_id)

    # Snapshots
    def save_env_snapshot(self, snap: EnvironmentSnapshot) -> EnvironmentSnapshot:
        self.environment_snapshots[snap.snapshot_id] = snap
        return snap

    def save_cfg_snapshot(self, snap: ConfigurationSnapshot) -> ConfigurationSnapshot:
        self.configuration_snapshots[snap.snapshot_id] = snap
        return snap

    # Executions
    def save_execution(self, execution: VerificationExecution) -> VerificationExecution:
        self.executions[execution.execution_id] = execution
        return execution

    def get_execution(self, execution_id: str) -> Optional[VerificationExecution]:
        return self.executions.get(execution_id)

    def list_executions(self) -> List[VerificationExecution]:
        return list(self.executions.values())

    # Evidence
    def add_evidence(self, artifact: EvidenceArtifact) -> EvidenceArtifact:
        if artifact.execution_id not in self.evidence:
            self.evidence[artifact.execution_id] = []
        self.evidence[artifact.execution_id].append(artifact)
        return artifact

    def get_evidence_for_execution(self, execution_id: str) -> List[EvidenceArtifact]:
        return self.evidence.get(execution_id, [])

    # Metrics
    def add_metric_result(self, metric: MetricResult) -> MetricResult:
        if metric.execution_id not in self.metrics:
            self.metrics[metric.execution_id] = []
        self.metrics[metric.execution_id].append(metric)
        return metric

    def get_metrics_for_execution(self, execution_id: str) -> List[MetricResult]:
        return self.metrics.get(execution_id, [])

    # Quality Decisions
    def add_quality_decision(self, decision: QualityDecision) -> QualityDecision:
        if decision.execution_id not in self.quality_decisions:
            self.quality_decisions[decision.execution_id] = []
        self.quality_decisions[decision.execution_id].append(decision)
        return decision

    # Certifications
    def save_certification(self, cert: Certification) -> Certification:
        self.certifications[cert.certification_id] = cert
        return cert

    def get_certification(self, cert_id: str) -> Optional[Certification]:
        return self.certifications.get(cert_id)

    def get_certification_for_execution(self, execution_id: str) -> Optional[Certification]:
        for c in self.certifications.values():
            if c.execution_id == execution_id:
                return c
        return None

    # Audit
    def append_audit_record(self, entity_type: str, entity_id: str, action: str, new_state: dict, previous_state: Optional[dict] = None) -> AuditRecord:
        record = AuditRecord(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            previous_state=previous_state,
            new_state=new_state,
            previous_hash=self._last_audit_hash
        )
        record.compute_hash()
        self._last_audit_hash = record.record_hash
        self.audit_records.append(record)
        return record

    def list_audit_trail(self) -> List[AuditRecord]:
        return list(self.audit_records)


verification_domain_repository = VerificationDomainRepository()
