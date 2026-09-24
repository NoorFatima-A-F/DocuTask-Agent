"""
Platform Module Loader.
Discovers and instantiates platform modules with dependency verification.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional, Type
from .models import ModuleRecord, ModuleState
from ..kernel.metadata import ModuleMetadata
from ..kernel.exceptions import ModuleLoadException
from ..kernel.versioning import SemanticVersion


class ModuleLoader:
    """Discovers, validates, and instantiates platform modules."""

    @staticmethod
    def validate_module_metadata(metadata: ModuleMetadata) -> None:
        """Validate required metadata attributes."""
        if not metadata.name or not metadata.name.strip():
            raise ModuleLoadException("Module metadata missing required 'name'")
        if not isinstance(metadata.version, SemanticVersion):
            raise ModuleLoadException("Module metadata version must be SemanticVersion")

    @staticmethod
    def create_record(module_cls: Type[Any], configuration: Optional[Dict[str, Any]] = None) -> ModuleRecord:
        """Create a ModuleRecord from a module class or instance."""
        instance = module_cls() if isinstance(module_cls, type) else module_cls

        if hasattr(instance, "metadata") and isinstance(instance.metadata, ModuleMetadata):
            meta = instance.metadata
        else:
            name = getattr(instance, "module_name", type(instance).__name__)
            meta = ModuleMetadata(name=name, version=SemanticVersion(1, 0, 0))

        ModuleLoader.validate_module_metadata(meta)

        return ModuleRecord(
            name=meta.name,
            version=meta.version,
            metadata=meta,
            state=ModuleState.VALIDATED,
            instance=instance,
            loaded_at=datetime.now(timezone.utc),
            configuration=configuration or {},
        )
