"""
Phase 13.19: White-Labeling & Tenant Custom Branding Service.
Manages custom domains (CNAME), logos, color palettes, and email footers.
"""

from typing import Dict, List, Optional, Any
from app.platform_saas.models.schemas import BrandingConfig


class WhiteLabelService:
    def __init__(self):
        self._brandings: Dict[str, BrandingConfig] = {}
        self._seed_default_branding()

    def _seed_default_branding(self) -> None:
        b1 = BrandingConfig(
            tenant_id="tenant_acme_corp",
            custom_cname_domain="ai.acmecorp.com",
            brand_name="Acme Enterprise AI Studio",
            logo_url="https://assets.acmecorp.com/brand/logo-dark.svg",
            primary_color_hex="#3b82f6",
            secondary_color_hex="#10b981",
            support_email="ai-support@acmecorp.com",
            email_footer_text="Acme Corp AI - Confidential Enterprise System",
        )
        b2 = BrandingConfig(
            tenant_id="tenant_globex_health",
            custom_cname_domain="clinical-ai.globexhealth.com",
            brand_name="Globex Clinical Intelligence Platform",
            logo_url="https://globexhealth.com/static/brand/globex-shield.png",
            primary_color_hex="#0ea5e9",
            secondary_color_hex="#8b5cf6",
            support_email="hipaa-help@globexhealth.com",
            email_footer_text="Globex Healthcare Systems - HIPAA Certified AI Portal",
        )
        self._brandings[b1.tenant_id] = b1
        self._brandings[b2.tenant_id] = b2

    def configure_branding(
        self,
        tenant_id: str,
        brand_name: str,
        logo_url: str,
        primary_color_hex: str = "#4f46e5",
        secondary_color_hex: str = "#06b6d4",
        support_email: str = "support@example.com",
        custom_cname_domain: Optional[str] = None,
        email_footer_text: str = "Powered by Enterprise AI Platform",
    ) -> BrandingConfig:
        config = BrandingConfig(
            tenant_id=tenant_id,
            custom_cname_domain=custom_cname_domain,
            brand_name=brand_name,
            logo_url=logo_url,
            primary_color_hex=primary_color_hex,
            secondary_color_hex=secondary_color_hex,
            support_email=support_email,
            email_footer_text=email_footer_text,
        )
        self._brandings[tenant_id] = config
        return config

    def get_branding(self, tenant_id: str) -> BrandingConfig:
        return self._brandings.get(
            tenant_id,
            BrandingConfig(
                tenant_id=tenant_id,
                brand_name="Enterprise AI Platform",
                logo_url="/logo.png",
                support_email="support@aiplatform.internal",
            ),
        )

    def list_brandings(self) -> List[BrandingConfig]:
        return list(self._brandings.values())
