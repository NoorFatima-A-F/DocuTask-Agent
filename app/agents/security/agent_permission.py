"""
Agent Role and Permission Definitions for Security Governance Layer.
Defines granular Role-Based Access Control (RBAC) privileges across autonomous agent types.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, Set


class AgentRole(str, Enum):
    ADMIN = "ADMIN"
    COORDINATOR = "COORDINATOR"
    EXTRACTOR = "EXTRACTOR"
    VALIDATOR = "VALIDATOR"
    AUDITOR = "AUDITOR"
    RECOVERY_SPECIALIST = "RECOVERY_SPECIALIST"


class AgentPermission(str, Enum):
    READ_DOCUMENT = "READ_DOCUMENT"
    WRITE_DOCUMENT = "WRITE_DOCUMENT"
    EXECUTE_OCR = "EXECUTE_OCR"
    EXECUTE_LLM = "EXECUTE_LLM"
    MUTATE_GRAPH = "MUTATE_GRAPH"
    INVOKE_TOOL = "INVOKE_TOOL"
    DELETE_DATA = "DELETE_DATA"
    EXPORT_DATA = "EXPORT_DATA"
    ESCALATE_HUMAN = "ESCALATE_HUMAN"
    REPLAY_WORKFLOW = "REPLAY_WORKFLOW"


# Principle of Least Privilege: Role -> Granted Permissions Mapping
ROLE_PERMISSION_MATRIX: Dict[AgentRole, Set[AgentPermission]] = {
    AgentRole.ADMIN: {
        AgentPermission.READ_DOCUMENT,
        AgentPermission.WRITE_DOCUMENT,
        AgentPermission.EXECUTE_OCR,
        AgentPermission.EXECUTE_LLM,
        AgentPermission.MUTATE_GRAPH,
        AgentPermission.INVOKE_TOOL,
        AgentPermission.DELETE_DATA,
        AgentPermission.EXPORT_DATA,
        AgentPermission.ESCALATE_HUMAN,
        AgentPermission.REPLAY_WORKFLOW,
    },
    AgentRole.COORDINATOR: {
        AgentPermission.READ_DOCUMENT,
        AgentPermission.WRITE_DOCUMENT,
        AgentPermission.EXECUTE_LLM,
        AgentPermission.MUTATE_GRAPH,
        AgentPermission.INVOKE_TOOL,
        AgentPermission.ESCALATE_HUMAN,
        AgentPermission.REPLAY_WORKFLOW,
    },
    AgentRole.EXTRACTOR: {
        AgentPermission.READ_DOCUMENT,
        AgentPermission.WRITE_DOCUMENT,
        AgentPermission.EXECUTE_OCR,
        AgentPermission.EXECUTE_LLM,
        AgentPermission.INVOKE_TOOL,
    },
    AgentRole.VALIDATOR: {
        AgentPermission.READ_DOCUMENT,
        AgentPermission.EXECUTE_LLM,
        AgentPermission.INVOKE_TOOL,
        AgentPermission.ESCALATE_HUMAN,
    },
    AgentRole.AUDITOR: {
        AgentPermission.READ_DOCUMENT,
        AgentPermission.EXPORT_DATA,
    },
    AgentRole.RECOVERY_SPECIALIST: {
        AgentPermission.READ_DOCUMENT,
        AgentPermission.WRITE_DOCUMENT,
        AgentPermission.MUTATE_GRAPH,
        AgentPermission.INVOKE_TOOL,
        AgentPermission.ESCALATE_HUMAN,
        AgentPermission.REPLAY_WORKFLOW,
    },
}
