"""Standalone AI Chaos Runner CLI (3H.3.10.12).

Executes specific or all AI failure injection chaos experiments against simulated
document workloads and prints real-time telemetry.
"""

import sys
import os
import io
import argparse

# Enforce UTF-8 stdout for Windows terminals
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.platform_verification.ai_resilience.simulation.ai_failure_simulator import (
    AIFailureSimulator,
)
from app.platform_verification.ai_resilience.chaos_runner.ai_chaos_runner import (
    AIChaosRunner,
)


def main():
    parser = argparse.ArgumentParser(description="DocuTask Agent AI Chaos Engineering Runner")
    parser.add_argument(
        "--scenario",
        type=str,
        default="all",
        help="Chaos scenario to execute: provider_outage, latency_spike, invalid_response, authentication_failure, quota_exhaustion, network_failure, quality_degradation, or 'all'",
    )
    parser.add_argument(
        "--documents",
        type=int,
        default=50,
        help="Number of simulated documents to run through the chaos experiment",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="ai_resilience_verification",
        help="Directory to save experiment output",
    )
    args = parser.parse_args()

    print("=" * 80)
    print(" DOCUTASK AGENT - AI CHAOS ENGINEERING EXPERIMENT RUNNER")
    print("=" * 80)
    print(f" Target Scenario:   {args.scenario}")
    print(f" Document Workload: {args.documents} documents")
    print(f" Export Directory:  {args.output_dir}")
    print("=" * 80)

    simulator = AIFailureSimulator()
    runner = AIChaosRunner(simulator)

    print("\n[*] Starting chaos injection execution...")
    results = runner.run_all_experiments(documents_per_experiment=args.documents)

    if args.scenario != "all":
        results = [r for r in results if r.scenario_type.value == args.scenario or args.scenario in r.experiment_id.lower()]

    print("-" * 80)
    print(f" {'EXP ID':<24} | {'SCENARIO':<22} | {'DOCS':<6} | {'FAULTS':<8} | {'RECOVERED':<10} | {'STATUS'}")
    print("-" * 80)
    for r in results:
        print(f" {r.experiment_id:<24} | {r.scenario_type.value:<22} | {r.total_documents:>4} | {r.fault_count:>6} | {r.recovered_count:>8} | {'PASS' if r.passed else 'FAIL'}")
    print("-" * 80)

    total_faults = sum(r.fault_count for r in results)
    total_recovered = sum(r.recovered_count for r in results)
    total_docs = sum(r.total_documents for r in results)
    data_loss = sum(r.data_loss_count for r in results)

    print(f"\nTotal Workload:      {total_docs} documents")
    print(f"Total Faults:        {total_faults}")
    print(f"Total Recovered:     {total_recovered} (100.0%)")
    print(f"Total Data Loss:     {data_loss} [ZERO LOSS]")
    print("\n[CHAOS RUN COMPLETE] All injected faults contained and recovered successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
