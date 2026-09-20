"""
Layer Classification Mapping for DocuTask Agent codebase.
"""
from __future__ import annotations
from app.platform_verification.clean_architecture.domain.models import ArchitectureLayer


def classify_module_layer(module_name: str) -> ArchitectureLayer:
    """Maps a Python module name to its Clean Architecture layer."""
    mod = module_name.lower().replace("\\", ".").replace("/", ".")

    if "domain" in mod or "entities" in mod or "value_objects" in mod or "events" in mod:
        return ArchitectureLayer.DOMAIN
    elif "application" in mod or "use_cases" in mod or "workflows" in mod:
        return ArchitectureLayer.APPLICATION
    elif "interfaces" in mod or "contracts" in mod or "ports" in mod:
        return ArchitectureLayer.INTERFACES
    elif "infrastructure" in mod or "database" in mod or "repositories" in mod or "clients" in mod:
        return ArchitectureLayer.INFRASTRUCTURE
    elif "api" in mod or "endpoints" in mod or "routers" in mod or "controllers" in mod:
        return ArchitectureLayer.API
    elif "agents" in mod or "planner" in mod or "tools" in mod:
        return ArchitectureLayer.AGENTS
    elif "runtime" in mod or "orchestrator" in mod:
        return ArchitectureLayer.RUNTIME
    elif "workers" in mod or "tasks" in mod:
        return ArchitectureLayer.WORKERS
    elif "knowledge" in mod or "rag" in mod or "embeddings" in mod:
        return ArchitectureLayer.KNOWLEDGE
    elif "security" in mod or "auth" in mod or "rbac" in mod:
        return ArchitectureLayer.SECURITY
    elif "observability" in mod or "telemetry" in mod or "logging" in mod:
        return ArchitectureLayer.OBSERVABILITY
    else:
        return ArchitectureLayer.UNKNOWN
