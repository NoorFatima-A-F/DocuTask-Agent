"""
Enterprise Verification Domain Model & Persistence Architecture (Part 1.2).
"""
from app.platform_verification.domain_model.domain.verification_management import (
    VerificationDefinition, VerificationRequirement, VerificationCategory, VerificationStatus, RequirementSeverity
)
from app.platform_verification.domain_model.domain.verification_plan import (
    VerificationPlan, ExecutionStrategy, TimeoutPolicy, RetryPolicy, ResourceRequirements
)
from app.platform_verification.domain_model.domain.dataset_management import (
    Dataset, DatasetVersion, DatasetClassification, DatasetLineage
)
from app.platform_verification.domain_model.domain.environment_management import (
    Environment, EnvironmentSnapshot, EnvironmentType, HardwareProfile
)
from app.platform_verification.domain_model.domain.configuration_management import (
    Configuration, ConfigurationSnapshot
)
from app.platform_verification.domain_model.domain.execution_management import (
    VerificationExecution, ExecutionState, ExecutionAttempt, ExecutionEvent
)
from app.platform_verification.domain_model.domain.evidence_management import (
    EvidenceArtifact, EvidenceType, EvidenceMetadata, RetentionPolicy
)
from app.platform_verification.domain_model.domain.metrics_management import (
    MetricDefinition, MetricResult, MetricCategory
)
from app.platform_verification.domain_model.domain.statistical_evaluation import (
    StatisticalAnalysis, StatisticalMethod
)
from app.platform_verification.domain_model.domain.quality_management import (
    QualityGate, QualityDecision, QualityDecisionOutcome, GateSeverity
)
from app.platform_verification.domain_model.domain.certification_management import (
    Certification, CertificationLevel
)
from app.platform_verification.domain_model.domain.audit_management import AuditRecord
from app.platform_verification.domain_model.lineage.evidence_graph import (
    EvidenceGraphEngine, evidence_graph_engine
)
from app.platform_verification.domain_model.runtime.verification_domain_runtime import (
    VerificationDomainRuntime, verification_domain_runtime
)
