"""
Unit and Integration tests for Enterprise API Architecture Verification (PART 2E).
"""
import pytest
from app.platform_verification.api_verification import (
    EnterpriseApiVerificationRuntime,
)


@pytest.fixture
def runtime():
    return EnterpriseApiVerificationRuntime()


def test_api_compatibility_engine_detects_removed_fields(runtime):
    """Test detecting breaking changes when an API schema field is removed or renamed."""
    old_schema = {
        "paths": {"/documents/{id}": {"get": {}}},
        "components": {
            "schemas": {
                "DocumentResponse": {
                    "type": "object",
                    "required": ["id", "status"],
                    "properties": {
                        "id": {"type": "string"},
                        "status": {"type": "string"},
                        "name": {"type": "string"},
                    },
                }
            }
        },
    }

    # New schema removes 'name' and adds required 'author'
    new_schema = {
        "paths": {"/documents/{id}": {"get": {}}},
        "components": {
            "schemas": {
                "DocumentResponse": {
                    "type": "object",
                    "required": ["id", "status", "author"],
                    "properties": {
                        "id": {"type": "string"},
                        "status": {"type": "string"},
                        "author": {"type": "string"},
                    },
                }
            }
        },
    }

    changes = runtime.compatibility_engine.compare_schemas(
        old_schema=old_schema,
        new_schema=new_schema,
        version_before="v1.0",
        version_after="v2.0",
    )

    assert len(changes) >= 2
    assert any(c.change_type == "REMOVED_FIELD" and c.field_name == "name" for c in changes)
    assert any(c.change_type == "NEW_REQUIRED_FIELD" and c.field_name == "author" for c in changes)


def test_async_agent_workflow_state_machine(runtime):
    """Test validating AI agent asynchronous task lifecycle state transitions."""
    # Valid transitions
    ok1, _ = runtime.workflow_validator.validate_task_transitions("CREATED", "RUNNING")
    assert ok1 is True

    ok2, _ = runtime.workflow_validator.validate_task_transitions("RUNNING", "COMPLETED")
    assert ok2 is True

    # Invalid transition (Cannot resume completed task)
    ok3, msg3 = runtime.workflow_validator.validate_task_transitions("COMPLETED", "RUNNING")
    assert ok3 is False
    assert "Illegal state transition" in msg3


def test_api_ast_purity_analyzer(runtime):
    """Test AST scanning of existing repository API endpoints."""
    pkg = runtime.run_full_scan()
    assert pkg.scan_id.startswith("API-SCAN-")
    assert pkg.scorecard is not None
    assert pkg.scorecard.total_score >= 80.0
    assert len(pkg.evidence_sha256) == 64
