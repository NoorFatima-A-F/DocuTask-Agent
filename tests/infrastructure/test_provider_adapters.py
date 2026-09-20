"""Tests for Multi-Cloud Provider Adapters (Kubernetes, AWS, GCP, Azure, Local)."""

from app.infrastructure.providers.aws import AWSComputeProvider, AWSSecretsManagerProvider
from app.infrastructure.providers.azure import AzureComputeProvider, AzureKeyVaultProvider
from app.infrastructure.providers.gcp import GCPComputeProvider, GCPSecretManagerProvider
from app.infrastructure.providers.kubernetes import KubernetesComputeProvider, KubernetesSecretProvider
from app.infrastructure.providers.local import LocalComputeProvider, LocalSecretProvider


def test_kubernetes_provider():
    k8s = KubernetesComputeProvider(namespace="doctask-prod")
    res = k8s.create_instance(name="doc-service", image="docutask:1.0", cpu=2.0, memory_mb=4096)
    assert res.provider_name == "kubernetes"
    assert res.status == "Running"
    assert "doctask-prod" in res.endpoint

    sec = KubernetesSecretProvider(namespace="doctask-prod")
    assert sec.set_secret("db_pass", "secret123") is True
    assert sec.get_secret("db_pass") == "secret123"


def test_aws_provider():
    aws = AWSComputeProvider(region="us-east-1")
    res = aws.create_instance(name="worker", image="worker:latest", cpu=1.0, memory_mb=2048)
    assert res.provider_name == "aws"
    assert res.instance_id.startswith("arn:aws:ecs:")

    sec = AWSSecretsManagerProvider(region="us-east-1")
    assert sec.set_secret("api_token", "tok_aws_999") is True
    assert sec.get_secret("api_token") == "tok_aws_999"


def test_gcp_provider():
    gcp = GCPComputeProvider(project_id="doctask-ai", region="us-central1")
    res = gcp.create_instance(name="knowledge-engine", image="ke:1.0", cpu=4.0, memory_mb=8192)
    assert res.provider_name == "gcp"
    assert "a.run.app" in res.endpoint

    sec = GCPSecretManagerProvider(project_id="doctask-ai")
    assert sec.set_secret("gcp_key", "sec_val") is True
    assert sec.get_secret("gcp_key") == "sec_val"


def test_azure_provider():
    azure = AzureComputeProvider(subscription_id="sub-1", resource_group="rg-ai")
    res = azure.create_instance(name="analytics", image="analytics:v1", cpu=2.0, memory_mb=4096)
    assert res.provider_name == "azure"
    assert "azurecontainerapps.io" in res.endpoint

    sec = AzureKeyVaultProvider(vault_name="kv-prod")
    assert sec.set_secret("cert", "pem_content") is True
    assert sec.get_secret("cert") == "pem_content"


def test_local_provider():
    local = LocalComputeProvider()
    res = local.create_instance(name="local-worker", image="local:dev", cpu=1.0, memory_mb=1024)
    assert res.provider_name == "local"
    assert "localhost" in res.endpoint

    sec = LocalSecretProvider()
    assert sec.set_secret("local_pass", "dev_secret") is True
    assert sec.get_secret("local_pass") == "dev_secret"
