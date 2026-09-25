"""Part F: Human-in-the-Loop Collaboration, Approval & Exception Center."""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from ..domain.interfaces import IApprovalCenterEngine
from ..domain.models import (
    ApprovalItem,
    ApprovalStatus,
    BoundingBoxCitation,
    ExceptionItem,
    ExceptionSeverity,
)


class ApprovalCenterEngine(IApprovalCenterEngine):
    """Manages human-in-the-loop review, confidence exception routing, and supervisor sign-offs."""

    def __init__(self):
        self._approvals: Dict[str, ApprovalItem] = {}
        self._exceptions: Dict[str, ExceptionItem] = {}
        self._seed_default_items()

    def _seed_default_items(self):
        # Seed Approvals
        app1 = ApprovalItem(
            approval_id="APP-2026-001",
            tenant_id="TENANT-FIN-01",
            workflow_id="WF-DEFAULT-INVOICE",
            document_title="Invoice_GlobalLogistics_INV-8891.pdf",
            document_type="Vendor Invoice",
            ai_confidence_score=0.982,
            recommended_action="APPROVE_AND_POST_TO_QUICKBOOKS",
            status=ApprovalStatus.PENDING,
            citations=[
                BoundingBoxCitation(page_number=1, coordinates=[0.12, 0.15, 0.45, 0.22], extracted_text="Acme Global Solutions Inc.", field_name="vendor_name"),
                BoundingBoxCitation(page_number=1, coordinates=[0.75, 0.15, 0.92, 0.20], extracted_text="$14,500.50", field_name="total_amount"),
                BoundingBoxCitation(page_number=1, coordinates=[0.75, 0.85, 0.90, 0.90], extracted_text="INV-2026-8891", field_name="invoice_number"),
            ],
            reviewer_notes="High-confidence extraction verified against PO #PO-9912.",
        )
        app2 = ApprovalItem(
            approval_id="APP-2026-002",
            tenant_id="TENANT-LEG-04",
            workflow_id="WF-LEGAL-REVIEW",
            document_title="Master_Services_Agreement_Nexus.pdf",
            document_type="Legal Contract",
            ai_confidence_score=0.945,
            recommended_action="FLAG_UNLIMITED_LIABILITY_CLAUSE",
            status=ApprovalStatus.PENDING,
            citations=[
                BoundingBoxCitation(page_number=4, coordinates=[0.10, 0.45, 0.85, 0.60], extracted_text="Neither party shall be subject to any limitation of liability for data breaches.", field_name="liability_cap"),
            ],
            reviewer_notes="Detected non-standard indemnification clause requiring Legal Counsel approval.",
        )
        self._approvals[app1.approval_id] = app1
        self._approvals[app2.approval_id] = app2

        # Seed Exceptions
        exc1 = ExceptionItem(
            exception_id="EXC-2026-001",
            tenant_id="TENANT-FIN-01",
            workflow_id="WF-DEFAULT-INVOICE",
            severity=ExceptionSeverity.MEDIUM,
            error_type="MISSING_TAX_ID",
            description="Vendor 'BioTech Laboratories GmbH' invoice DE-99412-B missing European VAT ID.",
            suggested_remediation="Auto-retrieve VAT ID from Vendor Master Database or prompt AP analyst.",
            resolved=False,
        )
        exc2 = ExceptionItem(
            exception_id="EXC-2026-002",
            tenant_id="TENANT-HLT-02",
            workflow_id="WF-PRIOR-AUTH",
            severity=ExceptionSeverity.LOW,
            error_type="UNCLEAR_CLINICAL_NOTE_SCAN",
            description="Page 3 of MRI clinical justification contains low-contrast blurry scan.",
            suggested_remediation="Trigger Multimodal OCR image enhancement filter or request high-res re-upload.",
            resolved=False,
        )
        self._exceptions[exc1.exception_id] = exc1
        self._exceptions[exc2.exception_id] = exc2

    def get_pending_approvals(self, tenant_id: Optional[str] = None) -> List[ApprovalItem]:
        items = list(self._approvals.values())
        if tenant_id:
            items = [i for i in items if i.tenant_id == tenant_id]
        return [i for i in items if i.status == ApprovalStatus.PENDING]

    def submit_decision(self, approval_id: str, decision: str, notes: Optional[str] = None) -> ApprovalItem:
        item = self._approvals.get(approval_id)
        if not item:
            raise KeyError(f"Approval item '{approval_id}' not found")

        decision_upper = decision.upper()
        if "APPROV" in decision_upper:
            item.status = ApprovalStatus.APPROVED
        elif "REJECT" in decision_upper:
            item.status = ApprovalStatus.REJECTED
        elif "ESCALAT" in decision_upper:
            item.status = ApprovalStatus.ESCALATED
        else:
            item.status = ApprovalStatus.APPROVED

        item.reviewer_notes = notes or f"Decision submitted: {decision_upper}"
        item.decided_at = datetime.now(timezone.utc).isoformat()
        return item

    def list_exceptions(self, tenant_id: Optional[str] = None) -> List[ExceptionItem]:
        if not tenant_id:
            return list(self._exceptions.values())
        return [e for e in self._exceptions.values() if e.tenant_id == tenant_id]
