"""
FastAPI REST Gateway for Enterprise Verification Extension Framework & Plugins.
Part 1.1F of the Enterprise Verification Platform.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.platform_verification.extension_framework.domain.models import (
    PluginMetadata, PluginExecutionResult, PluginHealthMetrics,
    PluginLifecycleState, PluginHealthState
)
from app.platform_verification.extension_framework.runtime.extension_framework_runtime import (
    ExtensionFrameworkRuntime, extension_framework_runtime
)

router = APIRouter(tags=["Enterprise Verification Extension Framework & Plugins"])

def get_framework_runtime() -> ExtensionFrameworkRuntime:
    return extension_framework_runtime


class PluginTransitionRequest(BaseModel):
    target_state: PluginLifecycleState
    reason: str = "Admin requested transition"


class PluginExecuteRequest(BaseModel):
    verification_id: str
    dataset_reference: Optional[Dict[str, Any]] = None
    caller_identity: str = "EnterpriseVerificationRunner"


class PluginScaffoldRequest(BaseModel):
    plugin_name: str
    plugin_id: str
    author: str = "Enterprise Verification Squad"
    capabilities: List[str]


# 1. Plugin Inventory & Capabilities
@router.get("", response_model=List[PluginMetadata])
def list_plugins(
    capability: Optional[str] = None,
    runtime: ExtensionFrameworkRuntime = Depends(get_framework_runtime)
):
    return runtime.registry.list_plugins(capability=capability)


@router.get("/capabilities", response_model=List[str])
def list_capabilities(
    runtime: ExtensionFrameworkRuntime = Depends(get_framework_runtime)
):
    return runtime.registry.list_all_capabilities()


@router.get("/{plugin_id}", response_model=PluginMetadata)
def get_plugin_metadata(
    plugin_id: str,
    runtime: ExtensionFrameworkRuntime = Depends(get_framework_runtime)
):
    plugin = runtime.registry.get_plugin(plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_id}' not found.")
    return plugin.metadata


# 2. Lifecycle State & Audit Trail
@router.get("/{plugin_id}/lifecycle")
def get_plugin_lifecycle(
    plugin_id: str,
    runtime: ExtensionFrameworkRuntime = Depends(get_framework_runtime)
):
    state = runtime.lifecycle.get_state(plugin_id)
    audit = runtime.lifecycle.get_audit_trail(plugin_id)
    return {
        "plugin_id": plugin_id,
        "current_state": state,
        "audit_trail": audit
    }


@router.post("/{plugin_id}/lifecycle/transition")
def transition_plugin_lifecycle(
    plugin_id: str,
    request: PluginTransitionRequest,
    runtime: ExtensionFrameworkRuntime = Depends(get_framework_runtime)
):
    try:
        new_state = runtime.lifecycle.transition_state(
            plugin_id=plugin_id,
            target_state=request.target_state,
            reason=request.reason
        )
        return {"plugin_id": plugin_id, "new_state": new_state}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 3. Health & Telemetry
@router.get("/{plugin_id}/health", response_model=PluginHealthMetrics)
def get_plugin_health(
    plugin_id: str,
    runtime: ExtensionFrameworkRuntime = Depends(get_framework_runtime)
):
    return runtime.health.get_health(plugin_id)


@router.get("/health/all", response_model=List[PluginHealthMetrics])
def list_all_plugin_health(
    runtime: ExtensionFrameworkRuntime = Depends(get_framework_runtime)
):
    return runtime.health.list_all_health()


# 4. Sandboxed Execution
@router.post("/{plugin_id}/execute", response_model=PluginExecutionResult)
def execute_plugin(
    plugin_id: str,
    request: PluginExecuteRequest,
    runtime: ExtensionFrameworkRuntime = Depends(get_framework_runtime)
):
    try:
        return runtime.execute_verification_plugin(
            plugin_id=plugin_id,
            verification_id=request.verification_id,
            dataset_ref=request.dataset_reference,
            caller_identity=request.caller_identity
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# 5. Developer Tooling: Scaffolding & Docs
@router.post("/scaffold")
def scaffold_plugin(
    request: PluginScaffoldRequest,
    runtime: ExtensionFrameworkRuntime = Depends(get_framework_runtime)
):
    return runtime.scaffolder.generate_plugin_scaffold(
        plugin_name=request.plugin_name,
        plugin_id=request.plugin_id,
        author=request.author,
        capabilities=request.capabilities
    )


@router.get("/{plugin_id}/docs")
def get_plugin_documentation(
    plugin_id: str,
    runtime: ExtensionFrameworkRuntime = Depends(get_framework_runtime)
):
    plugin = runtime.registry.get_plugin(plugin_id)
    if not plugin:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_id}' not found.")
    doc = runtime.docs.generate_markdown(plugin)
    return {"plugin_id": plugin_id, "documentation_markdown": doc}
