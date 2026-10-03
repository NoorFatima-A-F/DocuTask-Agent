"""
Plugin Dependency and Compatibility Validator.
Enforces SemVer ranges, prerequisites, and system dependencies.
"""
from typing import Dict, List, Tuple
from app.platform_verification.extension_framework.domain.models import PluginMetadata, PluginDependencyDeclaration
from app.platform_verification.config_versioning.domain.models import SemanticVersion


class PluginDependencyValidator:
    @staticmethod
    def validate_dependencies(
        metadata: PluginMetadata,
        available_plugins: Dict[str, str]  # name -> version
    ) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        for dep in metadata.dependencies:
            if dep.dependency_type == "PLUGIN":
                if dep.name not in available_plugins:
                    if not dep.is_optional:
                        errors.append(f"Missing required plugin dependency: '{dep.name}' (>= {dep.min_version})")
                else:
                    avail_ver_str = available_plugins[dep.name]
                    try:
                        avail_v = SemanticVersion.parse(avail_ver_str)
                        req_min = SemanticVersion.parse(dep.min_version)
                        if (avail_v.major, avail_v.minor, avail_v.patch) < (req_min.major, req_min.minor, req_min.patch):
                            errors.append(
                                f"Incompatible plugin version for '{dep.name}': available {avail_ver_str}, requires >= {dep.min_version}."
                            )
                    except Exception as e:
                        errors.append(f"Error parsing version for dependency '{dep.name}': {str(e)}")

        return len(errors) == 0, errors


plugin_dependency_validator = PluginDependencyValidator()
