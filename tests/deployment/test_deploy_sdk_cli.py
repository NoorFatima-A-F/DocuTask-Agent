"""Unit tests for Infrastructure SDK and doctaskctl CLI."""
from app.deployment.cli.commands import run_cli
from app.deployment.core.deployment import DeploymentStrategyType
from app.deployment.sdk.client import InfrastructureSDK
from app.deployment.sdk.plugins import DeploymentPlugin


class AuditPluginSample(DeploymentPlugin):
    def __init__(self):
        self.pre_deploy_called = False
        self.post_deploy_called = False

    @property
    def name(self) -> str:
        return "test_audit"

    def pre_deploy(self, context):
        self.pre_deploy_called = True
        return True

    def post_deploy(self, context):
        self.post_deploy_called = True


def test_infrastructure_sdk_flow_with_plugin():
    plugin = AuditPluginSample()
    sdk = InfrastructureSDK()
    sdk.plugins.register(plugin)

    rel = sdk.create_release(
        version="3.0.0",
        name="Phase 9J SDK Release",
        commit_sha="abcdef999",
        artifact_ids=["art-1"],
    )

    dep = sdk.deploy(
        release_id=rel.release_id,
        target_environment="prod",
        strategy=DeploymentStrategyType.ROLLING,
    )

    assert dep.status.value == "ACTIVE"
    assert plugin.pre_deploy_called is True
    assert plugin.post_deploy_called is True


def test_doctaskctl_cli_execution():
    sdk = InfrastructureSDK()

    # 1. Release create via CLI
    rel_out = run_cli([
        "release", "create",
        "--version", "1.8.0",
        "--name", "CLI Release",
        "--commit", "cli12345",
        "--artifacts", "art-cli",
    ], sdk=sdk)
    assert rel_out["status"] == "SUCCESS"
    rel_id = rel_out["release"]["release_id"]

    # 2. Deploy via CLI
    dep_out = run_cli([
        "deploy",
        "--release", rel_id,
        "--env", "dev",
        "--strategy", "ROLLING",
        "--replicas", "2",
    ], sdk=sdk)
    assert dep_out["status"] == "SUCCESS"

    # 3. Flag eval via CLI
    sdk.flags.create_flag(key="beta_feature", name="Beta", enabled=True)
    flag_out = run_cli(["flag", "eval", "--key", "beta_feature", "--env", "prod"], sdk=sdk)
    assert flag_out["status"] == "SUCCESS"
    assert flag_out["enabled"] is True
