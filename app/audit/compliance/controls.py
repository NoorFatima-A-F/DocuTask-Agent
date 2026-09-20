"""Compliance Controls Domain Models & Registry."""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from .frameworks import ComplianceFramework


class ControlStatus(str, Enum):
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    PARTIALLY_COMPLIANT = "PARTIALLY_COMPLIANT"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    PENDING_REVIEW = "PENDING_REVIEW"


class ComplianceControl(BaseModel):
    control_id: str
    framework: ComplianceFramework
    code: str
    title: str
    requirement: str
    description: str
    required_evidence_types: List[str] = Field(default_factory=list)
    status: ControlStatus = ControlStatus.PENDING_REVIEW
    owner: str = "compliance_officer"
    frequency: str = "CONTINUOUS"  # CONTINUOUS, MONTHLY, QUARTERLY, ANNUAL


# Standard Baseline Controls
DEFAULT_COMPLIANCE_CONTROLS: List[ComplianceControl] = [
    # SOC 2
    ComplianceControl(
        control_id="SOC2-CC7.2",
        framework=ComplianceFramework.SOC2,
        code="CC7.2",
        title="Security Monitoring & Audit Logging",
        requirement="The entity monitors system components and user activities to detect anomalous actions.",
        description="Continuous immutable audit trail of logins, permissions, and operations.",
        required_evidence_types=["AUTHENTICATION", "AUTHORIZATION", "SYSTEM"],
        status=ControlStatus.COMPLIANT,
    ),
    ComplianceControl(
        control_id="SOC2-CC6.1",
        framework=ComplianceFramework.SOC2,
        code="CC6.1",
        title="Logical Access & Role Security",
        requirement="Logical access to platform assets and tools is restricted to authorized roles.",
        description="Tool permissions and RBAC authorization verification.",
        required_evidence_types=["AUTHORIZATION", "GOVERNANCE_EVIDENCE"],
        status=ControlStatus.COMPLIANT,
    ),
    # ISO 27001
    ComplianceControl(
        control_id="ISO-A12.4.1",
        framework=ComplianceFramework.ISO27001,
        code="A.12.4.1",
        title="Event Logging",
        requirement="Event logs recording user activities, exceptions, faults and information security events are kept.",
        description="Append-only cryptographic event logging across tenants.",
        required_evidence_types=["EXECUTION_EVIDENCE", "SYSTEM"],
        status=ControlStatus.COMPLIANT,
    ),
    # GDPR
    ComplianceControl(
        control_id="GDPR-Art30",
        framework=ComplianceFramework.GDPR,
        code="Art. 30",
        title="Records of Processing Activities",
        requirement="Maintain a record of processing activities under its responsibility.",
        description="Data access, transformation, and AI inference audit trails.",
        required_evidence_types=["DATA", "DATA_EVIDENCE"],
        status=ControlStatus.COMPLIANT,
    ),
    # NIST AI RMF
    ComplianceControl(
        control_id="NIST-GOVERN-1.2",
        framework=ComplianceFramework.NIST_AI_RMF,
        code="GOVERN 1.2",
        title="AI System Governance & Lineage",
        requirement="Roles, responsibilities, and system lineage are documented and tracked.",
        description="Model registry records, prompt versions, and evaluation metrics.",
        required_evidence_types=["AI", "AI_EVIDENCE", "GOVERNANCE_EVIDENCE"],
        status=ControlStatus.COMPLIANT,
    ),
    ComplianceControl(
        control_id="NIST-MANAGE-2.4",
        framework=ComplianceFramework.NIST_AI_RMF,
        code="MANAGE 2.4",
        title="AI Safety & Incident Tracking",
        requirement="Mechanisms are in place to detect and respond to AI safety incidents.",
        description="Safety gateway events, injection blocks, and incident lifecycle tracking.",
        required_evidence_types=["SAFETY", "SAFETY_EVIDENCE"],
        status=ControlStatus.COMPLIANT,
    ),
    # EU AI ACT
    ComplianceControl(
        control_id="EU-AI-Art12",
        framework=ComplianceFramework.EU_AI_ACT,
        code="Art. 12",
        title="High-Risk AI Record-Keeping",
        requirement="High-risk AI systems must have automatic recording of events (logs) over their lifetime.",
        description="End-to-end provenance of prompts, models, knowledge inputs, and tool executions.",
        required_evidence_types=["AI", "AI_EVIDENCE", "EXECUTION_EVIDENCE"],
        status=ControlStatus.COMPLIANT,
    ),
    ComplianceControl(
        control_id="EU-AI-Art14",
        framework=ComplianceFramework.EU_AI_ACT,
        code="Art. 14",
        title="Human Oversight for AI Decisions",
        requirement="High-risk AI systems must enable effective oversight by natural persons.",
        description="Human approval workflows for high-risk and destructive actions.",
        required_evidence_types=["GOVERNANCE", "GOVERNANCE_EVIDENCE"],
        status=ControlStatus.COMPLIANT,
    ),
]
