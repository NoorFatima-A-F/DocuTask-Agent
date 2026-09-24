"""Tests for Tool Safety Validator, Permission Manager, and Sandboxing."""

from app.safety.tools.permissions import ToolPermissionManager
from app.safety.tools.validator import ToolSafetyValidator
from app.safety.tools.sandbox import ToolSandboxEngine


def test_tool_permission_manager():
    mgr = ToolPermissionManager()
    
    # Safe read allowed for standard user
    assert mgr.can_invoke("view_file", user_role="user") is True
    
    # Destructive high risk blocked for standard user
    assert mgr.can_invoke("delete_database_table", user_role="user") is False
    assert mgr.can_invoke("delete_database_table", user_role="admin") is True


def test_tool_safety_validator_dangerous_parameters():
    validator = ToolSafetyValidator()
    
    # Path traversal attempt
    is_safe, violations = validator.validate_tool_invocation(
        tool_name="view_file",
        parameters={"path": "../../etc/shadow"},
        user_role="developer",
    )
    assert is_safe is False
    assert any("Path traversal" in v.message for v in violations)

    # Destructive SQL command in parameter
    is_safe_sql, sql_viols = validator.validate_tool_invocation(
        tool_name="run_command",
        parameters={"query": "DROP TABLE users CASCADE;"},
        user_role="developer",
    )
    assert is_safe_sql is False
    assert any("Destructive SQL" in v.message for v in sql_viols)


def test_tool_sandbox_execution_and_dry_run():
    sandbox = ToolSandboxEngine()
    
    # Dry run should pass without performing live mutations
    res_dry = sandbox.execute_in_sandbox(
        tool_name="write_to_file",
        parameters={"file": "test.txt", "content": "hello"},
        user_role="developer",
        is_dry_run=True,
    )
    assert res_dry.is_executed is True
    assert res_dry.is_dry_run is True
    assert res_dry.safety_passed is True

    # Blocked dangerous invocation
    res_blocked = sandbox.execute_in_sandbox(
        tool_name="delete_database_table",
        parameters={"table": "invoices"},
        user_role="user",
        is_dry_run=False,
    )
    assert res_blocked.is_executed is False
    assert res_blocked.safety_passed is False
    assert "blocked" in res_blocked.error.lower()
