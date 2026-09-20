"""
Enterprise Plugin Marketplace & Digital Certification Manager.
"""
from datetime import datetime, timezone
import hashlib
from typing import Dict, List, Optional
from app.platform_verification.extension_framework.domain.models import (
    PluginMarketplaceEntry, PluginCategory, SecurityClassification
)


class PluginMarketplaceManager:
    def __init__(self):
        self._entries: Dict[str, PluginMarketplaceEntry] = {}

    def publish_plugin(
        self,
        plugin_id: str,
        version: str,
        category: PluginCategory,
        author: str,
        certification_level: SecurityClassification = SecurityClassification.COMMUNITY
    ) -> PluginMarketplaceEntry:
        # Generate signature
        sig = hashlib.sha256(f"{plugin_id}:{version}:{author}:{certification_level.value}".encode("utf-8")).hexdigest()
        entry = PluginMarketplaceEntry(
            plugin_id=plugin_id,
            version=version,
            category=category,
            author=author,
            certification_level=certification_level,
            digital_signature=sig,
            is_published=True
        )
        self._entries[plugin_id] = entry
        return entry

    def get_entry(self, plugin_id: str) -> Optional[PluginMarketplaceEntry]:
        return self._entries.get(plugin_id)

    def list_entries(self, category: Optional[PluginCategory] = None) -> List[PluginMarketplaceEntry]:
        entries = list(self._entries.values())
        if category:
            entries = [e for e in entries if e.category == category]
        return entries

    def verify_signature(self, plugin_id: str) -> bool:
        entry = self.get_entry(plugin_id)
        if not entry:
            return False
        expected_sig = hashlib.sha256(f"{entry.plugin_id}:{entry.version}:{entry.author}:{entry.certification_level.value}".encode("utf-8")).hexdigest()
        return entry.digital_signature == expected_sig


plugin_marketplace = PluginMarketplaceManager()
