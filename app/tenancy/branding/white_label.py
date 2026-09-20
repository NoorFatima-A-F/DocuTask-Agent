"""White-Label Customization Engine (ESP-MOOS).

Manages organization branding, logos, color schemes, typography, and portal styling.
"""

from __future__ import annotations

import uuid
from typing import Dict, Optional
from app.tenancy.core.models import BrandingProfile


class WhiteLabelEngine:
    """Manages white-label branding profiles for tenant organizations."""

    def __init__(self):
        self._profiles: Dict[str, BrandingProfile] = {}

    def set_branding(
        self,
        organization_id: str,
        logo_url: str = "",
        favicon_url: str = "",
        primary_color: str = "#0052CC",
        secondary_color: str = "#172B4D",
        font_family: str = "Inter, sans-serif",
        custom_login_title: str = "DocuTask Enterprise",
        email_footer_text: str = "",
        css_overrides: str = "",
    ) -> BrandingProfile:
        """Create or update white-label branding profile."""
        profile = BrandingProfile(
            branding_id=f"brand_{uuid.uuid4().hex[:8]}",
            organization_id=organization_id,
            logo_url=logo_url,
            favicon_url=favicon_url,
            primary_color=primary_color,
            secondary_color=secondary_color,
            font_family=font_family,
            custom_login_title=custom_login_title,
            email_footer_text=email_footer_text,
            css_overrides=css_overrides,
        )
        self._profiles[organization_id] = profile
        return profile

    def get_branding(self, organization_id: str) -> BrandingProfile:
        """Retrieve organization branding or default profile."""
        return self._profiles.get(
            organization_id,
            BrandingProfile(
                branding_id="brand_default",
                organization_id=organization_id,
                primary_color="#0052CC",
            ),
        )
