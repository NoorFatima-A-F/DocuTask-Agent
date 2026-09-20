"""
Dependency Inventory & Pinning Registry.
Tracks direct, transitive, system, and AI model dependencies.
"""
from typing import Dict, List, Optional
from app.platform_verification.config_versioning.domain.models import DependencyItem, DependencyCategory
from app.platform_verification.config_versioning.domain.interfaces import DependencyRegistryInterface

class DependencyRegistry(DependencyRegistryInterface):
    def __init__(self):
        self._dependencies: Dict[str, DependencyItem] = {}
        self._load_core_platform_dependencies()

    def _load_core_platform_dependencies(self):
        core_deps = [
            DependencyItem(name="fastapi", version="0.115.0", category=DependencyCategory.PYTHON_PACKAGE, license="MIT"),
            DependencyItem(name="pydantic", version="2.10.4", category=DependencyCategory.PYTHON_PACKAGE, license="MIT"),
            DependencyItem(name="sqlalchemy", version="2.0.36", category=DependencyCategory.PYTHON_PACKAGE, license="MIT"),
            DependencyItem(name="asyncpg", version="0.30.0", category=DependencyCategory.PYTHON_PACKAGE, license="Apache-2.0"),
            DependencyItem(name="redis", version="5.2.1", category=DependencyCategory.PYTHON_PACKAGE, license="MIT"),
            DependencyItem(name="google-genai", version="0.1.1", category=DependencyCategory.PYTHON_PACKAGE, license="Apache-2.0"),
            DependencyItem(name="gemini-2.5-flash", version="2026-03-stable", category=DependencyCategory.AI_MODEL, license="Proprietary Google"),
            DependencyItem(name="postgresql", version="16.3-alpine", category=DependencyCategory.DATABASE, license="PostgreSQL"),
            DependencyItem(name="redis-server", version="7.2.4-alpine", category=DependencyCategory.MESSAGE_BROKER, license="BSD-3-Clause"),
        ]
        for d in core_deps:
            self._dependencies[d.name] = d

    def register_dependency(self, item: DependencyItem) -> DependencyItem:
        self._dependencies[item.name] = item
        return item

    def list_dependencies(self) -> List[DependencyItem]:
        return list(self._dependencies.values())

    def get_all_dependencies(self) -> List[DependencyItem]:
        return self.list_dependencies()

    def get_dependency(self, name: str) -> Optional[DependencyItem]:
        return self._dependencies.get(name)

dependency_registry = DependencyRegistry()
