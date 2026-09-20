"""
Automated Markdown Documentation Generator for Verification Plugins.
"""
from app.platform_verification.extension_framework.domain.interfaces import VerificationPluginInterface


class PluginDocumentationGenerator:
    @staticmethod
    def generate_markdown(plugin: VerificationPluginInterface) -> str:
        meta = plugin.metadata
        caps = "\n".join([f"- `{c}`" for c in meta.capabilities])
        perms = "\n".join([f"- `{p.value}`" for p in meta.granted_permissions])
        
        return f"""# {meta.name} (v{meta.version})

**Plugin ID**: `{meta.plugin_id}`  
**Author**: {meta.author} | **Owner**: {meta.owner}  
**Security Classification**: `{meta.security_classification.value}`  
**License**: {meta.license}

## Description
{meta.description}

## Capabilities
{caps}

## Required Permissions
{perms}

## Minimum Platform Version
`{meta.min_platform_version}`
"""


plugin_doc_generator = PluginDocumentationGenerator()
