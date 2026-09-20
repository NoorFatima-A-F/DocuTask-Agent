"""
Domain models for Module Boundary & Plugin Architecture Verification (PART 2D).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union


class ModuleType(str, Enum):
    PLATFORM_CORE = "PLATFORM_CORE"
    RUNTIME_ENGINE = "RUNTIME_ENGINE"
    SUBSYSTEM_MODULE = "SUBSYSTEM_MODULE"
    EXTENSION_PLUGIN = "EXTENSION_PLUGIN"
    AGENT_PLUGIN = "AGENT_PLUGIN"
    CONNECTOR = "CONNECTOR"


class PluginLifecycleState(str, Enum):
    UNLOADED = "UNLOADED"
    INITIALIZING = "INITIALIZING"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"
    STOPPING = "STOPPING"
    SHUTDOWN = "SHUTDOWN"
    FAILED = "FAILED"


class BoundaryViolationSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class ModularityCertificationBand(str, Enum):
    ENTERPRISE_PLATFORM_MODULAR = "ENTERPRISE_PLATFORM_MODULAR"  # 95-100
    PRODUCTION_MODULAR = "PRODUCTION_MODULAR"                    # 90-94
    ACCEPTABLE_MODULARITY = "ACCEPTABLE_MODULARITY"              # 80-89
    MONOLITHIC_COUPLING_RISK = "MONOLITHIC_COUPLING_RISK"        # 70-79
    FAILED = "FAILED"                                            # < 70


@dataclass
class ModuleManifest:
    """Explicit declaration of module identity, boundaries, and ownership."""
    module_name: str
    version: str
    module_type: ModuleType
    owner: str
    architecture_domain: str
    allowed_dependencies: List[str] = field(default_factory=list)
    forbidden_dependencies: List[str] = field(default_factory=list)
    exported_contracts: List[str] = field(default_factory=list)
    owned_responsibilities: List[str] = field(default_factory=list)
    isolation_enabled: bool = True
    criticality: str = "HIGH"
    core_version_required: str = ">=2.0.0"


@dataclass
class ModuleDependencyEdge:
    """Directed dependency between two modules."""
    source_module: str
    target_module: str
    is_allowed: bool = True
    violation_reason: Optional[str] = None
    severity: BoundaryViolationSeverity = BoundaryViolationSeverity.LOW


@dataclass
class ModuleBoundaryViolation:
    """Detected boundary violation between modules or from plugin to core."""
    violation_id: str
    source_module: str
    target_module: str
    source_file: str
    line_number: int
    severity: BoundaryViolationSeverity
    message: str
    remediation: str


@dataclass
class PluginContractReport:
    """Verification result for a plugin's contract and lifecycle compliance."""
    plugin_id: str
    plugin_name: str
    version: str
    plugin_type: str  # "LLM_PROVIDER", "OCR_PROVIDER", "AGENT"
    satisfies_plugin_interface: bool
    implements_initialize: bool
    implements_execute: bool
    implements_health: bool
    implements_shutdown: bool
    is_isolated: bool
    is_compatible_with_core: bool
    passed: bool
    errors: List[str] = field(default_factory=list)


@dataclass
class ModuleQualityMetrics:
    """Modularity quality indices for a module."""
    module_name: str
    coupling_score: float      # Lower is better (0 to 100)
    cohesion_score: float      # Higher is better (0 to 100)
    independence_score: float  # Higher is better (0 to 100)
    extension_score: float     # Higher is better (0 to 100)
    composite_modularity_index: float  # 0 to 100
    risk_level: str = "LOW"


@dataclass
class ModuleArchitectureEvidencePackage:
    """Comprehensive sealed evidence package for module boundary verification."""
    scan_id: str
    repository_name: str = "DocuTask-Agent"
    commit_sha: str = "HEAD"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    registered_modules_count: int = 0
    registered_plugins_count: int = 0
    boundary_violations: List[ModuleBoundaryViolation] = field(default_factory=list)
    plugin_reports: List[PluginContractReport] = field(default_factory=list)
    module_metrics: Dict[str, ModuleQualityMetrics] = field(default_factory=dict)
    total_modularity_score: float = 0.0
    certification_band: ModularityCertificationBand = ModularityCertificationBand.ENTERPRISE_PLATFORM_MODULAR
    is_certified: bool = True
    evidence_sha256: str = ""

    def compute_sha256(self) -> str:
        payload = f"{self.scan_id}:{self.timestamp}:{self.total_modularity_score}:{len(self.boundary_violations)}:{len(self.plugin_reports)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
