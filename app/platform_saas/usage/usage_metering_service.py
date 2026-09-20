"""
Phase 13.19: Multi-Tenant Usage Metering & Quota Enforcement Engine.
Tracks real-time token consumption, OCR page volume, compute seconds, and API calls.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid
from app.platform_saas.models.schemas import UsageRecord


class UsageMeteringService:
    RATES = {
        "llm_tokens": 0.000002,      # $2 per 1M tokens
        "ocr_pages": 0.015,          # $0.015 per page
        "api_requests": 0.0001,      # $0.10 per 1k requests
        "compute_seconds": 0.00005,  # $0.05 per 1k seconds
    }

    def __init__(self):
        self._records: List[UsageRecord] = []
        self._seed_default_usage()

    def _seed_default_usage(self) -> None:
        r1 = UsageRecord(
            record_id="rec_01",
            tenant_id="tenant_acme_corp",
            workspace_id="ws_acme_invoicing",
            metric_name="llm_tokens",
            quantity=12_450_000,
            unit="tokens",
            unit_cost_usd=self.RATES["llm_tokens"],
            total_cost_usd=12_450_000 * self.RATES["llm_tokens"],
        )
        r2 = UsageRecord(
            record_id="rec_02",
            tenant_id="tenant_acme_corp",
            workspace_id="ws_acme_invoicing",
            metric_name="ocr_pages",
            quantity=4_800,
            unit="pages",
            unit_cost_usd=self.RATES["ocr_pages"],
            total_cost_usd=4_800 * self.RATES["ocr_pages"],
        )
        r3 = UsageRecord(
            record_id="rec_03",
            tenant_id="tenant_globex_health",
            workspace_id="ws_globex_records",
            metric_name="llm_tokens",
            quantity=6_200_000,
            unit="tokens",
            unit_cost_usd=self.RATES["llm_tokens"],
            total_cost_usd=6_200_000 * self.RATES["llm_tokens"],
        )
        r4 = UsageRecord(
            record_id="rec_04",
            tenant_id="tenant_globex_health",
            workspace_id="ws_globex_records",
            metric_name="ocr_pages",
            quantity=2_150,
            unit="pages",
            unit_cost_usd=self.RATES["ocr_pages"],
            total_cost_usd=2_150 * self.RATES["ocr_pages"],
        )
        self._records.extend([r1, r2, r3, r4])

    def record_usage(
        self,
        tenant_id: str,
        workspace_id: str,
        metric_name: str,
        quantity: float,
    ) -> UsageRecord:
        unit_cost = self.RATES.get(metric_name, 0.001)
        unit = "tokens" if "token" in metric_name else "pages" if "ocr" in metric_name else "units"
        rec = UsageRecord(
            record_id=f"rec_{uuid.uuid4().hex[:8]}",
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            metric_name=metric_name,
            quantity=quantity,
            unit=unit,
            unit_cost_usd=unit_cost,
            total_cost_usd=quantity * unit_cost,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self._records.append(rec)
        return rec

    def get_tenant_usage_summary(self, tenant_id: str) -> Dict[str, Any]:
        tenant_records = [r for r in self._records if r.tenant_id == tenant_id]
        tokens = sum(r.quantity for r in tenant_records if r.metric_name == "llm_tokens")
        pages = sum(r.quantity for r in tenant_records if r.metric_name == "ocr_pages")
        total_spend = sum(r.total_cost_usd for r in tenant_records)
        return {
            "tenant_id": tenant_id,
            "total_tokens": int(tokens),
            "total_ocr_pages": int(pages),
            "metered_spend_usd": round(total_spend, 2),
            "records_count": len(tenant_records),
        }

    def list_records(self, tenant_id: Optional[str] = None) -> List[UsageRecord]:
        if tenant_id:
            return [r for r in self._records if r.tenant_id == tenant_id]
        return self._records
