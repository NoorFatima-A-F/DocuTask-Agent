"""Marketplace Package Interface."""

from __future__ import annotations

from app.platform.marketplace.marketplace_service import (
    MarketplacePackage,
    MarketplaceService,
    global_marketplace_service,
)

__all__ = ["MarketplacePackage", "MarketplaceService", "global_marketplace_service"]
