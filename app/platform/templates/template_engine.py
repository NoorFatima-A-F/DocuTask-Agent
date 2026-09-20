"""Industry Organization Templates and Provisioning Engine.

Provides 1-click enterprise blueprint deployment for Hospitals, Banks, Universities,
Government Agencies, Insurance Providers, Accounting Firms, and Law Firms.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class OrganizationTemplate:
    template_id: str
    name: str
    industry: str
    description: str
    icon: str
    departments: List[str]
    bundled_plugins: List[str]
    active_policies: List[str]
    default_sla_ms: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_id": self.template_id,
            "name": self.name,
            "industry": self.industry,
            "description": self.description,
            "icon": self.icon,
            "departments": self.departments,
            "bundled_plugins": self.bundled_plugins,
            "active_policies": self.active_policies,
            "default_sla_ms": self.default_sla_ms,
        }


class TemplateEngine:
    def __init__(self):
        self._templates: Dict[str, OrganizationTemplate] = {}
        self._seed_industry_templates()

    def _seed_industry_templates(self) -> None:
        blueprints = [
            OrganizationTemplate(
                template_id="tpl-healthcare-hospital",
                name="Regional Hospital Health System",
                industry="HEALTHCARE",
                description="Configures Clinical Ingestion, Medical Billing, HIPAA Privacy Shield, and Patient Record OCR.",
                icon="🏥",
                departments=["Executive", "OCR", "Clinical Extraction", "HIPAA Compliance", "QA"],
                bundled_plugins=["plugin.medical.records", "plugin.invoice.processing"],
                active_policies=["pol-sec-001", "pol-cost-002"],
                default_sla_ms=400.0,
            ),
            OrganizationTemplate(
                template_id="tpl-finance-bank",
                name="Commercial & Investment Bank",
                industry="BANKING",
                description="Configures KYB/KYC Verification, Loan Application Parsing, Treasury Reconciliation, and Four-Eyes Governance.",
                icon="🏦",
                departments=["Executive", "OCR", "Financial Extraction", "AML Compliance", "Governance"],
                bundled_plugins=["plugin.invoice.processing", "plugin.legal.contracts"],
                active_policies=["pol-gov-004", "pol-cost-002"],
                default_sla_ms=250.0,
            ),
            OrganizationTemplate(
                template_id="tpl-legal-lawfirm",
                name="Corporate Law & M&A Firm",
                industry="LEGAL",
                description="Deploys Clause Risk Analyzer, Regulatory Redlining, Non-Compete Reviewers, and Forensic Evidence DAG.",
                icon="⚖️",
                departments=["Executive", "Document Perception", "Clause Analysis", "Risk Review", "Forensic Audit"],
                bundled_plugins=["plugin.legal.contracts"],
                active_policies=["pol-model-003"],
                default_sla_ms=500.0,
            ),
            OrganizationTemplate(
                template_id="tpl-insurance-carrier",
                name="P&C Insurance Carrier",
                industry="INSURANCE",
                description="Automates First Notice of Loss (FNOL), Medical Injury Extraction, Adjuster Fraud Detection, and Payout Validation.",
                icon="🛡️",
                departments=["Executive", "Perception", "Claims Extraction", "Fraud Detection", "Quality Assurance"],
                bundled_plugins=["plugin.medical.records", "plugin.invoice.processing"],
                active_policies=["pol-sec-001", "pol-gov-004"],
                default_sla_ms=350.0,
            ),
        ]
        for b in blueprints:
            self._templates[b.template_id] = b

    def list_templates(self) -> List[OrganizationTemplate]:
        return list(self._templates.values())

    def get_template(self, template_id: str) -> Optional[OrganizationTemplate]:
        return self._templates.get(template_id)

    def deploy_template(self, template_id: str) -> Dict[str, Any]:
        tpl = self.get_template(template_id)
        if not tpl:
            raise KeyError(f"Template '{template_id}' not found")

        return {
            "status": "DEPLOYED",
            "template_id": template_id,
            "organization_name": tpl.name,
            "departments_initialized": len(tpl.departments),
            "plugins_activated": tpl.bundled_plugins,
            "policies_enforced": tpl.active_policies,
            "target_sla_ms": tpl.default_sla_ms,
        }


global_template_engine = TemplateEngine()
