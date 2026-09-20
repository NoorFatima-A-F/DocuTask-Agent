"""
CLI Interface for Continuous Verification Pipeline (PART 7).
"""
from __future__ import annotations
import argparse
import sys
from typing import List, Optional
from app.platform_verification.cicd_pipeline.domain.models import TargetEnvironment
from app.platform_verification.cicd_pipeline.runtime.cicd_platform_runtime import (
    EnterpriseCICDPlatformRuntime,
)


def run_pipeline_cli(args: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="verify pipeline", description="Continuous Verification CLI")
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

    run_parser = subparsers.add_parser("run", help="Trigger verification pipeline")
    run_parser.add_argument("--commit", required=True, help="Commit SHA")
    run_parser.add_argument("--paths", nargs="+", required=True, help="List of changed paths")
    run_parser.add_argument("--env", default="STAGING", choices=["DEVELOPMENT", "STAGING", "PRODUCTION"])

    status_parser = subparsers.add_parser("status", help="Check pipeline status")
    status_parser.add_argument("--id", required=True, help="Pipeline ID")

    parsed = parser.parse_args(args)
    runtime = EnterpriseCICDPlatformRuntime()

    if parsed.command == "run":
        ctx = runtime.change_detector.analyze_changes(
            change_id="CLI-CHANGE",
            commit_sha=parsed.commit,
            branch="main",
            author="cli-user",
            changed_paths=parsed.paths,
        )
        rec = runtime.orchestrator.trigger_pipeline(
            change_context=ctx,
            target_env=TargetEnvironment(parsed.env),
        )
        print(f"Pipeline {rec.pipeline_id} completed with status: {rec.status.value}")
        print(f"Deployment Decision: {rec.deployment_decision}")
        return 0 if rec.status.value == "PASSED" else 1

    elif parsed.command == "status":
        rec = runtime.orchestrator.get_pipeline_status(parsed.id)
        if not rec:
            print(f"Pipeline {parsed.id} not found.")
            return 1
        print(f"Pipeline: {rec.pipeline_id} ({rec.status.value})")
        for s in rec.stage_records:
            print(f"  - {s.stage_name}: {s.status.value}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(run_pipeline_cli())
