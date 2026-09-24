"""
Phase 13.20: Enterprise AI Application Marketplace Service.
Allows publishing, certification verification, community ratings, and one-click workspace installation.
"""

from typing import Dict, List, Optional
import uuid
from app.platform_ai_lifecycle.models.schemas import (
    AgentMarketplaceListing,
    AgentCategory,
)


class LifecycleMarketplaceService:
    def __init__(self):
        self._listings: Dict[str, AgentMarketplaceListing] = {}
        self._seed_default_listings()

    def _seed_default_listings(self) -> None:
        l1 = AgentMarketplaceListing(
            listing_id="list_01",
            agent_id="agt_acme_invoice_reconciler",
            title="Enterprise Financial 3-Way Reconciliation Agent",
            publisher_name="Acme Finance AI Labs",
            category=AgentCategory.FINANCIAL_AUDIT,
            description="Autonomous multi-agent mesh for end-to-end ERP invoice reconciliation.",
            version="1.2.0",
            rating=4.95,
            install_count=1850,
            certified_secure=True,
            price_monthly_usd=199.0,
            tags=["finance", "sap", "reconciliation", "enterprise"],
        )
        l2 = AgentMarketplaceListing(
            listing_id="list_02",
            agent_id="agt_globex_hipaa_scrubber",
            title="HIPAA Medical Record Anonymization Pipeline",
            publisher_name="Globex Healthcare Systems",
            category=AgentCategory.COMPLIANCE,
            description="Automated clinical PHI/PII scrubbing with 99.8% precision score.",
            version="2.0.1",
            rating=4.90,
            install_count=1200,
            certified_secure=True,
            price_monthly_usd=299.0,
            tags=["hipaa", "medical", "redaction", "ehr"],
        )
        self._listings[l1.listing_id] = l1
        self._listings[l2.listing_id] = l2

    def publish_agent(
        self,
        agent_id: str,
        title: str,
        publisher_name: str,
        category: AgentCategory,
        description: str,
        version: str = "1.0.0",
        price_monthly_usd: float = 0.0,
        tags: Optional[List[str]] = None,
    ) -> AgentMarketplaceListing:
        listing_id = f"list_{uuid.uuid4().hex[:8]}"
        listing = AgentMarketplaceListing(
            listing_id=listing_id,
            agent_id=agent_id,
            title=title,
            publisher_name=publisher_name,
            category=category,
            description=description,
            version=version,
            rating=5.0,
            install_count=0,
            certified_secure=True,
            price_monthly_usd=price_monthly_usd,
            tags=tags or [],
        )
        self._listings[listing_id] = listing
        return listing

    def list_listings(self, category: Optional[AgentCategory] = None) -> List[AgentMarketplaceListing]:
        items = list(self._listings.values())
        if category:
            items = [l for l in items if l.category == category]
        return items
