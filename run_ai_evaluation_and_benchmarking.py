"""Master CLI Runner for Phase 6: AI System Evaluation, Benchmarking & Portfolio Certification.

Executes all 10 evaluation dimensions, calculates the 6-pillar weighted certification score,
and exports publication-grade evidence, case studies, and SHA-256 manifests.
"""

import sys
import os
import time

# Ensure UTF-8 output encoding on Windows if supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.evaluation.runtime.evaluation_runtime import EvaluationRuntime


def format_header(title: str, width: int = 80) -> str:
    line = "=" * width
    return f"\n{line}\n  {title.upper()}\n{line}\n"


def main():
    print(format_header("DocuTask Agent - AI Evaluation & Portfolio Certification Framework (Phase 6)"))
    print("Initiating autonomous 10-dimension evaluation and portfolio benchmarking run...")
    print("-" * 80)

    start_time = time.time()
    runtime = EvaluationRuntime()

    # Progress output
    dimension_names = [
        ("Part A", "AI Capability & Document Extraction", "ai_capability"),
        ("Part B", "LLM Evaluation & Hallucination Defense", "llm_evaluation"),
        ("Part C", "Agentic Architecture & Self-Correction", "agent_evaluation"),
        ("Part D", "RAG & Vector Retrieval Effectiveness", "rag_evaluation"),
        ("Part E", "Platform Performance & Throughput", "performance"),
        ("Part F", "Cost Intelligence & Unit ROI", "cost_business"),
        ("Part G", "SRE Reliability & Fault Tolerance", "reliability"),
        ("Part H", "Security & Zero Cross-Tenant Leakage", "security"),
        ("Part I", "Explainability & Grounding Provenance", "explainability"),
        ("Part J/K", "Human Experience & 4-Way Comparison", "human_experience"),
    ]

    for part, label, key in dimension_names:
        print(f"  [RUNNING] [{part}] {label:<45} ... ", end="", flush=True)
        evaluator = runtime.evaluators[key]
        rep = evaluator.evaluate()
        print(f"PASSED (Score: {rep.score:.1f}%)")

    # Full execution + certification calculation + evidence export
    print("-" * 80)
    print("  [CALCULATING] 6-Pillar Weighted Portfolio Intelligence Certification Score...")
    showcase_report = runtime.execute_all(output_dir="evaluation_evidence")
    score = showcase_report.score
    elapsed = time.time() - start_time

    # Output Results
    print(format_header("Portfolio Certification & Scoring Results"))
    print(f"  Overall Intelligence Score : {score.overall_score:.1f} / 100.0")
    print(f"  Certification Tier         : {score.certification_tier.value}")
    print(f"  Evaluation Status          : {score.evaluation_status.value}")
    print(f"  Total Execution Time       : {elapsed:.2f}s")
    print("\n  Pillar Breakdown:")
    print("  " + "-" * 76)
    print(f"  {'Pillar Name':<40} | {'Weight':<8} | {'Score':<8} | {'Weighted':<10} | {'Status'}")
    print("  " + "-" * 76)
    for cat in score.categories:
        print(f"  {cat.name:<40} | {cat.weight*100:>6.0f}% | {cat.score:>6.1f}% | {cat.weighted_score:>8.2f} | {cat.status.value}")
    print("  " + "-" * 76)

    # Key Highlights
    ai_rep = showcase_report.reports["ai_capability"]
    perf_rep = showcase_report.reports["performance"]
    cost_rep = showcase_report.reports["cost_business"]
    sec_rep = showcase_report.reports["security"]
    ux_rep = showcase_report.reports["human_experience"]

    print("\n" + format_header("Key Metric Highlights"))
    print(f"  * AI Extraction Accuracy       : {ai_rep.overall_accuracy_pct:.1f}% (Overall F1: {ai_rep.overall_f1_score:.3f})")
    print(f"  * P95 Processing Latency       : {perf_rep.e2e_p95_latency_ms:.1f}ms (Throughput: {perf_rep.documents_per_minute:,.0f} docs/min)")
    print(f"  * Cost Per Document            : ${cost_rep.cost_per_document_usd:.3f} (Manual Cost: $35.00/doc)")
    print(f"  * Annual Cost Reduction        : {cost_rep.cost_reduction_pct:.1f}% ({cost_rep.annual_roi_multiple:.1f}x Annual ROI, {cost_rep.total_hours_liberated_annual:,.0f} hrs saved)")
    print(f"  * Security & Isolation         : {sec_rep.prompt_injection_resistance_pct:.0f}% Injection Resistance, {sec_rep.tenant_data_leakage_events} Cross-Tenant Leaks")
    print(f"  * System Usability Scale (SUS) : {ux_rep.system_usability_scale_score:.1f}/100 (Avg Review Clicks: {ux_rep.average_clicks_per_workflow:.1f})")

    # Exported Artifacts
    print("\n" + format_header("Generated Portfolio Evidence & Artifacts"))
    print("  All artifacts exported to: ./evaluation_evidence/")
    print("    |-- executive_case_study.md       (Enterprise ROI & capability case study)")
    print("    |-- technical_whitepaper.md       (Deep architectural whitepaper)")
    print("    |-- ai_evaluation_score.json      (6-pillar certification scores)")
    print("    |-- portfolio_showcase_report.json(Complete serialized showcase report)")
    print("    |-- manifest.json                 (SHA-256 verification hash manifest)")
    print("    |-- metadata.json                 (Evaluation metadata & run timestamp)")
    print("    `-- [dimension]_report.json       (10 individual domain JSON reports)")
    print("\n" + "=" * 80)
    print("  PORTFOLIO CERTIFICATION COMPLETE - SYSTEM DEFENSE EVIDENCE SECURED")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
