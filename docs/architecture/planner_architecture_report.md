# Enterprise Intelligent Planner & Hierarchical Task Decomposition Engine — Architecture & Implementation Review Report (Prompt 17.0)

**Target System**: Cognitive Planning Subsystem (`app/agents/planner/`)  
**Target Path**: `C:\Users\User\Desktop\ai_document_processing_platform\app\agents\planner\`  
**Design Standard**: Enterprise Clean Architecture, Domain-Driven Design, Pydantic v2, SOLID, Cognitive AI Planning  
**Hackathon Target**: Google Cloud All Things Agentic Hackathon & Global Enterprise Production  

---

## Executive Summary

The **Enterprise Intelligent Planner & Hierarchical Task Decomposition Engine (Prompt 17.0)** has been implemented under `app/agents/planner/`.

This subsystem serves as the **cognitive brain** of the autonomous agent platform:
- Converts high-level **Goals** into optimized, validated, executable **PlanGraphs**.
- **NEVER executes tasks** (delegates to Execution Engine).
- **NEVER contains hardcoded business rules** (delegates governance to Decision Engine).
- **NEVER directly accesses LLM provider APIs or concrete SDKs** (communicates via `ILLMPlanningAdapter`).
- **NEVER mutates memory** (consumes historical plans in read-only mode via `PlannerMemoryAdapter`).

---

## 1. Planner Architectural Mermaid Diagrams

### 1. Planning Pipeline Diagram

```mermaid
graph TD
    GOAL["User Goal / Task Request"] --> ANALYZE["1. Goal Analysis (GoalAnalyzer)"]
    ANALYZE --> DECOMPOSE["2. Hierarchical Decomposition (HierarchicalTaskDecomposer)"]
    DECOMPOSE --> CANDIDATES["3. Multi-Candidate Generation (CandidatePlanGenerator)"]
    CANDIDATES --> EVAL["4. Evaluation & Scoring (CandidateEvaluator)"]
    EVAL --> RANK["5. Ranking & Selection (PlanRanker)"]
    RANK --> OPTIMIZE["6. Plan Optimization (PlanOptimizer)"]
    OPTIMIZE --> REFLECT["7. Reflection & Self-Critique (PlannerReflectionEngine)"]
    REFLECT -->|Flaws Detected| REPAIR["8. Incremental Repair (PlanRepairEngine)"]
    REFLECT -->|Flawless| VALIDATE["9. Structural Validation (PlannerPlanValidator)"]
    REPAIR --> VALIDATE
    VALIDATE --> RESULT["10. Validated PlanningResult (PlanGraph)"]
```

### 2. Planner Lifecycle State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> INITIALIZING
    INITIALIZING --> ANALYZING_GOAL : parse_goal()
    ANALYZING_GOAL --> DECOMPOSING : decompose_goal()
    DECOMPOSING --> GENERATING_CANDIDATES : generate_candidates()
    GENERATING_CANDIDATES --> OPTIMIZING : optimize_plan()
    OPTIMIZING --> REFLECTING : critique_plan()
    REFLECTING --> REPAIRING : flaws_detected
    REFLECTING --> FINALIZING : no_flaws
    REPAIRING --> FINALIZING : repair_completed
    FINALIZING --> COMPLETED : validate_success
    FINALIZING --> FAILED : validation_error
```

### 3. Hierarchical Decomposition Tree Diagram

```mermaid
graph TD
    GOAL["Strategic Goal: Process Invoices"] --> OBJ1["Objective 1: Ingest & Extract Text"]
    GOAL --> OBJ2["Objective 2: Parse Structured Fields"]
    GOAL --> OBJ3["Objective 3: Enforce Compliance"]

    OBJ1 --> MILE1["Milestone 1: OCR Readiness"]
    MILE1 --> TASK1["Atomic Task 1: Tesseract / Vision OCR"]

    OBJ2 --> MILE2["Milestone 2: LLM Schema Extraction"]
    MILE2 --> TASK2["Atomic Task 2: Extract Totals & Line Items"]

    OBJ3 --> MILE3["Milestone 3: Decision Engine Clearance"]
    MILE3 --> TASK3["Atomic Task 3: Policy & Budget Check"]
```

### 4. Candidate Plan Ranking & Beam Search Diagram

```mermaid
graph LR
    GOAL["Planner Request"] --> C1["Candidate 1: Hierarchical (Cost: $0.55, Dur: 17s, Conf: 0.95)"]
    GOAL --> C2["Candidate 2: Least Cost (Cost: $0.40, Dur: 25s, Conf: 0.85)"]
    GOAL --> C3["Candidate 3: Fast Parallel (Cost: $0.70, Dur: 10s, Conf: 0.92)"]

    C1 --> SCORER["PlanCandidateScorer & PlanRanker"]
    C2 --> SCORER
    C3 --> SCORER

    SCORER --> WINNER["Winning Plan: Candidate 1 (Score: 0.92)"]
```

### 5. Self-Reflection & Critique Flow Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Pipeline as PlanningPipeline
    participant Reflector as PlannerReflectionEngine
    participant Repairer as PlanRepairEngine

    Pipeline->>Reflector: critique_plan(Plan)
    Reflector->>Reflector: check_cycles()
    Reflector->>Reflector: check_isolated_nodes()
    Reflector->>Reflector: check_unreachable_prerequisites()
    alt Flaws Detected
        Reflector-->>Pipeline: return ReflectionCritique(has_flaws=True, repairs)
        Pipeline->>Repairer: repair_plan(Plan, critique)
        Repairer-->>Pipeline: return Repaired Plan
    else No Flaws
        Reflector-->>Pipeline: return ReflectionCritique(has_flaws=False)
    end
```

### 6. Incremental Plan Repair Diagram

```mermaid
graph TD
    FLAWED["Flawed Plan Graph: Isolated Nodes [N1] [N2]"] --> CRITIQUE["Reflection Critique: Suggests LINK_SEQUENTIAL_EDGES"]
    CRITIQUE --> REPAIR["PlanRepairEngine.repair_plan()"]
    REPAIR --> REPAIRED["Repaired Plan Graph: [N1] ── Sequential Edge ──> [N2]"]
```

### 7. Multi-Objective Plan Optimization Diagram

```mermaid
graph LR
    PLAN["Draft Plan Graph"] --> OPT["PlanOptimizer"]
    OPT --> COST["Refine Cost Estimates (-5%)"]
    OPT --> TIME["Compress Critical Path Duration (-10%)"]
    OPT --> PARALLEL["Parallelize Independent Subtasks"]
    COST --> OPTIMIZED["Optimized Plan Aggregate"]
    TIME --> OPTIMIZED
    PARALLEL --> OPTIMIZED
```

### 8. Strategy Selection Matrix Diagram

```mermaid
graph TD
    REQ["PlannerRequest Context"] --> SELECTOR["Planning Strategy Selector"]
    SELECTOR -->|Complex Goal| HIERARCHICAL["Hierarchical Planning"]
    SELECTOR -->|Tight Budget| LEAST_COST["Least-Cost Planning"]
    SELECTOR -->|Fast Latency| PARALLEL["Parallel Planning"]
    SELECTOR -->|Ambiguous Goal| LLM_GUIDED["LLM-Guided Planning"]
```

### 9. LLM Adapter Provider Decoupling Diagram

```mermaid
classDiagram
    class ILLMPlanningAdapter {
        <<abstract>>
        +generate_decomposition(prompt)* Dict
        +rank_candidates(prompt)* List~float~
    }

    class MockLLMPlanningAdapter {
        +generate_decomposition(prompt) Dict
        +rank_candidates(prompt) List~float~
    }

    class VertexAIGeminiPlanningAdapter {
        +generate_decomposition(prompt) Dict
        +rank_candidates(prompt) List~float~
    }

    ILLMPlanningAdapter <|-- MockLLMPlanningAdapter
    ILLMPlanningAdapter <|-- VertexAIGeminiPlanningAdapter
```

### 10. Read-Only Memory Integration Diagram

```mermaid
graph LR
    PLANNER["Intelligent Planner"] -->|1. search(historical_goal)| MEM_ADAPTER["PlannerMemoryAdapter"]
    MEM_ADAPTER -->|2. search(query, top_k)| MEM_MGR["MemoryManager (Read-Only)"]
    MEM_MGR -->>PLANNER: 3. Return Past Successful Workflows & Statistics
```

### 11. Decision Engine Governance Integration Diagram

```mermaid
graph LR
    PLANNER["Intelligent Planner"] -->|1. evaluate_plan_feasibility(estimated_cost)| DEC_ADAPTER["PlannerDecisionAdapter"]
    DEC_ADAPTER -->|2. evaluate(DecisionContext)| DEC_ENG["DecisionEngine (Authority)"]
    DEC_ENG -->>PLANNER: 3. Return DecisionResult (Approval & Risk Score)
```

### 12. Complete Class Diagram

```mermaid
classDiagram
    class IntelligentPlanner {
        +PlanningEngine engine
        +PlannerPlanValidator validator
        +plan(request) PlanningResult
    }

    class PlanningPipeline {
        +GoalAnalyzer goal_analyzer
        +CandidatePlanGenerator candidate_generator
        +PlanRanker plan_ranker
        +PlanOptimizer plan_optimizer
        +PlannerReflectionEngine reflection_engine
        +PlanRepairEngine repair_engine
        +execute_pipeline(request) Plan
    }

    class HierarchicalTaskDecomposer {
        +decompose_goal(goal) DecompositionTree
    }

    IntelligentPlanner *-- PlanningPipeline
    PlanningPipeline *-- HierarchicalTaskDecomposer
```

---

## 2. Google Cloud Readiness Assessment

| Google Cloud Service | Integration / Compatibility Pattern | Status |
| :--- | :--- | :--- |
| **Cloud Run** | Stateless cognitive planning execution | Fully Compatible |
| **Vertex AI / Gemini** | Decoupled via `ILLMPlanningAdapter` without direct SDK imports | Fully Compatible |
| **Cloud Tasks** | Serializable `PlannerRequest` and `PlanningResult` payloads | Fully Compatible |
| **Cloud Pub/Sub** | Pub/Sub domain events (`PlanningStarted`, `PlanGenerated`, `PlanRepaired`) | Fully Compatible |
| **Cloud SQL / AlloyDB AI** | PlannerRepository and candidate plan caching | Fully Compatible |
| **Secret Manager** | Security credential isolation | Fully Compatible |
| **Cloud Monitoring & Logging** | Structured planning metrics and trace logs | Fully Compatible |
| **OpenTelemetry & Cloud Trace** | PlanningTrace W3C trace context propagation | Fully Compatible |

---

## 3. Phase Readiness Assessment

The Intelligent Planner is **100% Ready for Phase 18.0 (Execution Engine & Stateful Task Dispatcher)**:
- Output plans strictly conform to the `Plan` aggregate and `PlanGraph` DAG contracts.
- The Execution Engine can consume `Plan` objects without needing to understand how they were cognitively synthesized.
