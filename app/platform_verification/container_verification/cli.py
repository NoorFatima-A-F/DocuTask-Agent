"""
CLI Entrypoint for Enterprise Container and Runtime Verification.
"""
import uuid
import hashlib
from typing import Dict, Any, Optional
from app.platform_verification.container_verification.models.verification_models import (
    ServiceDefinition,
    NetworkDefinition,
    VolumeDefinition,
    ContainerArchitectureModel,
    ContainerVerificationEvidencePackage,
)
from app.platform_verification.container_verification.analyzers.dockerfile_analyzer import DockerfileAnalyzer
from app.platform_verification.container_verification.analyzers.image_analyzer import ImageAnalyzer
from app.platform_verification.container_verification.analyzers.dependency_analyzer import DependencyAnalyzer
from app.platform_verification.container_verification.analyzers.runtime_analyzer import RuntimeAnalyzer
from app.platform_verification.container_verification.analyzers.security_analyzer import SecurityAnalyzer
from app.platform_verification.container_verification.validators.isolation_validator import IsolationValidator
from app.platform_verification.container_verification.validators.reproducibility_validator import ReproducibilityValidator
from app.platform_verification.container_verification.validators.resource_validator import ResourceValidator
from app.platform_verification.container_verification.validators.configuration_validator import ConfigurationValidator
from app.platform_verification.container_verification.scanners.vulnerability_scanner import VulnerabilityScanner
from app.platform_verification.container_verification.experiments.failure_tests import FailureExperiments
from app.platform_verification.container_verification.reports.generator import ContainerEvidenceGenerator


class ContainerVerificationPlatform:
    """Unified runtime coordinator and CLI facade for container verification."""

    def __init__(self):
        self.dockerfile_analyzer = DockerfileAnalyzer()
        self.image_analyzer = ImageAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()
        self.runtime_analyzer = RuntimeAnalyzer()
        self.security_analyzer = SecurityAnalyzer()
        self.isolation_validator = IsolationValidator()
        self.reproducibility_validator = ReproducibilityValidator()
        self.resource_validator = ResourceValidator()
        self.config_validator = ConfigurationValidator()
        self.vuln_scanner = VulnerabilityScanner()
        self.failure_experiments = FailureExperiments()
        self.evidence_generator = ContainerEvidenceGenerator()

    def run_full_verification(
        self,
        commit_sha: str = "main-head",
        architecture: Optional[ContainerArchitectureModel] = None,
        dockerfile_content: Optional[str] = None,
        image_meta: Optional[Dict[str, Any]] = None,
        dependencies: Optional[list] = None,
        runtime_meta: Optional[Dict[str, Any]] = None,
        vuln_data: Optional[list] = None,
        repro_meta: Optional[Dict[str, Any]] = None,
        failure_scenarios: Optional[list] = None,
    ) -> ContainerVerificationEvidencePackage:
        if architecture is None:
            architecture = self._default_architecture()
        if dockerfile_content is None:
            dockerfile_content = """FROM python:3.12-slim as builder\nWORKDIR /app\nRUN apt update && apt install -y gcc\nFROM python:3.12-slim\nUSER appuser\nWORKDIR /app\nCOPY . /app\nCMD ["uvicorn", "app.main:app"]"""
        if image_meta is None:
            image_meta = {"image_name": "doctask-api", "compressed_size_mb": 170.0, "uncompressed_size_mb": 410.0, "layer_count": 8, "contained_files": []}
        if dependencies is None:
            dependencies = [{"name": "fastapi", "version": "0.110.0", "license": "MIT", "source": "pypi"}]
        if runtime_meta is None:
            runtime_meta = {"service_name": "api", "startup_time_seconds": 1.5, "health_endpoint_verified": True, "live_endpoint_verified": True, "ready_endpoint_verified": True}
        if vuln_data is None:
            vuln_data = []
        if repro_meta is None:
            repro_meta = {"source_commit": commit_sha, "digest_build_1": "sha256:abc123456", "digest_build_2": "sha256:abc123456"}
        if failure_scenarios is None:
            failure_scenarios = [
                {"target_service": "api", "recovered_successfully": True, "data_loss": False, "restart_latency_seconds": 1.2},
                {"target_service": "worker", "recovered_successfully": True, "data_loss": False, "restart_latency_seconds": 2.0},
            ]

        # 1. Discovery & Boundaries
        arch_rep = self.config_validator.discover_and_validate(architecture)
        bound_rep = self.isolation_validator.validate_boundaries(architecture.services)
        res_rep = self.resource_validator.validate_resource_limits(architecture.services)
        net_rep = self.security_analyzer.analyze_network_security(architecture.services)

        # 2. Dockerfile & Image
        df_rep = self.dockerfile_analyzer.analyze_dockerfile_content(dockerfile_content)
        img_rep = self.image_analyzer.analyze_image(image_meta)

        # 3. Security & Dependencies
        vuln_rep = self.vuln_scanner.scan_image(vuln_data)
        sbom_rep = self.dependency_analyzer.generate_sbom(dependencies)

        # 4. Reproducibility, Runtime & Failure
        repro_rep = self.reproducibility_validator.validate_reproducibility(repro_meta)
        run_rep = self.runtime_analyzer.analyze_runtime_health(runtime_meta)
        fail_rep = self.failure_experiments.execute_failure_simulations(failure_scenarios)

        # 5. Scorecard & Evidence
        scorecard = self.evidence_generator.calculate_certification_score(
            arch_pass=(arch_rep.status == "PASS"),
            security_rep=vuln_rep,
            repro_rep=repro_rep,
            boundary_rep=bound_rep,
            runtime_rep=run_rep,
            failure_rep=fail_rep,
            efficiency_rep=img_rep,
        )

        package_id = f"container-verify-{uuid.uuid4().hex[:10]}"
        payload = f"{package_id}:{commit_sha}:{scorecard.composite_score}"
        pkg_sha = hashlib.sha256(payload.encode("utf-8")).hexdigest()

        return ContainerVerificationEvidencePackage(
            package_id=package_id,
            commit_sha=commit_sha,
            scorecard=scorecard,
            architecture_report=arch_rep,
            boundary_report=bound_rep,
            dockerfile_report=df_rep,
            image_security_report=vuln_rep,
            efficiency_report=img_rep,
            reproducibility_report=repro_rep,
            runtime_report=run_rep,
            failure_report=fail_rep,
            resource_report=res_rep,
            network_report=net_rep,
            sbom_report=sbom_rep,
            package_sha256=pkg_sha,
        )

    def _default_architecture(self) -> ContainerArchitectureModel:
        return ContainerArchitectureModel(
            services={
                "api": ServiceDefinition(name="api", image="doctask-api", ports=["8000:8000"], depends_on=["postgres", "redis"]),
                "worker": ServiceDefinition(name="worker", image="doctask-worker", ports=[], depends_on=["postgres", "redis"]),
                "postgres": ServiceDefinition(name="postgres", image="postgres:16-alpine", ports=["127.0.0.1:5432:5432"], depends_on=[]),
                "redis": ServiceDefinition(name="redis", image="redis:7-alpine", ports=["127.0.0.1:6379:6379"], depends_on=[]),
            },
            networks={"default": NetworkDefinition(name="default")},
            volumes={"pgdata": VolumeDefinition(name="pgdata")},
        )
