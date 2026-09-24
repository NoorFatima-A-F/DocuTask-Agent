"""
CLI Code Generator for New Verification Modules and Plugins.
Enforces Clean Architecture and SOLID principles automatically.
"""
import sys

TEMPLATE_MODELS = """\"\""
Domain Models for {name}.
\"\""
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

class {pascal}Entity(BaseModel):
    id: str = Field(default_factory=lambda: f"{prefix}_{uuid.uuid4().hex[:8]}")
    name: str = "{pascal} Default"
    tenant_id: str = "default-tenant"
    status: str = "ACTIVE"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
"""

TEMPLATE_INTERFACES = """\"\""
Domain Interfaces for {name}.
\"\""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.{name}.domain.models import {pascal}Entity

class {pascal}RepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: {pascal}Entity) -> {pascal}Entity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[{pascal}Entity]:
        pass
"""

TEMPLATE_USE_CASES = """\"\""
Application Use Cases for {name}.
\"\""
from typing import Optional
from app.platform_verification.modules.{name}.domain.models import {pascal}Entity
from app.platform_verification.modules.{name}.domain.interfaces import {pascal}RepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class Manage{pascal}UseCase:
    def __init__(self, repository: {pascal}RepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant") -> Result[{pascal}Entity, str]:
        try:
            entity = {pascal}Entity(name=name, tenant_id=tenant_id)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))
"""

def scaffold_module(name: str):
    import re
    from pathlib import Path
    sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())
    prefix = sanitized_name[:4].lower()
    pascal = "".join(w.capitalize() for w in sanitized_name.split("_"))
    root = Path("app/platform_verification/modules").resolve()
    base = (root / sanitized_name).resolve()
    if not (base == root or base.is_relative_to(root)):
        raise ValueError(f"Invalid module name: '{name}'")
    
    dirs = ["domain", "application", "infrastructure", "interfaces"]
    for d in dirs:
        sub_dir = (base / d).resolve()
        sub_dir.mkdir(parents=True, exist_ok=True)
        init_file = sub_dir / "__init__.py"
        with open(init_file, "w", encoding="utf-8") as f:
            f.write('"""Module layer."""\n')

    with open(base / "domain" / "models.py", "w", encoding="utf-8") as f:
        f.write(TEMPLATE_MODELS.format(name=sanitized_name, pascal=pascal, prefix=prefix))

    with open(base / "domain" / "interfaces.py", "w", encoding="utf-8") as f:
        f.write(TEMPLATE_INTERFACES.format(name=sanitized_name, pascal=pascal))

    with open(base / "application" / "use_cases.py", "w", encoding="utf-8") as f:
        f.write(TEMPLATE_USE_CASES.format(name=sanitized_name, pascal=pascal))

    print(f"Scaffolded module '{sanitized_name}' at '{base}'.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        scaffold_module(sys.argv[1])
    else:
        print("Usage: python code_generator.py <module_name>")
