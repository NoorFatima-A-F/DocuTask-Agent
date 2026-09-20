"""doctaskctl: Enterprise Developer and SRE Deployment CLI."""
import argparse
import sys
from typing import Any, Dict, List, Optional
from ..core.deployment import DeploymentStrategyType
from ..sdk.client import InfrastructureSDK


def build_parser() -> argparse.ArgumentParser:
    """Constructs the CLI argument parser."""
    parser = argparse.ArgumentParser(prog="doctaskctl", description="DocuTask Platform Deployment Control CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Release command
    rel_parser = subparsers.add_parser("release", help="Release management")
    rel_sub = rel_parser.add_subparsers(dest="subcommand", required=True)
    create_rel = rel_sub.add_parser("create", help="Create a release")
    create_rel.add_argument("--version", required=True, help="Semver version (e.g. 1.2.0)")
    create_rel.add_argument("--name", required=True, help="Release name")
    create_rel.add_argument("--commit", required=True, help="Git commit SHA")
    create_rel.add_argument("--artifacts", nargs="*", default=[], help="Artifact IDs")
    create_rel.add_argument("--publish", action="store_true", default=True, help="Auto publish")

    # Deploy command
    dep_parser = subparsers.add_parser("deploy", help="Deploy a release")
    dep_parser.add_argument("--release", required=True, help="Release ID to deploy")
    dep_parser.add_argument("--env", required=True, help="Target environment (dev, testing, staging, prod)")
    dep_parser.add_argument("--strategy", choices=["ROLLING", "BLUE_GREEN", "CANARY", "SHADOW"], default="ROLLING")
    dep_parser.add_argument("--replicas", type=int, default=3)

    # Rollback command
    rb_parser = subparsers.add_parser("rollback", help="Rollback a deployment")
    rb_parser.add_argument("--deployment", required=True, help="Failed deployment ID")
    rb_parser.add_argument("--target-release", default=None, help="Target release ID")
    rb_parser.add_argument("--reason", default="Manual CLI rollback", help="Rollback reason")

    # Promote command
    prom_parser = subparsers.add_parser("promote", help="Promote release to environment")
    prom_parser.add_argument("--release", required=True, help="Release ID")
    prom_parser.add_argument("--target-env", required=True, help="Target environment")
    prom_parser.add_argument("--source-env", default=None, help="Source environment")
    prom_parser.add_argument("--roles", nargs="*", default=[], help="Approved roles")

    # Flag command
    flag_parser = subparsers.add_parser("flag", help="Feature flag evaluation")
    flag_sub = flag_parser.add_subparsers(dest="subcommand", required=True)
    eval_flag = flag_sub.add_parser("eval", help="Evaluate a flag")
    eval_flag.add_argument("--key", required=True, help="Feature flag key")
    eval_flag.add_argument("--tenant", default=None, help="Tenant ID")
    eval_flag.add_argument("--env", default="prod", help="Environment")

    return parser


def run_cli(args: Optional[List[str]] = None, sdk: Optional[InfrastructureSDK] = None) -> Dict[str, Any]:
    """Executes CLI command against InfrastructureSDK instance."""
    parser = build_parser()
    parsed = parser.parse_args(args)
    client = sdk or InfrastructureSDK()

    if parsed.command == "release" and parsed.subcommand == "create":
        rel = client.create_release(
            version=parsed.version,
            name=parsed.name,
            commit_sha=parsed.commit,
            artifact_ids=parsed.artifacts,
            auto_publish=parsed.publish,
        )
        return {"status": "SUCCESS", "release": rel.to_dict()}

    elif parsed.command == "deploy":
        dep = client.deploy(
            release_id=parsed.release,
            target_environment=parsed.env,
            strategy=DeploymentStrategyType(parsed.strategy),
            replicas=parsed.replicas,
        )
        return {"status": "SUCCESS", "deployment": dep.to_dict()}

    elif parsed.command == "rollback":
        rec = client.rollback(
            deployment_id=parsed.deployment,
            target_release_id=parsed.target_release,
            reason=parsed.reason,
        )
        return {"status": "SUCCESS", "rollback_id": rec.rollback_id}

    elif parsed.command == "promote":
        dep = client.request_and_promote(
            release_id=parsed.release,
            target_env=parsed.target_env,
            source_env=parsed.source_env,
            approved_roles=parsed.roles,
        )
        return {"status": "SUCCESS", "deployment_id": dep.deployment_id}

    elif parsed.command == "flag" and parsed.subcommand == "eval":
        is_on = client.is_feature_enabled(
            key=parsed.key,
            tenant_id=parsed.tenant,
            environment=parsed.env,
        )
        return {"status": "SUCCESS", "key": parsed.key, "enabled": is_on}

    return {"status": "ERROR", "message": "Unknown command"}
