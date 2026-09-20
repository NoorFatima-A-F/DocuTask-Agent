# Phase 25.0 — Autonomous Planning Engine Validation Report

## 1. Objective & Scope

The Autonomous Planning Engine translates a `GoalSpecification` into a concrete, resilient `ExecutionPlan`. It decouples high-level intent from implementation details by performing capability discovery, topological decomposition, agent allocation, tool assignment, and fallback branch formulation.

---

## 2. Planning Architecture

```
GoalSpecification
      │
      ▼
TaskDecomposer ───> [t1: OCR] ───> [t2: Extract] ───> [t3: Validate] ───> [t4: Audit]
      │                   │                 │                  │                   │
      ▼                   ▼                 ▼                  ▼                   ▼
CapabilityDiscovery ──> agent_ocr      agent_extract     agent_validate       agent_audit
      │                   │                 │                  │                   │
      ▼                   ▼                 ▼                  ▼                   ▼
FallbackSynthesis ────> FallbackTool     FallbackAgent     ReflectionRepair    Escalation
```

### 2.1 Multi-Factor Capability Discovery
Agents and tools are matched using multi-attribute Pareto ranking:
$$\text{Score}(A) = 60 \cdot \text{Accuracy} + 20 \cdot \min\left(1.0, \frac{C_{\text{base}}}{C_A}\right) + 20 \cdot \min\left(1.0, \frac{L_{\text{base}}}{L_A}\right)$$
- If high accuracy ($A \ge 0.95$) is requested, reliability ratings take precedence over execution costs.
- If cost-sensitive budgets are set, sub-millisecond deterministic engines are selected.

### 2.2 Dynamic Task Decomposition
The `TaskDecomposer` generates domain-specific pipelines:
- **Invoice / Receipt:** `ocr` $\to$ `entity_extraction` $\to$ `arithmetic_verification` $\to$ `regulatory_audit`.
- **Compliance Audit:** `ocr` $\to$ `clause_extraction` $\to$ `regulatory_audit`.
- **Contract Review:** `ocr` $\to$ `clause_extraction` $\to$ `risk_assessment`.
- **Fraud Detection:** `ocr` $\to$ `tamper_analysis` $\to$ `fraud_scoring`.
- **Human Review Enforcement:** Automatically appends `human_review` node if mandated by constraints.

### 2.3 Topological Invariants & Fallback Formulation
- Enforces strict DAG properties ($V, E$) using Kahn's algorithm. Cycle detection triggers immediate `ValueError` prevention.
- Synthesizes up-front fallback strategies (`SWITCH_TOOL`, `SWITCH_AGENT`, `INJECT_REPAIR_NODE`) attached to critical tasks.

---

## 3. Verification Evidence

- **Unit & Property Tests:** 56 passing tests in `tests/agents/intelligence/test_autonomous_planner.py`.
- **Topological Sorting:** Tested against linear graphs, parallel multi-branch graphs, and complex 20-node deep DAGs.
- **Cycle Prevention:** 1-node self-cycles and 3-node cyclic dependencies correctly rejected.
- **Cost & Duration Estimation:** Real-time summation of agent $p_{95}$ latencies and tool invocation costs.
