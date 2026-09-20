# Enterprise Planning Contracts & Graph Representation — Architecture & Implementation Review Report (Prompt 16.0)

**Target System**: Planning Subsystem (`app/agents/planning/`)  
**Target Path**: `C:\Users\User\Desktop\ai_document_processing_platform\app\agents\planning\`  
**Design Standard**: Enterprise Clean Architecture, Domain-Driven Design, Pydantic v2, SOLID, DAG Theory  
**Hackathon Target**: Google Cloud All Things Agentic Hackathon & Global Enterprise Production  

---

## Executive Summary

The **Enterprise Planning Contracts & Graph Representation Foundation (Prompt 16.0)** has been designed and implemented under `app/agents/planning/`. This subsystem defines the canonical planning representation consumed by Executors, Workflow Engines, Observers, Reflection Engines, Recovery Engines, and Multi-Agent Coordinators.

This phase strictly defines **what a plan is**—establishing a provider-independent planning model, DAG graph topology, cycle detection, topological sorting, workflow execution branching, dry-run simulation, and deterministic state snapshots.

---

## 1. Planning Architectural Mermaid Diagrams

### 1. Planning Layer Architecture Diagram

```mermaid
graph TD
    subgraph "Reasoning Producers"
        INTELLIGENT_PLANNER["Intelligent Planner / LLM Decomposition (Prompt 17.0)"]
    end

    subgraph "Canonical Planning Model (app.agents.planning)"
        PLAN["Plan Aggregate (Domain Entity)"]
        GRAPH["PlanGraph (DAG Topology)"]
        NODES["PlanNodes (Task, Join, Split, Merge, Barrier, Checkpoint, Approval)"]
        EDGES["PlanEdges (Sequential, Conditional, Dependency, Fallback, Rollback)"]
        STATS["PlanStatistics & Cost Estimates"]
    end

    subgraph "Runtime Consumers"
        EXECUTOR["Execution Engine"]
        WORKFLOW["Workflow Engine"]
        OBSERVER["Observation & Monitoring Engine"]
        RECOVERY["Recovery & Compensation Engine"]
        REFLECTION["Reflection & Learning Engine"]
    end

    INTELLIGENT_PLANNER -->|Generates| PLAN
    PLAN *-- GRAPH
    PLAN *-- STATS
    GRAPH *-- NODES
    GRAPH *-- EDGES
    PLAN -->|Consumed by| EXECUTOR
    PLAN -->|Orchestrated by| WORKFLOW
    PLAN -->|Monitored by| OBSERVER
    PLAN -->|Replayed by| RECOVERY
    PLAN -->|Inspected by| REFLECTION
```

### 2. Plan Hierarchy Diagram

```mermaid
classDiagram
    class Plan {
        +PlanIdentity identity
        +string name
        +PlanLifecycleState lifecycle_state
        +PlanGraph graph
        +PlanMetadata metadata
        +PlanStatistics statistics
        +List~Dependency~ dependencies
        +List~PlanConstraint~ constraints
        +List~ResourceRequirement~ resource_requirements
        +PlanRiskAssessment risk_assessment
        +PlanSnapshot snapshot
    }

    class PlanIdentity {
        +UUID plan_id
        +string goal_id
        +string workflow_id
        +string correlation_id
        +string tenant_id
    }

    class PlanStatistics {
        +int total_nodes_count
        +int total_edges_count
        +float estimated_duration_seconds
        +float estimated_cost_usd
        +int estimated_tokens
    }

    Plan *-- PlanIdentity
    Plan *-- PlanStatistics
```

### 3. Task Graph Diagram

```mermaid
graph LR
    ENTRY["Entry: START_NODE"] --> OCR["Task: OCR_EXTRACTION"]
    OCR --> SPLIT{"Split Node"}
    SPLIT --> ENTITY["Task: ENTITY_EXTRACTION"]
    SPLIT --> TABLE["Task: TABLE_PARSING"]
    ENTITY --> JOIN["Join Node"]
    TABLE --> JOIN
    JOIN --> GATE["Approval Gate: CHECK_TOTALS"]
    GATE --> VALIDATE["Task: RULE_VALIDATION"]
    VALIDATE --> EXIT["Exit: END_NODE"]
```

### 4. DAG Structure & Topological Sorting Diagram

```mermaid
graph TD
    A["Node A (In-Degree: 0)"] --> B["Node B (In-Degree: 1)"]
    A --> C["Node C (In-Degree: 1)"]
    B --> D["Node D (In-Degree: 2)"]
    C --> D
    D --> E["Node E (In-Degree: 1)"]

    subgraph "Topological Execution Order (Kahn's Algorithm)"
        ORDER["A -> B -> C -> D -> E"]
    end
```

### 5. Workflow Model Diagram

```mermaid
classDiagram
    class WorkflowDefinition {
        +string workflow_id
        +string name
        +PlanGraph graph
        +List~ParallelBranch~ parallel_branches
        +List~ConditionalBranch~ conditional_branches
        +float timeout_seconds
    }

    class ConditionalBranch {
        +string branch_id
        +BranchCondition condition
        +string target_node_id
        +string fallback_node_id
    }

    class ParallelBranch {
        +string branch_id
        +List~string~ concurrent_node_ids
        +string join_node_id
    }

    WorkflowDefinition *-- ConditionalBranch
    WorkflowDefinition *-- ParallelBranch
```

### 6. Dependency Graph Diagram

```mermaid
graph LR
    T1["Task 1: Preprocess"] -->|Hard Dependency| T2["Task 2: Segment Image"]
    T2 -->|Data Dependency| T3["Task 3: OCR Text"]
    T3 -->|Temporal Dependency| T4["Task 4: Post-Process"]
```

### 7. Scheduling & Timeline Flow Diagram

```mermaid
gantt
    title Plan Execution Timeline & Schedule Windows
    dateFormat  X
    axisFormat %s sec

    section Pipeline Tasks
    OCR Extraction (Node 1)       :active, 0, 10
    LLM Schema Extraction (Node 2): 10, 25
    Rule & Policy Validation (Node 3): 25, 30
```

### 8. Validation Flow Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Builder as PlanBuilder
    participant Val as PlanValidator
    participant DAG as DAGValidator
    participant Res as GraphValidationResult

    Builder->>Val: validate_plan(Plan)
    Val->>DAG: detect_cycles(PlanGraph)
    alt Cycles Detected
        DAG-->>Val: raise CyclicDependencyException
        Val-->>Builder: return GraphValidationResult (Invalid, Error)
    else Acyclic & Valid
        DAG-->>Val: Pass
        Val-->>Builder: return GraphValidationResult (Valid)
    end
```

### 9. Planning Lifecycle State Machine Diagram

```mermaid
stateDiagram-v2
    [*] --> DRAFT
    DRAFT --> VALIDATED : PlanValidator.validate()
    VALIDATED --> OPTIMIZED : OptimizationEngine.optimize()
    OPTIMIZED --> APPROVED : ApprovalGate.approve()
    VALIDATED --> REJECTED : Governance / Risk Failure
    APPROVED --> EXECUTING : ExecutionEngine.start()
    EXECUTING --> COMPLETED : All Tasks Succeeded
    EXECUTING --> FAILED : Unrecoverable Error
    EXECUTING --> CANCELLED : Aborted by User/System
    COMPLETED --> ARCHIVED : Retention Policy
    FAILED --> ARCHIVED : Retention Policy
```

### 10. Complete Class Diagram

```mermaid
classDiagram
    class PlanManager {
        +IPlanRepository repository
        +IPlanValidator validator
        +PlanCache cache
        +register_plan(plan) Plan
        +get_plan(plan_id) Plan
    }

    class PlanGraph {
        +string graph_id
        +Dict~str, PlanNode~ nodes
        +List~PlanEdge~ edges
        +get_node(id) PlanNode
        +get_outgoing_edges(id) List~PlanEdge~
    }

    class DAGValidator {
        +detect_cycles(graph)
        +topological_sort(graph) List~str~
    }

    class PlanningSimulation {
        +simulate(plan) SimulationResult
    }

    PlanManager *-- PlanGraph
    PlanManager ..> DAGValidator
    PlanManager ..> PlanningSimulation
```

---

## 2. Google Cloud Readiness Assessment

| Google Cloud Service | Integration / Compatibility Pattern | Status |
| :--- | :--- | :--- |
| **Cloud Run** | Stateless DAG execution and plan validation APIs | Fully Compatible |
| **Cloud Tasks** | Serializable `Plan` payloads for distributed asynchronous task execution | Fully Compatible |
| **Cloud Pub/Sub** | Pub/Sub domain events (`PlanCreatedEvent`, `PlanApprovedEvent`, `PlanExecutedEvent`) | Fully Compatible |
| **Cloud SQL / AlloyDB AI** | PlanRepository and PlanSnapshot persistence | Fully Compatible |
| **Vertex AI** | Embedding vectors and future LLM decomposition integration | Fully Compatible |
| **Cloud Monitoring & Logging** | Structured plan metrics and execution timeline traces | Fully Compatible |
| **OpenTelemetry & Cloud Trace** | PlanCorrelation and W3C trace context propagation | Fully Compatible |

---

## 3. Phase Readiness Assessment

The Planning Foundation is **100% Ready for Prompt 17.0 (Intelligent Planner Implementation)**:
- Graph models, cycle detection, topological sorting, and serialization contracts are completely established.
- The future Intelligent Planner can generate `Plan` objects without needing to define graph or validation infrastructure.
