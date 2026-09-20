"""
OpenAPI Schema Backward Compatibility Engine.
"""
from __future__ import annotations
from typing import Any, Dict, List
from app.platform_verification.api_verification.domain.interfaces import IApiCompatibilityEngine
from app.platform_verification.api_verification.domain.models import ApiBreakingChange


class EnterpriseApiCompatibilityEngine(IApiCompatibilityEngine):
    """Detects breaking changes between OpenAPI specifications."""

    def compare_schemas(
        self, old_schema: Dict[str, Any], new_schema: Dict[str, Any], version_before: str, version_after: str
    ) -> List[ApiBreakingChange]:
        changes: List[ApiBreakingChange] = []

        old_paths = old_schema.get("paths", {})
        new_paths = new_schema.get("paths", {})

        # 1. Check for removed endpoint paths
        for path, methods in old_paths.items():
            if path not in new_paths:
                changes.append(
                    ApiBreakingChange(
                        change_type="REMOVED_ENDPOINT",
                        path=path,
                        field_name="",
                        version_before=version_before,
                        version_after=version_after,
                        is_breaking=True,
                        description=f"Endpoint '{path}' was removed in {version_after}.",
                    )
                )
            else:
                # Check for removed HTTP methods
                for method in methods:
                    if method not in new_paths[path]:
                        changes.append(
                            ApiBreakingChange(
                                change_type="REMOVED_HTTP_METHOD",
                                path=path,
                                field_name=method.upper(),
                                version_before=version_before,
                                version_after=version_after,
                                is_breaking=True,
                                description=f"HTTP method '{method.upper()}' was removed from '{path}'.",
                            )
                        )

        # 2. Check for breaking schema property removals or alterations
        old_components = old_schema.get("components", {}).get("schemas", {})
        new_components = new_schema.get("components", {}).get("schemas", {})

        for s_name, s_def in old_components.items():
            if s_name in new_components:
                old_props = s_def.get("properties", {})
                new_props = new_components[s_name].get("properties", {})
                old_req = s_def.get("required", [])
                new_req = new_components[s_name].get("required", [])

                # Check removed property
                for p_name in old_props:
                    if p_name not in new_props:
                        changes.append(
                            ApiBreakingChange(
                                change_type="REMOVED_FIELD",
                                path=s_name,
                                field_name=p_name,
                                version_before=version_before,
                                version_after=version_after,
                                is_breaking=True,
                                description=f"Field '{p_name}' was removed from schema '{s_name}'.",
                            )
                        )

                # Check newly added required property
                for req_p in new_req:
                    if req_p not in old_req and req_p not in old_props:
                        changes.append(
                            ApiBreakingChange(
                                change_type="NEW_REQUIRED_FIELD",
                                path=s_name,
                                field_name=req_p,
                                version_before=version_before,
                                version_after=version_after,
                                is_breaking=True,
                                description=f"New required field '{req_p}' added to schema '{s_name}' without default.",
                            )
                        )

        return changes
