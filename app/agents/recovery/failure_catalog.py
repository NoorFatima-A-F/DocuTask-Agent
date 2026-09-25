"""
Failure Catalog.
Known failure taxonomy, standard error codes, and recommended mitigations.
"""

from typing import Dict
from pydantic import BaseModel
from app.agents.recovery.failure import FailureCategory


class CatalogEntry(BaseModel):
    category: FailureCategory
    default_recoverable: bool = True
    recommended_action: str = "RETRY"
    description: str = ""


class FailureCatalog:
    """Catalog of enterprise failure taxonomy and remediation guidance."""

    ENTRIES: Dict[FailureCategory, CatalogEntry] = {
        FailureCategory.TOOL_FAILURE: CatalogEntry(
            category=FailureCategory.TOOL_FAILURE,
            default_recoverable=True,
            recommended_action="ALTERNATE_TOOL_OR_RETRY",
            description="Tool raised an unhandled exception or timed out."
        ),
        FailureCategory.WORKER_FAILURE: CatalogEntry(
            category=FailureCategory.WORKER_FAILURE,
            default_recoverable=True,
            recommended_action="RECREATE_WORKER_OR_RETRY",
            description="Worker node crashed or failed to respond to heartbeats."
        ),
        FailureCategory.TIMEOUT_FAILURE: CatalogEntry(
            category=FailureCategory.TIMEOUT_FAILURE,
            default_recoverable=True,
            recommended_action="EXTEND_DEADLINE_OR_RETRY",
            description="Task elapsed duration exceeded configured deadline."
        ),
        FailureCategory.TOKEN_BUDGET_FAILURE: CatalogEntry(
            category=FailureCategory.TOKEN_BUDGET_FAILURE,
            default_recoverable=False,
            recommended_action="ESCALATE_TO_PLANNER_OR_HUMAN",
            description="Token budget quota exceeded."
        ),
        FailureCategory.DEPENDENCY_FAILURE: CatalogEntry(
            category=FailureCategory.DEPENDENCY_FAILURE,
            default_recoverable=False,
            recommended_action="REPLAN_OR_ROLLBACK",
            description="Deadlock or missing prerequisite node detected."
        ),
    }

    @classmethod
    def get_entry(cls, category: FailureCategory) -> CatalogEntry:
        return cls.ENTRIES.get(
            category,
            CatalogEntry(
                category=category,
                default_recoverable=True,
                recommended_action="RETRY",
                description="Generic runtime failure."
            )
        )
