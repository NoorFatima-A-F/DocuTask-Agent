"""
Phase 13.20: Enterprise AI Starter Template Catalog.
Provides turnkey templates for rapid agent scaffolding.
"""

from typing import Dict, List, Optional, Any
from app.platform_ai_lifecycle.models.schemas import AgentTemplate, AgentCategory


class TemplateCatalogService:
    def __init__(self):
        self._templates: Dict[str, AgentTemplate] = {}
        self._seed_templates()

    def _seed_templates(self) -> None:
        t1 = AgentTemplate(
            template_id="tmpl_invoice_reconciliation",
            name="Autonomous Invoice & PO Reconciliation Agent",
            category=AgentCategory.FINANCIAL_AUDIT,
            description="3-way automated matching of invoices, POs, and receipts with ERP connector.",
            recommended_model="gemini-pro",
            default_tools=["tool_erp_lookup", "tool_ocr_extract", "tool_bank_statement_verify"],
            default_prompt="You are an autonomous invoice reconciliation agent. Compare line items against purchase orders.",
        )
        t2 = AgentTemplate(
            template_id="tmpl_medical_hipaa_redaction",
            name="HIPAA & GDPR Clinical Document Redactor",
            category=AgentCategory.COMPLIANCE,
            description="High-precision PHI/PII redactor for medical charts and patient records.",
            recommended_model="gemini-pro",
            default_tools=["tool_ner_medical", "tool_redaction_mask"],
            default_prompt="You are an expert compliance redactor. Mask all 18 HIPAA identifier types.",
        )
        t3 = AgentTemplate(
            template_id="tmpl_legal_contract_analyzer",
            name="Legal Contract Risk & Deviation Analyzer",
            category=AgentCategory.LEGAL_ANALYSIS,
            description="Extracts contractual clauses, identifies non-standard liabilities and risks.",
            recommended_model="gemini-pro",
            default_tools=["tool_clause_extractor", "tool_legal_kb_search"],
            default_prompt="Analyze legal contracts against corporate standard playbook for risk deviations.",
        )
        for t in [t1, t2, t3]:
            self._templates[t.template_id] = t

    def list_templates(self, category: Optional[AgentCategory] = None) -> List[AgentTemplate]:
        items = list(self._templates.values())
        if category:
            items = [t for t in items if t.category == category]
        return items

    def get_template(self, template_id: str) -> Optional[AgentTemplate]:
        return self._templates.get(template_id)
