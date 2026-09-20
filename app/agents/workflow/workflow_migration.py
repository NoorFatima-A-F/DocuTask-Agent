"""
Workflow Migration Engine.
Coordinates zero-downtime, in-flight schema migrations of running workflow instances across definition versions.
"""

import logging
from typing import Any, Dict, Optional
from uuid import UUID
from app.agents.workflow.exceptions import InvalidWorkflowMigrationError
from app.agents.workflow.lifecycle import WorkflowLifecycleState
from app.agents.workflow.workflow_definition import WorkflowDefinition
from app.agents.workflow.workflow_instance import WorkflowInstance
from app.agents.workflow.workflow_version import WorkflowVersion

logger = logging.getLogger(__name__)


class WorkflowMigrationEngine:
    """Manages version compatibility checking and state migration for running workflow instances."""

    def can_migrate(
        self,
        current_version: WorkflowVersion,
        target_version: WorkflowVersion,
    ) -> bool:
        """Determines if the target version is backward-compatible with current version."""
        return target_version.is_backward_compatible_with(current_version)

    def migrate_instance(
        self,
        instance: WorkflowInstance,
        target_definition: WorkflowDefinition,
    ) -> WorkflowInstance:
        """
        Migrates a workflow instance to the target definition if compatible.
        Transitions state to MIGRATING temporarily and back to RUNNING.
        """
        source_version = instance.identity.version
        target_version = target_definition.version

        if not self.can_migrate(source_version, target_version):
            raise InvalidWorkflowMigrationError(
                f"Cannot migrate instance {instance.instance_id} from {source_version.to_string()} "
                f"to breaking version {target_version.to_string()}.",
                workflow_id=instance.instance_id,
            )

        logger.info(
            f"Migrating instance {instance.instance_id} from {source_version.to_string()} to {target_version.to_string()}"
        )

        # Transition to MIGRATING
        migrating_instance = instance.transition_to(WorkflowLifecycleState.MIGRATING)

        # Update identity to new definition and version
        updated_identity = migrating_instance.identity.model_copy(
            update={
                "definition_id": target_definition.definition_id,
                "version": target_version,
            }
        )

        # Complete migration by transitioning back to RUNNING
        migrated_instance = migrating_instance.model_copy(
            update={
                "identity": updated_identity,
                "definition_id": target_definition.definition_id,
            }
        ).transition_to(WorkflowLifecycleState.RUNNING)

        return migrated_instance
