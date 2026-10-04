"""
DocuTask Agentic CLI.
Autonomous Evaluation, Chaos Injection, and Telemetry Engine.
"""

from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from evals.suites.chaos import ChaosEngine
from evals.suites.extraction import ExtractionHarness
from evals.suites.reliability import DisasterRecoveryHarness


def evaluate(
    suite: str = "all",
    threshold: float = 0.85,
    strict: bool = True,
    output_dir: str = "artifacts",
) -> Dict[str, Any]:
    """Execute agent-driven evaluation harness and record telemetry."""
    print("=" * 70)
    print(f"  DocuTask-Agent Autonomous Evaluation Suite: [{suite.upper()}]")
    print(f"  Target Confidence Threshold: {threshold * 100:.1f}% | Strict Mode: {strict}")
    print("=" * 70)

    os.makedirs(output_dir, exist_ok=True)
    telemetry: Dict[str, Any] = {}

    if suite in ("extraction", "all"):
        harness = ExtractionHarness(confidence_threshold=threshold)
        res = harness.evaluate_dataset("golden_invoices")
        telemetry["extraction"] = res
        print(f"[+] Extraction Suite: {res.get('status', 'PASSED')} | Accuracy: {res.get('precision', 0.0) * 100:.1f}% | F1: {res.get('f1_score', 0.0)}")
        if strict and res.get("precision", 1.0) < threshold:
            print(f"[!] Warning: Extraction precision below strict threshold ({threshold})")

    if suite in ("chaos", "all"):
        chaos = ChaosEngine(fault_rate=0.15)
        res = chaos.run_chaos_drill()
        telemetry["chaos"] = res
        print(f"[+] Chaos Drill Suite: {res.get('status', 'PASSED')} | Recovery: {res.get('self_healing_recovery_time_sec', 0.0)}s")

    if suite in ("reliability", "all"):
        dr = DisasterRecoveryHarness(workers=10, fault_rate=0.2)
        res = dr.run(source_region="us-east-1", target_region="eu-central-1")
        telemetry["reliability"] = res
        print(f"[+] Reliability Suite: {res.get('status', 'PASSED')} | RPO: {res.get('rpo_achieved_sec', 0.0)}s | Data Loss: {res.get('data_loss_detected', False)}")

    artifact_path = Path(output_dir) / "verification_telemetry.json"
    with open(artifact_path, "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2)

    print(f"[*] Telemetry archived to: {artifact_path}")
    return telemetry


def simulate_chaos(fault_rate: float = 0.15) -> Dict[str, Any]:
    """Inject stochastic faults into task processing pipelines."""
    print(f"[*] Executing Chaos Drill with fault injection probability: {fault_rate:.2f}")
    engine = ChaosEngine(fault_rate=fault_rate)
    res = engine.run_chaos_drill()
    print(f"[+] Chaos Drill Completed: status={res.get('status')} self_healing_time={res.get('self_healing_recovery_time_sec')}s")
    return res


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="docutask-agent",
        description="DocuTask Agent CLI: Autonomous Evaluations & Chaos Testing",
    )
    subparsers = parser.add_subparsers(dest="command", help="Agent commands")

    # evaluate
    eval_p = subparsers.add_parser("evaluate", help="Execute agent-driven evaluation suite")
    eval_p.add_argument(
        "--suite",
        default="all",
        choices=["all", "extraction", "chaos", "reliability"],
        help="Target suite (extraction | chaos | reliability | all)",
    )
    eval_p.add_argument(
        "--threshold",
        type=float,
        default=0.85,
        help="Minimum precision / confidence threshold",
    )
    eval_p.add_argument(
        "--strict",
        action="store_true",
        default=True,
        help="Halt or flag if confidence degrades",
    )
    eval_p.add_argument(
        "--output-dir",
        default="artifacts",
        help="Output directory for telemetry JSON",
    )

    # simulate-chaos
    chaos_p = subparsers.add_parser("simulate-chaos", help="Execute synthetic chaos fault drill")
    chaos_p.add_argument(
        "--fault-rate",
        type=float,
        default=0.15,
        help="Stochastic failure injection probability (0.0 - 1.0)",
    )

    return parser


def main(args: Optional[List[str]] = None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        return 0

    if parsed.command == "evaluate":
        evaluate(
            suite=parsed.suite,
            threshold=parsed.threshold,
            strict=parsed.strict,
            output_dir=parsed.output_dir,
        )
        return 0
    elif parsed.command == "simulate-chaos":
        simulate_chaos(fault_rate=parsed.fault_rate)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
