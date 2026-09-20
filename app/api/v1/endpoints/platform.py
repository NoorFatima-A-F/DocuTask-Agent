"""Platform OS, Extensibility & Ecosystem Endpoints (Phase 9 AAPEROS).

Exposes REST endpoints for the SDK, dynamic capability registry, plugin runtime,
visual workflows, DSL compilation, marketplace, organization templates, policies,
sandboxing, and automatic contract generation.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.platform.capability.capability_registry import global_capability_registry
from app.platform.certification.certification_pipeline import global_certification_pipeline
from app.platform.composition.composition_engine import global_composition_engine
from app.platform.contracts.contract_generator import ContractGenerator
from app.platform.dsl.dsl_parser import DSLCompiler, DSLParser
from app.platform.lifecycle.lifecycle_manager import global_lifecycle_manager
from app.platform.marketplace.marketplace_service import global_marketplace_service
from app.platform.plugins.plugin_loader import global_plugin_loader
from app.platform.plugins.plugin_runtime import global_plugin_runtime
from app.platform.policy.policy_engine import global_policy_engine
from app.platform.sandbox.sandbox_runtime import global_sandbox_runtime
from app.platform.templates.template_engine import global_template_engine
from app.platform.tools.dynamic_tool_registry import (
    ToolInvoker,
    ToolMetadata,
    global_tool_registry,
)
from app.platform.workflow.workflow_engine import (
    WorkflowDefinition,
    WorkflowEdge,
    WorkflowNode,
    global_workflow_engine,
)

router = APIRouter()


# Request / Response Pydantic Models
class ExecutePluginRequest(BaseModel):
    plugin_id: str
    capability: str
    input_payload: Dict[str, Any] = Field(default_factory=dict)


class CompileDSLRequest(BaseModel):
    dsl_content: Dict[str, Any]


class RegisterToolRequest(BaseModel):
    tool_id: str
    name: str
    category: str
    description: str
    capabilities: List[str] = Field(default_factory=list)
    required_permissions: List[str] = Field(default_factory=list)
    cost_per_call_usd: float = 0.0001
    p95_latency_ms: float = 100.0


class ValidatePolicyRequest(BaseModel):
    action_context: Dict[str, Any]


class ComposePipelineRequest(BaseModel):
    pipeline_id: str
    name: str
    description: str
    steps: List[Dict[str, Any]]


# Endpoints

@router.get("/sdk", summary="List SDK interfaces, base classes, and extension points")
def get_sdk_manifest() -> Dict[str, Any]:
    return {
        "sdk_version": "2026.1.0",
        "supported_base_classes": [
            "BaseAgent",
            "BasePlanner",
            "BaseWorker",
            "BaseTool",
            "BaseMemoryStore",
            "BasePolicyRule",
            "BaseWorkflow",
            "BaseValidator",
            "BaseReflectionCritic",
            "BaseBenchmarkSuite",
        ],
        "lifecycle_states": ["UNINITIALIZED", "INITIALIZING", "IDLE", "EXECUTING", "PAUSED", "COMPLETED", "FAILED"],
        "extension_points": ["capability_provider", "tool_integration", "policy_evaluator", "workflow_step"],
    }


@router.get("/plugins", summary="List loaded dynamic plugins")
def list_plugins() -> List[Dict[str, Any]]:
    plugins = global_plugin_loader.list_plugins()
    return [
        {
            **ctx.manifest.to_dict(),
            "is_enabled": ctx.is_enabled,
            "installed_at": ctx.installed_at,
        }
        for ctx in plugins
    ]


@router.post("/plugins/{plugin_id}/toggle", summary="Enable or disable plugin")
def toggle_plugin(plugin_id: str, enable: bool = True) -> Dict[str, Any]:
    if enable:
        success = global_lifecycle_manager.enable_plugin(plugin_id)
    else:
        success = global_lifecycle_manager.disable_plugin(plugin_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_id}' not found")
    return {"status": "SUCCESS", "plugin_id": plugin_id, "is_enabled": enable}


@router.post("/plugins/{plugin_id}/rollback", summary="Rollback plugin to previous version")
def rollback_plugin(plugin_id: str) -> Dict[str, Any]:
    ctx = global_lifecycle_manager.rollback_plugin(plugin_id)
    if not ctx:
        raise HTTPException(status_code=400, detail=f"No previous version available for '{plugin_id}'")
    return {"status": "ROLLED_BACK", "plugin_id": plugin_id, "active_version": ctx.manifest.version}


@router.post("/execute", summary="Execute plugin capability")
def execute_plugin(req: ExecutePluginRequest) -> Dict[str, Any]:
    try:
        res = global_plugin_runtime.execute_plugin_capability(
            plugin_id=req.plugin_id,
            capability=req.capability,
            input_payload=req.input_payload,
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/capabilities", summary="List registered dynamic capabilities")
def list_capabilities() -> List[Dict[str, Any]]:
    caps = global_capability_registry.list_capabilities()
    return [c.to_dict() for c in caps]


@router.get("/tools", summary="List dynamic external tools")
def list_tools() -> List[Dict[str, Any]]:
    tools = global_tool_registry.list_tools()
    return [t.to_dict() for t in tools]


@router.post("/tools/register", summary="Register new tool integration")
def register_tool(req: RegisterToolRequest) -> Dict[str, Any]:
    tool = ToolMetadata(
        tool_id=req.tool_id,
        name=req.name,
        category=req.category,
        description=req.description,
        capabilities=req.capabilities,
        required_permissions=req.required_permissions,
        cost_per_call_usd=req.cost_per_call_usd,
        p95_latency_ms=req.p95_latency_ms,
    )
    global_tool_registry.register_tool(tool)
    return {"status": "REGISTERED", "tool_id": req.tool_id}


@router.post("/workflow/compile", summary="Compile Workflow DSL into executable DAG")
def compile_workflow_dsl(req: CompileDSLRequest) -> Dict[str, Any]:
    spec = DSLParser.parse_dict(req.dsl_content)
    wf = DSLCompiler.compile_to_workflow_definition(spec)
    global_workflow_engine.register_workflow(wf)
    return wf.to_dict()


@router.post("/workflow/execute/{workflow_id}", summary="Execute registered workflow")
def execute_workflow(workflow_id: str, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
    wf = global_workflow_engine.get_workflow(workflow_id)
    if not wf:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")
    res = global_workflow_engine.execute_workflow(wf, inputs or {})
    return res


@router.get("/marketplace", summary="List Agent Marketplace catalog")
def list_marketplace() -> List[Dict[str, Any]]:
    pkgs = global_marketplace_service.list_packages()
    return [p.to_dict() for p in pkgs]


@router.post("/marketplace/install/{package_id}", summary="1-Click install package from marketplace")
def install_marketplace_package(package_id: str) -> Dict[str, Any]:
    try:
        return global_marketplace_service.install_package(package_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/templates", summary="List Industry Organization Templates")
def list_templates() -> List[Dict[str, Any]]:
    tpls = global_template_engine.list_templates()
    return [t.to_dict() for t in tpls]


@router.post("/templates/deploy/{template_id}", summary="Deploy complete organization blueprint")
def deploy_template(template_id: str) -> Dict[str, Any]:
    try:
        return global_template_engine.deploy_template(template_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/compose", summary="Compose multi-agent pipeline")
def compose_pipeline(req: ComposePipelineRequest) -> Dict[str, Any]:
    pipe = global_composition_engine.create_pipeline(
        pipeline_id=req.pipeline_id,
        name=req.name,
        description=req.description,
        steps_data=req.steps,
    )
    return pipe.to_dict()


@router.get("/policies", summary="List enterprise governance policies")
def list_policies() -> List[Dict[str, Any]]:
    policies = global_policy_engine.list_policies()
    return [p.to_dict() for p in policies]


@router.post("/policies/validate", summary="Validate action against enterprise policies")
def validate_policy(req: ValidatePolicyRequest) -> Dict[str, Any]:
    res = global_policy_engine.evaluate_action(req.action_context)
    return res.to_dict()


@router.post("/certify/{plugin_id}", summary="Run automated 6-point plugin certification")
def certify_plugin(plugin_id: str) -> Dict[str, Any]:
    badge = global_certification_pipeline.certify_plugin(plugin_id)
    return badge.to_dict()


@router.get("/contracts", summary="Auto-generate OpenAPI and JSON schemas")
def get_contracts() -> Dict[str, Any]:
    dossier = ContractGenerator.generate_all()
    return dossier.to_dict()


@router.get("/sandbox/status", summary="Inspect sandbox resource quotas and isolation")
def get_sandbox_status() -> Dict[str, Any]:
    return global_sandbox_runtime.get_status()


@router.get("/diagnostics", summary="Platform OS runtime kernel diagnostics")
def get_platform_diagnostics() -> Dict[str, Any]:
    return {
        "status": "OPERATIONAL",
        "kernel_version": "AAPEROS-2026.1",
        "active_plugins": len(global_plugin_loader.list_plugins()),
        "registered_capabilities": len(global_capability_registry.list_capabilities()),
        "registered_tools": len(global_tool_registry.list_tools()),
        "active_policies": len(global_policy_engine.list_policies()),
        "sandbox_violations": len(global_sandbox_runtime.get_violations()),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
