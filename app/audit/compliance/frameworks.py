"""Compliance Framework Definitions & Profiles."""

from enum import Enum
from typing import Dict, List
from pydantic import BaseModel, Field


class ComplianceFramework(str, Enum):
    SOC2 = "SOC2"
    ISO27001 = "ISO27001"
    GDPR = "GDPR"
    HIPAA = "HIPAA"
    PCI_DSS = "PCI_DSS"
    NIST_AI_RMF = "NIST_AI_RMF"
    ISO42001 = "ISO42001"
    EU_AI_ACT = "EU_AI_ACT"


class FrameworkProfile(BaseModel):
    framework: ComplianceFramework
    name: str
    description: str
    target_domains: List[str] = Field(default_factory=list)


FRAMEWORK_PROFILES: Dict[ComplianceFramework, FrameworkProfile] = {
    ComplianceFramework.SOC2: FrameworkProfile(
        framework=ComplianceFramework.SOC2,
        name="SOC 2 Type II",
        description="AICPA Trust Services Criteria (Security, Availability, Confidentiality)",
        target_domains=["Security Monitoring", "Access Controls", "Change Management"],
    ),
    ComplianceFramework.ISO27001: FrameworkProfile(
        framework=ComplianceFramework.ISO27001,
        name="ISO/IEC 27001:2022",
        description="Information Security Management Systems",
        target_domains=["Event Logging", "Access Control", "Operational Security"],
    ),
    ComplianceFramework.GDPR: FrameworkProfile(
        framework=ComplianceFramework.GDPR,
        name="EU General Data Protection Regulation",
        description="Protection of natural persons with regard to personal data processing",
        target_domains=["Data Lineage", "Consent & Erasure", "Records of Processing"],
    ),
    ComplianceFramework.HIPAA: FrameworkProfile(
        framework=ComplianceFramework.HIPAA,
        name="HIPAA Security Rule",
        description="Security standards for the protection of Electronic Protected Health Information",
        target_domains=["Audit Controls", "PHI Integrity", "Access Management"],
    ),
    ComplianceFramework.NIST_AI_RMF: FrameworkProfile(
        framework=ComplianceFramework.NIST_AI_RMF,
        name="NIST AI Risk Management Framework 1.0",
        description="Guidance for managing risks in the design, development, and use of AI",
        target_domains=["Govern", "Map", "Measure", "Manage"],
    ),
    ComplianceFramework.ISO42001: FrameworkProfile(
        framework=ComplianceFramework.ISO42001,
        name="ISO/IEC 42001:2023",
        description="Artificial Intelligence Management System (AIMS)",
        target_domains=["AI Risk Management", "AI Impact Assessment", "AI Life Cycle"],
    ),
    ComplianceFramework.EU_AI_ACT: FrameworkProfile(
        framework=ComplianceFramework.EU_AI_ACT,
        name="European Union Artificial Intelligence Act",
        description="Harmonised rules on artificial intelligence (High-risk AI obligations)",
        target_domains=["Record-keeping", "Human Oversight", "Transparency", "Cybersecurity"],
    ),
}
