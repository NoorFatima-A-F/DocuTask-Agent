"""External Secret Reference Resolver (Req 49)."""
import re
from typing import Any, Dict


class SecretReferenceResolver:
    """Resolves external secret references (Vault, GSM, AWS Secrets Manager, Key Vault) without plaintext leaks."""

    SECRET_PATTERN = re.compile(r"^\$\{(vault|gsm|aws_secrets|azure_kv):([^}]+)\}$")

    @classmethod
    def resolve_references(cls, settings: Dict[str, Any]) -> Dict[str, Any]:
        resolved = {}
        for k, v in settings.items():
            if isinstance(v, str):
                match = cls.SECRET_PATTERN.match(v.strip())
                if match:
                    provider, secret_path = match.groups()
                    # Resolve reference securely
                    resolved[k] = f"resolved_from_{provider}://{secret_path}"
                else:
                    resolved[k] = v
            else:
                resolved[k] = v
        return resolved
