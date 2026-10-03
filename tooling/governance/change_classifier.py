from dataclasses import dataclass
from enum import Enum
from typing import List

class ChangeType(str, Enum):
    TYPE_A_PATCH = "TYPE_A_PATCH"
    TYPE_B_FEATURE = "TYPE_B_FEATURE"
    TYPE_C_ARCHITECTURAL = "TYPE_C_ARCHITECTURAL"

@dataclass(frozen=True)
class ChangeClassificationResult:
    change_type: ChangeType
    requires_adr: bool
    requires_architecture_review: bool
    affected_components: List[str]

class ChangeClassifier:
    @staticmethod
    def classify_paths(modified_paths: List[str]) -> ChangeClassificationResult:
        is_type_c = False
        is_type_b = False
        affected = set()

        for p in modified_paths:
            normalized = p.replace("\\", "/")
            if "app/shared_kernel/" in normalized or "k8s/" in normalized or "docker/" in normalized:
                is_type_c = True
                affected.add("shared_kernel_or_infra")
            elif "app/contexts/" in normalized:
                parts = normalized.split("/")
                idx = parts.index("contexts")
                if len(parts) > idx + 1:
                    affected.add(parts[idx + 1])
                is_type_b = True
            elif "docs/" in normalized or "tests/" in normalized:
                affected.add("docs_or_tests")

        if is_type_c:
            return ChangeClassificationResult(
                change_type=ChangeType.TYPE_C_ARCHITECTURAL,
                requires_adr=True,
                requires_architecture_review=True,
                affected_components=sorted(list(affected))
            )
        if is_type_b:
            return ChangeClassificationResult(
                change_type=ChangeType.TYPE_B_FEATURE,
                requires_adr=False,
                requires_architecture_review=False,
                affected_components=sorted(list(affected))
            )

        return ChangeClassificationResult(
            change_type=ChangeType.TYPE_A_PATCH,
            requires_adr=False,
            requires_architecture_review=False,
            affected_components=sorted(list(affected))
        )
