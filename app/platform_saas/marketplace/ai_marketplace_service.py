"""
Phase 13.19: Enterprise AI Marketplace & Template Ecosystem.
Enables sharing, discovering, and installing Agent Packs, Workflow Templates, OCR Pipelines, and Prompt Packs.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid
from app.platform_saas.models.schemas import MarketplaceAsset, AssetType


class AIMarketplaceService:
    def __init__(self):
        self._assets: Dict[str, MarketplaceAsset] = {}
        self._installed_assets: Dict[str, List[str]] = {}  # tenant_id -> list of asset_ids
        self._seed_default_marketplace()

    def _seed_default_marketplace(self) -> None:
        a1 = MarketplaceAsset(
            asset_id="asset_financial_reconciliation",
            title="Autonomous Financial Reconciliation Agent Pack",
            asset_type=AssetType.AGENT_PACK,
            publisher_tenant_id="tenant_acme_corp",
            publisher_name="Acme Finance AI Labs",
            version="2.4.0",
            description="End-to-end multi-agent mesh for 3-way invoice, PO, and bank statement matching.",
            downloads_count=1420,
            rating=4.95,
            verified=True,
            price_monthly_usd=199.0,
            tags=["finance", "reconciliation", "invoices", "multi-agent"],
        )
        a2 = MarketplaceAsset(
            asset_id="asset_hipaa_redaction_pipeline",
            title="HIPAA & GDPR Medical Document Redaction Pipeline",
            asset_type=AssetType.OCR_PIPELINE,
            publisher_tenant_id="tenant_globex_health",
            publisher_name="Globex Healthcare Systems",
            version="1.8.2",
            description="High-throughput PHI/PII redaction and anonymization pipeline with 99.8% precision.",
            downloads_count=980,
            rating=4.88,
            verified=True,
            price_monthly_usd=299.0,
            tags=["hipaa", "medical", "redaction", "compliance"],
        )
        a3 = MarketplaceAsset(
            asset_id="asset_legal_contract_analyzer",
            title="Legal Contract Risk & Clause Extractor",
            asset_type=AssetType.WORKFLOW_TEMPLATE,
            publisher_tenant_id="tenant_acme_corp",
            publisher_name="Enterprise Legal AI",
            version="3.1.0",
            description="Autonomous extraction and deviation scoring for master service agreements and NDAs.",
            downloads_count=2150,
            rating=4.92,
            verified=True,
            price_monthly_usd=0.0,
            tags=["legal", "contracts", "clauses", "risk"],
        )
        a4 = MarketplaceAsset(
            asset_id="asset_sap_s4hana_connector",
            title="SAP S/4HANA Autonomous Posting Connector",
            asset_type=AssetType.TOOL_PLUGIN,
            publisher_tenant_id="tenant_acme_corp",
            publisher_name="Acme ERP Solutions",
            version="1.2.0",
            description="Bi-directional REST/OData connector for posting validated GL entries and vendor items.",
            downloads_count=640,
            rating=4.75,
            verified=True,
            price_monthly_usd=450.0,
            tags=["sap", "erp", "connector", "odata"],
        )

        for asset in [a1, a2, a3, a4]:
            self._assets[asset.asset_id] = asset

        self._installed_assets["tenant_acme_corp"] = ["asset_financial_reconciliation", "asset_sap_s4hana_connector"]
        self._installed_assets["tenant_globex_health"] = ["asset_hipaa_redaction_pipeline"]

    def publish_asset(
        self,
        title: str,
        asset_type: AssetType,
        publisher_tenant_id: str,
        publisher_name: str,
        description: str,
        version: str = "1.0.0",
        price_monthly_usd: float = 0.0,
        tags: Optional[List[str]] = None,
    ) -> MarketplaceAsset:
        asset_id = f"asset_{uuid.uuid4().hex[:8]}"
        asset = MarketplaceAsset(
            asset_id=asset_id,
            title=title,
            asset_type=asset_type,
            publisher_tenant_id=publisher_tenant_id,
            publisher_name=publisher_name,
            version=version,
            description=description,
            downloads_count=0,
            rating=5.0,
            verified=True,
            price_monthly_usd=price_monthly_usd,
            tags=tags or [],
        )
        self._assets[asset_id] = asset
        return asset

    def get_asset(self, asset_id: str) -> Optional[MarketplaceAsset]:
        return self._assets.get(asset_id)

    def list_assets(self, asset_type: Optional[AssetType] = None, tag: Optional[str] = None) -> List[MarketplaceAsset]:
        items = list(self._assets.values())
        if asset_type:
            items = [a for a in items if a.asset_type == asset_type]
        if tag:
            items = [a for a in items if tag.lower() in [t.lower() for t in a.tags]]
        return items

    def install_asset(self, tenant_id: str, asset_id: str) -> Dict[str, Any]:
        asset = self._assets.get(asset_id)
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")
        if tenant_id not in self._installed_assets:
            self._installed_assets[tenant_id] = []
        if asset_id not in self._installed_assets[tenant_id]:
            self._installed_assets[tenant_id].append(asset_id)
            asset.downloads_count += 1
        return {
            "tenant_id": tenant_id,
            "asset_id": asset_id,
            "installed": True,
            "installed_at": datetime.now(timezone.utc).isoformat(),
        }

    def list_tenant_installed(self, tenant_id: str) -> List[MarketplaceAsset]:
        installed_ids = self._installed_assets.get(tenant_id, [])
        return [self._assets[aid] for aid in installed_ids if aid in self._assets]
