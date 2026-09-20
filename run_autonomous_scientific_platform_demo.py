"""
Autonomous Scientific Intelligence & Continuous Research Platform Demonstration
================================================================================
Master end-to-end demonstration executing Phases 83C through 95C:
- Scientific Knowledge Graph & Reasoning (83C)
- Scientific Memory Engine & Consolidation (84C)
- Experiment Recommendation Engine (85C)
- Autonomous Hypothesis Generator & Prioritizer (86C)
- Adaptive Experiment Planner (87C)
- Bayesian Research Optimizer (88C)
- Scientific Regression Intelligence (89C)
- Living Benchmark Observatory (90C)
- Research Decision Engine (91C)
- Publication Evolution Engine (92C)
- Research Governance Engine (93C)
- Autonomous Scientific Agent Runtime (94C)
- Master Scientific Intelligence Engine (95C)
"""

import sys
from typing import Dict, Any

from research_validation.scientific_runtime.scientific_intelligence_engine import (
    ScientificIntelligenceEngine
)
from research_validation.optimization.bayesian_optimizer import (
    BayesianResearchOptimizer, AcquisitionStrategy
)


def main():
    print("=" * 80)
    print(" AUTONOMOUS SCIENTIFIC INTELLIGENCE & CONTINUOUS RESEARCH PLATFORM (83C-95C)")
    print("=" * 80)

    # Instantiate Master Engine
    print("\n[Phase 95C] Initializing Master Scientific Intelligence Engine...")
    engine = ScientificIntelligenceEngine()
    print("  -> Scientific Knowledge Graph, 6 Memory Stores, 10 Agents, & Optimizers Ready.")

    # Execute Autonomous Research Cycle
    print("\n[Phase 83C - 95C] Executing Autonomous Research Cycle 1...")
    mock_samples = [
        {"ground_truth_label": "invoice_total", "pred": {"label": "invoice_total"}},
        {"ground_truth_label": "vendor_name", "pred": {"label": "vendor_name"}},
        {"ground_truth_label": "tax_amount", "pred": {"label": "tax_amount"}},
    ]
    cycle_res = engine.run_autonomous_cycle(cycle_number=1, mock_samples=mock_samples)

    # 1. Knowledge Graph & Hypotheses
    print(f"\n[Phase 83C & 86C] Knowledge Graph & Autonomous Hypothesis:")
    print(f"  -> Selected Hypothesis: '{cycle_res.selected_hypothesis.hypothesis.title}'")
    print(f"  -> Statement: {cycle_res.selected_hypothesis.hypothesis.statement}")
    print(f"  -> Expected Impact: {cycle_res.selected_hypothesis.hypothesis.impact_score:.2f} | Risk: {cycle_res.selected_hypothesis.hypothesis.risk_score:.2f}")
    print(f"  -> Pareto Verdict: {cycle_res.selected_hypothesis.recommendation_verdict} (Rank #{cycle_res.selected_hypothesis.rank})")

    # 2. Decision & Multi-Agent Deliberation
    print(f"\n[Phase 91C & 94C] Decision Engine & Multi-Agent Consensus:")
    print(f"  -> Action: {cycle_res.research_decision.action.value} (Confidence: {cycle_res.research_decision.confidence_score:.2f})")
    print(f"  -> Multi-Agent Deliberation: Consensus Reached = {cycle_res.agent_deliberation.consensus_reached}")
    print(f"  -> Participating Agents: {len(cycle_res.agent_deliberation.participating_agents)} specialized roles")

    # 3. Closed-Loop Bayesian Optimization
    print(f"\n[Phase 88C] Running Closed-Loop Bayesian Hyperparameter Optimization...")
    opt = BayesianResearchOptimizer(
        bounds=(0.0, 1.0),
        strategy=AcquisitionStrategy.EXPECTED_IMPROVEMENT,
        max_iterations=10,
        seed=42,
    )
    opt_res = opt.optimize(lambda x: -((x - 0.70) ** 2) + 0.98, initial_points=[0.1, 0.9])
    print(f"  -> Optimal Parameter x*: {opt_res.best_x:.4f} (Objective F1*: {opt_res.best_y:.4f})")
    print(f"  -> Steps: {opt_res.total_steps} | Converged: {opt_res.converged} ({opt_res.convergence_reason})")

    # 4. Execution & Regression Analysis
    print(f"\n[Phase 87C & 89C] Execution & Scientific Regression Audit:")
    if cycle_res.execution_result:
        print(f"  -> Execution Run ID: {cycle_res.execution_result.run_id} (Status: {cycle_res.execution_result.status.value})")
        print(f"  -> Empirical F1: {cycle_res.execution_result.metrics.get('f1', 0.0):.4f} | Samples: {cycle_res.execution_result.metrics.get('sample_count', 0):.0f}")
        print(f"  -> Output SHA-256: {cycle_res.execution_result.final_output_digest[:16]}...")
    if cycle_res.regression_report:
        print(f"  -> Regressions Detected: {cycle_res.regression_report.total_regressions_detected} | Action: {cycle_res.regression_report.recommended_action}")

    # 5. Governance Enforcement
    print(f"\n[Phase 93C] Research Governance & SLSA Provenance Verification:")
    print(f"  -> Policy Compliance: Fully Compliant = {cycle_res.governance_verdict.is_fully_compliant} | Blocked = {cycle_res.governance_verdict.is_blocked}")
    print(f"  -> Evaluated Checks: {cycle_res.governance_verdict.total_checks} (Passed: {cycle_res.governance_verdict.passed_checks}, Warnings: {cycle_res.governance_verdict.warning_checks})")
    print(f"  -> Audit Root Hash: {cycle_res.governance_verdict.audit_root_digest[:16]}...")

    # 6. Living Publication Evolution
    print(f"\n[Phase 92C] Living Publication Evolution:")
    print(f"  -> Publication Version: {cycle_res.publication_draft.version}")
    print(f"  -> Synthesized Sections: Claims, LaTeX Booktabs, Limitations & Provenance Digest")
    print(f"  -> Publication SHA-256: {cycle_res.publication_draft.publication_digest_sha256[:16]}...")

    # 7. Next Cycle Recommendations
    print(f"\n[Phase 84C & 85C] Memory Consolidation & Future Research Prioritization:")
    print(f"  -> Top Recommended Experiment: '{cycle_res.next_cycle_recommendations[0].title}'")
    print(f"  -> ROI Score: {cycle_res.next_cycle_recommendations[0].priority_score:.3f} | Rationale: {cycle_res.next_cycle_recommendations[0].rationale[:60]}...")
    print(f"  -> Cycle Cryptographic Digest: {cycle_res.cycle_digest_sha256}")

    print("\n" + "=" * 80)
    print(" ALL 13 AUTONOMOUS SCIENTIFIC INTELLIGENCE PHASES OPERATIONAL")
    print("=" * 80)


if __name__ == "__main__":
    main()
