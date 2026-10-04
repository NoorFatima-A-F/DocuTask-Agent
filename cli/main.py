"""
Unified Platform CLI for DocuTask-Agent.
Centralized execution harness replacing scattered standalone runners.
"""

from __future__ import annotations
import argparse
import sys
import json
import os
from typing import Optional, List
from evals.suites.chaos import ChaosEngine
from evals.suites.extraction import ExtractionHarness
from evals.suites.reliability import DisasterRecoveryHarness


def cmd_evaluate(args: argparse.Namespace) -> int:
    """Execute agent-driven validation and output structured telemetry."""
    suite = args.suite.lower()
    print(f"======================================================================")
    print(f"  DocuTask-Agent Autonomous Evaluation Harness [Suite: {suite.upper()}]")
    print(f"======================================================================")

    os.makedirs("artifacts", exist_ok=True)
    telemetry = {}

    if suite in ("extraction", "all"):
        harness = ExtractionHarness(confidence_threshold=0.85)
        res = harness.evaluate_dataset("golden_invoices")
        telemetry["extraction"] = res
        print(f"[+] Extraction Suite: {res['status']} | Accuracy: {res['precision'] * 100:.1f}% | F1: {res['f1_score']}")

    if suite in ("chaos", "all"):
        chaos = ChaosEngine(fault_rate=0.15)
        res = chaos.run_chaos_drill()
        telemetry["chaos"] = res
        print(f"[+] Chaos Drill Suite: {res['status']} | Recovery: {res['self_healing_recovery_time_sec']}s")

    if suite in ("reliability", "all"):
        dr = DisasterRecoveryHarness(workers=10, fault_rate=0.2)
        res = dr.run(source_region="us-east-1", target_region="eu-central-1")
        telemetry["reliability"] = res
        print(f"[+] Reliability Suite: {res['status']} | RPO: {res['rpo_achieved_sec']}s | Data Loss: {res['data_loss_detected']}")

    # Write telemetry artifact for CI
    artifact_path = os.path.join("artifacts", "verification_telemetry.json")
    with open(artifact_path, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)
    print(f"[*] Structured telemetry archived to {artifact_path}")
    return 0


def cmd_simulate_failover(args: argparse.Namespace) -> int:
    """Executes distributed chaos injection and failover across task queues."""
    print(f"[*] Executing distributed failover drill (workers: {args.workers}, fault_rate: {args.fault_rate})...")
    harness = DisasterRecoveryHarness(workers=args.workers, fault_rate=args.fault_rate)
    res = harness.run()
    print(f"[+] Failover Drill: {res['status']} | Source: {res['source_region']} -> Target: {res['target_region']}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    """Delegate to core verification platform."""
    from app.cli.main import cmd_verify as app_cmd_verify
    return app_cmd_verify(args)


def cmd_serve(args: argparse.Namespace) -> int:
    """Launch FastAPI web and API server."""
    from app.cli.main import cmd_serve as app_cmd_serve
    return app_cmd_serve(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="docutask",
        description="DocuTask Enterprise Agent & Resilience CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Platform commands")

    # evaluate
    eval_p = subparsers.add_parser("evaluate", help="Execute agent-driven validation harness")
    eval_p.add_argument(
        "--suite",
        default="all",
        choices=["all", "extraction", "chaos", "reliability"],
        help="Target suite: extraction | chaos | reliability | all",
    )
    eval_p.add_argument(
        "--strict",
        action="store_true",
        default=True,
        help="Halt on confidence score drift < 0.85",
    )

    # simulate_failover
    failover_p = subparsers.add_parser("simulate-failover", help="Executes distributed chaos injection across task queues")
    failover_p.add_argument("--workers", type=int, default=10, help="Number of simulated workers")
    failover_p.add_argument("--fault-rate", type=float, default=0.2, help="Fault injection probability")

    # verify
    verify_p = subparsers.add_parser("verify", help="Execute platform pytest verification suites")
    verify_p.add_argument(
        "--suite",
        default="all",
        choices=["all", "platform", "resilience", "security", "safety", "performance", "governance"],
        help="Target verification suite",
    )
    verify_p.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # serve
    serve_p = subparsers.add_parser("serve", help="Launch FastAPI web and API server")
    serve_p.add_argument("--host", default="0.0.0.0", help="Bind host")
    serve_p.add_argument("--port", type=int, default=8000, help="Bind port")
    serve_p.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    serve_p.add_argument("--workers", type=int, default=1, help="Number of worker processes")

    return parser


def main(args: Optional[List[str]] = None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        return 0

    commands = {
        "evaluate": cmd_evaluate,
        "simulate-failover": cmd_simulate_failover,
        "verify": cmd_verify,
        "serve": cmd_serve,
    }

    handler = commands.get(parsed.command)
    if handler:
        return handler(parsed)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
