"""Tests for Infrastructure SDK Client, Decorators, and REST API Routes."""

from app.infrastructure.api.routes import (
    deploy_service,
    list_resources,
    provision_resource,
    restart_runtime,
)
from app.infrastructure.api.schemas import (
    ResourceProvisionRequest,
    RuntimeActionRequest,
    RuntimeDeployRequest,
)
from app.infrastructure.core.resources import ResourceCategory
from app.infrastructure.sdk.client import InfrastructureSDK
from app.infrastructure.sdk.decorators import infrastructure_managed, with_resource_budget


def test_infrastructure_sdk_operations():
    sdk = InfrastructureSDK()

    # Deploy
    inst = sdk.deploy_service(name="knowledge-worker", replicas=2, environment="TESTING")
    assert inst.service_name == "knowledge-worker"
    assert inst.state.value == "RUNNING"

    # Provision resource
    res = sdk.provision_resource(
        name="vector-db",
        category=ResourceCategory.STORAGE,
        resource_type="DATABASE",
        environment="TESTING",
    )
    assert res.name == "vector-db"
    assert res.state.value == "ACTIVE"

    # Health check
    health = sdk.check_health("svc_knowledge-worker_testing")
    assert health.service_id == "svc_knowledge-worker_testing"

    # Restart service
    restarted = sdk.restart_service(inst.instance_id)
    assert restarted.state.value == "RUNNING"


def test_infrastructure_decorators():
    @infrastructure_managed("sample-service", "PRODUCTION")
    @with_resource_budget(cpu_limit=2.0, memory_limit_mb=2048)
    def run_workload():
        return "workload_complete"

    assert run_workload() == "workload_complete"
    assert run_workload.__infra_managed__ is True
    assert run_workload.__service_name__ == "sample-service"
    assert run_workload.__cpu_limit__ == 2.0


def test_infrastructure_api_routes():
    # Deploy route
    deploy_req = RuntimeDeployRequest(service="api-gateway", replicas=2, environment="DEVELOPMENT")
    inst_resp = deploy_service(deploy_req)
    assert inst_resp.service_name == "api-gateway"
    assert inst_resp.state == "RUNNING"

    # Provision resource route
    prov_req = ResourceProvisionRequest(
        name="redis-cache",
        category="STORAGE",
        resource_type="CACHE",
        environment="DEVELOPMENT",
    )
    res_resp = provision_resource(prov_req)
    assert res_resp.name == "redis-cache"

    # List resources route
    resources = list_resources("DEVELOPMENT")
    assert len(resources) >= 1

    # Restart route
    restart_resp = restart_runtime(RuntimeActionRequest(instance_id=inst_resp.instance_id))
    assert restart_resp.state == "RUNNING"
