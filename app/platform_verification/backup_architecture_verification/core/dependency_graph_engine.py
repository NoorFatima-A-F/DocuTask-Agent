"""
Part 4: Backup Dependency Graph Engine.
Constructs and validates the recovery dependency Directed Acyclic Graph (DAG),
ensuring no impossible recovery sequences or circular restore dependencies exist.
"""
from typing import List, Dict, Any, Set
from collections import defaultdict, deque
from app.platform_verification.backup_architecture_verification.domain.models import (
    AssetInventoryItem,
    DependencyGraphNode,
    BackupDependencyGraph,
)
from app.platform_verification.backup_architecture_verification.domain.interfaces import (
    IDependencyGraphEngine,
)


class DependencyGraphEngine(IDependencyGraphEngine):
    """
    Constructs the topological recovery order and validates that every asset
    can be restored in a safe, deterministic sequence without circular locks.
    """

    def __init__(self):
        # Default dependency mapping across platform subsystems
        self._default_dependency_rules: Dict[str, List[str]] = {
            "app_environment_variables": [],
            "enterprise_secrets_vault": ["app_environment_variables"],
            "platform_system_configs": ["app_environment_variables"],
            "system_governance_policies": ["platform_system_configs", "enterprise_secrets_vault"],
            "postgres_primary": ["enterprise_secrets_vault", "app_environment_variables"],
            "docker_named_volumes": ["platform_system_configs"],
            "minio_s3_object_store": ["enterprise_secrets_vault", "docker_named_volumes"],
            "uploaded_documents_raw": ["minio_s3_object_store", "postgres_primary"],
            "ocr_extracted_text_artifacts": ["uploaded_documents_raw", "minio_s3_object_store"],
            "extracted_structured_json": ["postgres_primary", "ocr_extracted_text_artifacts"],
            "ai_verification_evidence": ["minio_s3_object_store", "postgres_primary"],
            "redis_cache_queue": ["postgres_primary", "enterprise_secrets_vault"],
            "task_queue_persistence": ["redis_cache_queue", "postgres_primary"],
            "scheduled_cron_jobs": ["postgres_primary", "enterprise_secrets_vault"],
            "agent_registry_state": ["postgres_primary", "system_governance_policies"],
            "agent_memory_episodes": ["postgres_primary", "agent_registry_state"],
            "prompt_templates_repository": ["postgres_primary", "platform_system_configs"],
            "knowledge_base_documents": ["minio_s3_object_store", "postgres_primary"],
            "vector_embeddings_index": ["knowledge_base_documents", "postgres_primary"],
            "platform_verification_evidence": ["ai_verification_evidence", "postgres_primary"],
            "application_audit_logs": ["minio_s3_object_store", "postgres_primary"],
            "prometheus_metrics_db": ["docker_named_volumes", "platform_system_configs"],
            "grafana_dashboards": ["prometheus_metrics_db", "platform_system_configs"],
            "temporary_processing_cache": ["docker_named_volumes"],
            "user_session_cache": ["redis_cache_queue"],
            "generated_pdf_thumbnails": ["uploaded_documents_raw", "minio_s3_object_store"],
        }

    def build_and_validate_graph(self, assets: List[AssetInventoryItem]) -> BackupDependencyGraph:
        asset_names = {a.name: a for a in assets}
        nodes: Dict[str, DependencyGraphNode] = {}
        in_degree: Dict[str, int] = {a.name: 0 for a in assets}
        adj_list: Dict[str, List[str]] = defaultdict(list)
        validation_errors: List[str] = []

        # Populate nodes
        for asset in assets:
            deps = [
                dep for dep in self._default_dependency_rules.get(asset.name, [])
                if dep in asset_names
            ]
            nodes[asset.name] = DependencyGraphNode(
                name=asset.name,
                category=asset.category,
                criticality=asset.criticality,
                dependencies=deps,
                recovery_stage_order=0,
            )

        # Build adjacency list and in-degrees (dep -> asset, meaning dep must be restored before asset)
        for asset_name, node in nodes.items():
            for dep in node.dependencies:
                adj_list[dep].append(asset_name)
                in_degree[asset_name] += 1

        # Kahn's Algorithm for Topological Sort
        queue = deque([name for name, deg in in_degree.items() if deg == 0])
        topological_order: List[str] = []
        stage_map: Dict[str, int] = {name: 1 for name in queue}

        while queue:
            curr = queue.popleft()
            topological_order.append(curr)
            curr_stage = stage_map[curr]
            nodes[curr].recovery_stage_order = curr_stage

            for neighbor in adj_list[curr]:
                in_degree[neighbor] -= 1
                stage_map[neighbor] = max(stage_map.get(neighbor, 1), curr_stage + 1)
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        has_cycle = len(topological_order) != len(assets)
        if has_cycle:
            unresolved = [name for name, deg in in_degree.items() if deg > 0]
            validation_errors.append(f"Circular recovery dependency detected in nodes: {unresolved}")

        # Check for invalid recovery order sequences
        # e.g., Agent Registry before Database
        if "agent_registry_state" in topological_order and "postgres_primary" in topological_order:
            if topological_order.index("agent_registry_state") < topological_order.index("postgres_primary"):
                validation_errors.append("Invalid sequence: agent_registry_state scheduled before postgres_primary.")

        # e.g., Database before Secrets
        if "postgres_primary" in topological_order and "enterprise_secrets_vault" in topological_order:
            if topological_order.index("postgres_primary") < topological_order.index("enterprise_secrets_vault"):
                validation_errors.append("Invalid sequence: postgres_primary scheduled before enterprise_secrets_vault.")

        return BackupDependencyGraph(
            nodes=nodes,
            topological_recovery_order=topological_order,
            is_dag=not has_cycle,
            has_circular_dependency=has_cycle,
            validation_errors=validation_errors,
        )

    def validate_custom_recovery_sequence(
        self, graph: BackupDependencyGraph, proposed_sequence: List[str]
    ) -> bool:
        """Validates if an arbitrary proposed recovery sequence satisfies all dependency constraints."""
        seen: Set[str] = set()
        for item in proposed_sequence:
            if item not in graph.nodes:
                continue
            for dep in graph.nodes[item].dependencies:
                if dep in graph.nodes and dep not in seen:
                    return False
            seen.add(item)
        return True

    def export_dependency_graph_json(self, graph: BackupDependencyGraph) -> Dict[str, Any]:
        """Formats the dependency graph to JSON dictionary."""
        return {
            "is_valid_dag": graph.is_dag,
            "has_circular_dependency": graph.has_circular_dependency,
            "validation_errors": graph.validation_errors,
            "total_nodes": len(graph.nodes),
            "topological_recovery_order": graph.topological_recovery_order,
            "dependency_adjacency": {
                name: node.dependencies for name, node in graph.nodes.items()
            },
            "recovery_stages": {
                name: node.recovery_stage_order for name, node in graph.nodes.items()
            },
        }
