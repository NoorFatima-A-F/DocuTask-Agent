"""Governance CLI Commands Engine."""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional
from .client import CLIConfig


class GovernanceCLI:
    """Enterprise Governance Command Line Interface."""

    def __init__(self, config: Optional[CLIConfig] = None) -> None:
        self.config = config or CLIConfig()
        self.client = self.config.get_client()

    def build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="doctask-governance",
            description="DocuTask Enterprise AI Governance CLI Tool",
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Evaluate Command
        eval_parser = subparsers.add_parser("evaluate", help="Evaluate an action against governance policies")
        eval_parser.add_argument("--action", required=True, help="Action name (e.g. agent.execute)")
        eval_parser.add_argument("--resource", required=True, help="Target resource (e.g. invoice_agent)")
        eval_parser.add_argument("--context", help="JSON string representing execution context")

        # Policy Command
        policy_parser = subparsers.add_parser("policy", help="Manage governance policies")
        policy_sub = policy_parser.add_subparsers(dest="subcommand", help="Policy subcommands")
        policy_sub.add_parser("list", help="List all policies")
        get_p = policy_sub.add_parser("get", help="Get a policy by ID")
        get_p.add_argument("--id", required=True, help="Policy ID")

        # Report Command
        report_parser = subparsers.add_parser("report", help="Generate governance reports")
        report_sub = report_parser.add_subparsers(dest="subcommand", help="Report subcommands")
        gen_r = report_sub.add_parser("generate", help="Generate report")
        gen_r.add_argument("--type", default="compliance", choices=["compliance", "executive", "risk"], help="Report type")

        return parser

    def run(self, args: Optional[List[str]] = None) -> Dict[str, Any]:
        parser = self.build_parser()
        parsed_args = parser.parse_args(args)

        if not parsed_args.command:
            return {"status": "error", "message": "No command provided. Use --help."}

        if parsed_args.command == "evaluate":
            context = {}
            if parsed_args.context:
                try:
                    context = json.loads(parsed_args.context)
                except Exception:
                    pass
            decision = self.client.evaluate(
                action=parsed_args.action,
                resource=parsed_args.resource,
                context=context,
            )
            return {"status": "success", "data": decision.model_dump()}

        elif parsed_args.command == "policy":
            if parsed_args.subcommand == "list":
                policies = self.client.list_policies()
                return {"status": "success", "data": [p.model_dump() for p in policies]}
            elif parsed_args.subcommand == "get":
                policy = self.client.get_policy(parsed_args.id)
                return {"status": "success", "data": policy.model_dump()}

        elif parsed_args.command == "report":
            if parsed_args.subcommand == "generate":
                report = self.client.generate_report(report_type=parsed_args.type)
                return {"status": "success", "data": report.model_dump()}

        return {"status": "error", "message": f"Unsupported command: {parsed_args.command}"}


def main(args: Optional[List[str]] = None) -> None:
    cli = GovernanceCLI()
    res = cli.run(args)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
