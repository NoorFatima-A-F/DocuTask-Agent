"""Part C: AI Automation Template Marketplace."""

from typing import Dict, List, Optional
from ..domain.interfaces import ITemplateMarketplace
from ..domain.models import AutomationTemplate, IndustrySector, TemplateKPI


class TemplateMarketplace(ITemplateMarketplace):
    """Catalog of pre-configured enterprise AI automation templates."""

    def __init__(self):
        self._templates: Dict[str, AutomationTemplate] = {
            "TMPL-FIN-01": AutomationTemplate(
                template_id="TMPL-FIN-01",
                title="Autonomous Invoice Processing & ERP Sync Agent",
                industry=IndustrySector.FINANCE,
                category="Accounts Payable",
                description="End-to-end automated email invoice ingestion, OCR parsing, 3-way PO matching, and QuickBooks/SAP posting.",
                agent_roles_required=["ExtractionAgent", "ValidationAgent", "DecisionAgent"],
                tools_required=["OCRProcessor", "POMatchingEngine", "ERPConnector", "SanctionsChecker"],
                connectors_required=["Gmail", "Outlook", "QuickBooks", "Slack"],
                kpis=[
                    TemplateKPI(metric_name="Processing Time per Invoice", baseline_value="18 minutes", projected_ai_value="4.5 seconds", expected_improvement="99.5% faster"),
                    TemplateKPI(metric_name="Cost per Invoice Processed", baseline_value="$35.00", projected_ai_value="$0.025", expected_improvement="92.8% savings"),
                    TemplateKPI(metric_name="Straight-Through Processing (STP)", baseline_value="12%", projected_ai_value="91.5%", expected_improvement="+79.5% STP"),
                ],
                estimated_deployment_minutes=5,
                is_featured=True,
                rating=4.95,
            ),
            "TMPL-HR-02": AutomationTemplate(
                template_id="TMPL-HR-02",
                title="Candidate Resume Screening & Competency Ranking Agent",
                industry=IndustrySector.HR_RECRUITING,
                category="Talent Acquisition",
                description="Ingests bulk PDF/DOCX resumes, ranks candidates by technical competency match, and automatically schedules interviews.",
                agent_roles_required=["ParserAgent", "RankingAgent", "SchedulerAgent"],
                tools_required=["ResumeParser", "SkillVectorMatcher", "CalendarBookingTool"],
                connectors_required=["GoogleDrive", "Greenhouse", "Outlook", "Slack"],
                kpis=[
                    TemplateKPI(metric_name="Time-to-Shortlist", baseline_value="7.5 days", projected_ai_value="3 minutes", expected_improvement="99.3% reduction"),
                    TemplateKPI(metric_name="Candidate Matching Accuracy", baseline_value="68.0%", projected_ai_value="96.5%", expected_improvement="+28.5% precision"),
                ],
                estimated_deployment_minutes=4,
                is_featured=True,
                rating=4.90,
            ),
            "TMPL-LEG-03": AutomationTemplate(
                template_id="TMPL-LEG-03",
                title="Commercial Contract Clause Risk & Compliance Review Agent",
                industry=IndustrySector.LEGAL,
                category="Contract Intelligence",
                description="Extracts indemnification caps, governing law, and SLA clauses to flag non-standard enterprise liability risks.",
                agent_roles_required=["LegalExtractionAgent", "RiskAuditorAgent"],
                tools_required=["ClauseExtractor", "LegalRiskScorer", "RedlineGenerator"],
                connectors_required=["SharePoint", "OneDrive", "DocuSign", "Teams"],
                kpis=[
                    TemplateKPI(metric_name="Contract Review Cycle", baseline_value="4 days", projected_ai_value="45 seconds", expected_improvement="99.0% reduction"),
                    TemplateKPI(metric_name="Risk Detection Precision", baseline_value="82.0%", projected_ai_value="98.5%", expected_improvement="+16.5% coverage"),
                ],
                estimated_deployment_minutes=6,
                is_featured=True,
                rating=4.92,
            ),
            "TMPL-HLT-04": AutomationTemplate(
                template_id="TMPL-HLT-04",
                title="Clinical Prior Authorization & Claims Triage Agent",
                industry=IndustrySector.HEALTHCARE,
                category="Healthcare Operations",
                description="Parses clinical chart notes against ICD-10 / CPT criteria to recommend prior authorization approval.",
                agent_roles_required=["ClinicalReasoningAgent", "MedicalCodingAgent"],
                tools_required=["ICD10Lookup", "MedicalGuidelinesMatcher", "EHRConnector"],
                connectors_required=["EpicEHR", "Cerner", "SecureFHIRGateway"],
                kpis=[
                    TemplateKPI(metric_name="Authorization Turnaround", baseline_value="72 hours", projected_ai_value="12 seconds", expected_improvement="99.9% faster"),
                    TemplateKPI(metric_name="Denial Appeal Accuracy", baseline_value="74.0%", projected_ai_value="97.8%", expected_improvement="+23.8% success"),
                ],
                estimated_deployment_minutes=7,
                is_featured=False,
                rating=4.88,
            ),
            "TMPL-SUP-05": AutomationTemplate(
                template_id="TMPL-SUP-05",
                title="Customer Support Ticket Multi-Agent Auto-Triage",
                industry=IndustrySector.CUSTOMER_SUPPORT,
                category="Customer Operations",
                description="Classifies inbound customer support queries, fetches account context, and generates drafted responses with RAG knowledge.",
                agent_roles_required=["TriageAgent", "KnowledgeRetrievalAgent", "DraftingAgent"],
                tools_required=["SentimentAnalyzer", "RAGKnowledgeSearch", "ZendeskAPI"],
                connectors_required=["Zendesk", "Salesforce", "Slack"],
                kpis=[
                    TemplateKPI(metric_name="First Response Time", baseline_value="4.5 hours", projected_ai_value="1.2 minutes", expected_improvement="99.5% reduction"),
                    TemplateKPI(metric_name="First Contact Resolution (FCR)", baseline_value="48.0%", projected_ai_value="84.0%", expected_improvement="+36.0% resolution"),
                ],
                estimated_deployment_minutes=3,
                is_featured=False,
                rating=4.85,
            ),
        }

    def list_templates(self, industry_filter: Optional[str] = None) -> List[AutomationTemplate]:
        if not industry_filter:
            return list(self._templates.values())
        return [
            t for t in self._templates.values()
            if t.industry.value.lower() == industry_filter.lower() or t.industry.name.lower() == industry_filter.lower()
        ]

    def get_template(self, template_id: str) -> Optional[AutomationTemplate]:
        return self._templates.get(template_id)
