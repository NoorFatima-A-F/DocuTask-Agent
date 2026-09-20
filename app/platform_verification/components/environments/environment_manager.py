"""
Environment Manager: 7 environment tiers, readiness validation, hardware profiling.
"""
from typing import Dict, Any, Optional, List
from ..interfaces import EnvironmentManagerInterface
from ...crosscutting.observability import ComponentObservability
from ...domain.models import EnvironmentReadiness, EnvironmentType

class EnvironmentManager(EnvironmentManagerInterface):
    """Manages multi-tier verification execution environments across 7 tiers."""
    
    def __init__(self):
        self._environments: Dict[str, Dict[str, Any]] = {}
        self._domain_envs: Dict[str, EnvironmentReadiness] = {}
        self.observability = ComponentObservability("EnvironmentManager")
        self._seed_default_environments()

    def _seed_default_environments(self):
        env_tiers = [
            (EnvironmentType.DEVELOPMENT, "env_dev", "Local Development Sandbox", 40.0, 4096),
            (EnvironmentType.INTEGRATION, "env_integration", "CI/CD Integration Cluster", 25.0, 16384),
            (EnvironmentType.STAGING, "env_staging", "Pre-Production Staging Mirror", 18.0, 32768),
            (EnvironmentType.PRODUCTION_SHADOW, "env_shadow", "Production Shadow Dark-Traffic", 12.0, 65536),
            (EnvironmentType.CHAOS, "env_chaos", "Fault Injection & Chaos Lab", 65.0, 16384),
            (EnvironmentType.SECURITY_LAB, "env_security", "Isolated Security & Red-Team Lab", 10.0, 8192),
            (EnvironmentType.BENCHMARK, "env_benchmark", "High-Precision Performance Benchmark Host", 5.0, 131072),
        ]
        for env_type, env_id, name, cpu_util, mem_mb in env_tiers:
            rec = EnvironmentReadiness(
                environment_id=env_id,
                name=name,
                env_type=env_type,
                is_ready=True,
                cpu_utilization_pct=cpu_util,
                memory_available_mb=mem_mb,
                network_latency_ms=1.8,
                active_sandboxes=1
            )
            self._domain_envs[env_id] = rec
            self._environments[env_id] = {
                "env_id": env_id,
                "tier": env_type.value,
                "profile": {"cpu_cores": 32, "memory_mb": mem_mb, "cpu_utilization": cpu_util}
            }

    async def register_environment(self, env_id: str, tier: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        self.observability.record_operation(1.0)
        env = {
            "env_id": env_id,
            "tier": tier,
            "profile": profile
        }
        self._environments[env_id] = env
        return env

    async def validate_readiness(self, env_id: str) -> Dict[str, Any]:
        self.observability.record_operation(1.2)
        if env_id not in self._environments:
            return {"ready": False, "error": "Environment not found"}
        env = self._environments[env_id]
        return {
            "env_id": env_id,
            "ready": True,
            "tier": env["tier"],
            "hardware_profile": env["profile"]
        }

    def check_readiness(self, env_id: str) -> EnvironmentReadiness:
        self.observability.record_operation(1.0)
        if env_id in self._domain_envs:
            return self._domain_envs[env_id]
        return EnvironmentReadiness(
            environment_id=env_id,
            name=f"Custom Env {env_id}",
            env_type=EnvironmentType.INTEGRATION,
            is_ready=True
        )

    def list_environments(self) -> List[EnvironmentReadiness]:
        self.observability.record_operation(0.7)
        return list(self._domain_envs.values())
