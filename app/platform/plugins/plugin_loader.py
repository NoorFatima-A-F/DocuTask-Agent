"""Plugin Execution Context and Dynamic Loader."""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from app.platform.capability.capability_model import CapabilityProvider
from app.platform.capability.capability_registry import (
    CapabilityRegistry,
    global_capability_registry,
)
from app.platform.di.container import DIContainer, global_di_container
from app.platform.plugins.plugin_manifest import PluginManifest


class PluginContext:
    def __init__(
        self,
        manifest: PluginManifest,
        di_container: DIContainer,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.manifest = manifest
        self.di = di_container.create_child_scope()
        self.config = {**manifest.default_config, **(config or {})}
        self.installed_at = time.time()
        self.is_enabled = True

    def get_service(self, service_key: str) -> Any:
        return self.di.resolve(service_key)


class PluginLoader:
    def __init__(
        self,
        plugins_directory: str = "plugins",
        registry: Optional[CapabilityRegistry] = None,
        di_container: Optional[DIContainer] = None,
    ):
        self.plugins_dir = plugins_directory
        self.registry = registry or global_capability_registry
        self.di = di_container or global_di_container
        self._loaded_plugins: Dict[str, PluginContext] = {}

    def discover_and_load_all(self) -> List[PluginManifest]:
        manifests: List[PluginManifest] = []
        # Predefined built-in plugin blueprints
        builtin_plugins = [
            {
                "plugin_id": "plugin.invoice.processing",
                "name": "Enterprise Invoice & Billing Agent",
                "version": "1.4.0",
                "author": "DocuTask Core Team",
                "description": "Extracts vendor, subtotal, tax, and line items with strict Mod11 VAT reconciliation.",
                "entry_point": "plugins.invoice.main",
                "capabilities_provided": ["perception.ocr", "extraction.invoice", "validation.reconciliation"],
                "capabilities_required": [],
                "permission_scopes": ["ocr:read", "storage:write", "evidence:seal"],
                "default_config": {"tolerance_usd": 0.01, "mod11_strict": True},
            },
            {
                "plugin_id": "plugin.resume.screener",
                "name": "HR Resume & ATS Evaluation Agent",
                "version": "1.2.0",
                "author": "TalentAI Labs",
                "description": "Parses candidate experience, skills taxonomy, and scores job description alignment.",
                "entry_point": "plugins.resume.main",
                "capabilities_provided": ["extraction.resume", "scoring.ats_match"],
                "capabilities_required": ["perception.ocr"],
                "permission_scopes": ["ocr:read", "storage:write"],
                "default_config": {"scoring_threshold": 0.85},
            },
            {
                "plugin_id": "plugin.medical.records",
                "name": "Clinical Health Record & HIPAA Agent",
                "version": "2.0.1",
                "author": "MedSecure Systems",
                "description": "De-identifies PHI and extracts ICD-10 diagnostic codes under strict HIPAA policies.",
                "entry_point": "plugins.medical.main",
                "capabilities_provided": ["privacy.deidentify", "extraction.clinical"],
                "capabilities_required": [],
                "permission_scopes": ["ocr:read", "phi:anonymize", "evidence:seal"],
                "default_config": {"phi_redaction_level": "strict"},
            },
            {
                "plugin_id": "plugin.legal.contracts",
                "name": "Commercial Contract & Clause Reviewer",
                "version": "1.1.5",
                "author": "LexisCorp AI",
                "description": "Scans indemnification limits, termination clauses, and non-compete covenants.",
                "entry_point": "plugins.contracts.main",
                "capabilities_provided": ["extraction.contract", "analysis.risk"],
                "capabilities_required": ["perception.ocr"],
                "permission_scopes": ["ocr:read", "storage:write"],
                "default_config": {"indemnity_cap_alert_usd": 1000000},
            },
        ]

        for p_data in builtin_plugins:
            manifest = PluginManifest.from_dict(p_data)
            self.load_plugin(manifest)
            manifests.append(manifest)

        return manifests

    def load_plugin(self, manifest: PluginManifest, config: Optional[Dict[str, Any]] = None) -> PluginContext:
        ctx = PluginContext(manifest=manifest, di_container=self.di, config=config)
        self._loaded_plugins[manifest.plugin_id] = ctx

        # Register provided capabilities into registry
        for cap_name in manifest.capabilities_provided:
            provider = CapabilityProvider(
                provider_id=f"{manifest.plugin_id}::{cap_name}",
                plugin_id=manifest.plugin_id,
                implementation_name=manifest.name,
                priority=100,
                cost_per_unit_usd=0.001,
                p95_latency_ms=250.0,
                quality_score=0.98,
            )
            self.registry.register_provider(cap_name, provider)

        return ctx

    def get_plugin(self, plugin_id: str) -> Optional[PluginContext]:
        return self._loaded_plugins.get(plugin_id)

    def list_plugins(self) -> List[PluginContext]:
        return list(self._loaded_plugins.values())

    def unload_plugin(self, plugin_id: str) -> bool:
        if plugin_id in self._loaded_plugins:
            ctx = self._loaded_plugins[plugin_id]
            for cap_name in ctx.manifest.capabilities_provided:
                self.registry.unregister_provider(cap_name, f"{plugin_id}::{cap_name}")
            del self._loaded_plugins[plugin_id]
            return True
        return False


global_plugin_loader = PluginLoader()
global_plugin_loader.discover_and_load_all()
