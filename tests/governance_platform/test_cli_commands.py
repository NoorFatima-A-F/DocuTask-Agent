"""Tests for the Governance CLI tool."""

from app.governance.platform.cli.commands import GovernanceCLI


def test_cli_evaluate_command():
    cli = GovernanceCLI()
    res = cli.run(["evaluate", "--action", "agent.execute", "--resource", "invoice_agent"])
    assert res["status"] == "success"
    assert res["data"]["decision"] == "ALLOW"
    assert res["data"]["allowed"] is True


def test_cli_policy_commands():
    cli = GovernanceCLI()
    res = cli.run(["policy", "list"])
    assert res["status"] == "success"
    assert isinstance(res["data"], list)


def test_cli_report_command():
    cli = GovernanceCLI()
    res = cli.run(["report", "generate", "--type", "compliance"])
    assert res["status"] == "success"
    assert res["data"]["report_type"] == "compliance"
