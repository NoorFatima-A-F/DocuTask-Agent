"""doctaskctl: Official Platform Delivery & SRE CLI (Req 57, 58)."""
import argparse
from typing import Any, Dict, List, Optional
from ..sdk.client import InfrastructureSDK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="doctaskctl", description="DocuTask Platform Delivery Control CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # release
    rel_p = subparsers.add_parser("release", help="Release management")
    rel_sub = rel_p.add_subparsers(dest="subcommand", required=True)
    rel_create = rel_sub.add_parser("create", help="Create and package release")
    rel_create.add_argument("--version", required=True)
    rel_create.add_argument("--commit", required=True)
    rel_inspect = rel_sub.add_parser("inspect", help="Inspect release manifest")
    rel_inspect.add_argument("--id", required=True)

    # deploy
    dep_p = subparsers.add_parser("deploy", help="Deploy release to environment")
    dep_p.add_argument("--release", required=True)
    dep_p.add_argument("--env", required=True)
    dep_p.add_argument("--strategy", default="ROLLING")
    dep_p.add_argument("--replicas", type=int, default=3)
    dep_p.add_argument("--idempotency-key", default=None)

    # promote
    prom_p = subparsers.add_parser("promote", help="Promote release")
    prom_p.add_argument("--release", required=True)
    prom_p.add_argument("--target-env", required=True)
    prom_p.add_argument("--source-env", default=None)

    # rollback
    rb_p = subparsers.add_parser("rollback", help="Rollback deployment")
    rb_p.add_argument("--deployment", required=True)
    rb_p.add_argument("--reason", required=True)
    rb_p.add_argument("--change-ticket", default=None)
    rb_p.add_argument("--target-version", default="1.0.0")

    # artifact
    art_p = subparsers.add_parser("artifact", help="Artifact operations")
    art_sub = art_p.add_subparsers(dest="subcommand", required=True)
    art_verify = art_sub.add_parser("verify", help="Verify supply chain signature and SBOM")
    art_verify.add_argument("--digest", required=True)

    # diagnose
    diag_p = subparsers.add_parser("diagnose", help="Diagnose environment health")
    diag_p.add_argument("--env", required=True)

    # drift
    drift_p = subparsers.add_parser("drift", help="GitOps drift detection")
    drift_sub = drift_p.add_subparsers(dest="subcommand", required=True)
    drift_detect = drift_sub.add_parser("detect", help="Detect drift on application")
    drift_detect.add_argument("--app", required=True)

    return parser


def run_cli(args: Optional[List[str]] = None, sdk: Optional[InfrastructureSDK] = None) -> Dict[str, Any]:
    parser = build_parser()
    parsed = parser.parse_args(args)
    client = sdk or InfrastructureSDK()

    if parsed.command == "release" and parsed.subcommand == "create":
        rel = client.release(version=parsed.version, commit_sha=parsed.commit)
        return {"status": "SUCCESS", "release_id": rel.release_id, "version": rel.version}

    elif parsed.command == "release" and parsed.subcommand == "inspect":
        rel = client.release_manager.get_release(parsed.id)
        if not rel:
            return {"status": "ERROR", "message": "Not found"}
        return {"status": "SUCCESS", "manifest": rel.generate_manifest().to_dict()}

    elif parsed.command == "deploy":
        dep = client.deploy(
            release_id=parsed.release,
            environment_id=parsed.env,
            strategy=parsed.strategy,
            replicas=parsed.replicas,
            idempotency_key=parsed.idempotency_key,
        )
        return {"status": "SUCCESS", "deployment_id": dep.deployment_id, "deployment_status": dep.status.value}

    elif parsed.command == "promote":
        dep = client.promote(
            release_id=parsed.release,
            target_env=parsed.target_env,
            source_env=parsed.source_env,
        )
        return {"status": "SUCCESS", "deployment_id": dep.deployment_id, "target_env": parsed.target_env}

    elif parsed.command == "rollback":
        inc = client.rollback(
            deployment_id=parsed.deployment,
            reason=parsed.reason,
            target_version=parsed.target_version,
        )
        return {"status": "SUCCESS", "incident_id": inc.incident_id, "restored_version": inc.restored_version}

    elif parsed.command == "artifact" and parsed.subcommand == "verify":
        report = client.verify_artifact(artifact_digest=parsed.digest)
        return {"status": "SUCCESS", "verified": report.passed, "denial_reasons": report.denial_reasons}

    elif parsed.command == "diagnose":
        diag = client.diagnose(environment_id=parsed.env)
        return {"status": "SUCCESS", "diagnostic": diag}

    elif parsed.command == "drift" and parsed.subcommand == "detect":
        app = client.gitops_controller.get_application(parsed.app)
        if not app:
            client.gitops_controller.register_application(parsed.app, "prod", "1.0.0")
        report = client.gitops_controller.check_drift(parsed.app)
        return {"status": "SUCCESS", "has_drift": report.has_drift, "action": report.recommended_action.value}

    return {"status": "ERROR", "message": "Unknown command"}
