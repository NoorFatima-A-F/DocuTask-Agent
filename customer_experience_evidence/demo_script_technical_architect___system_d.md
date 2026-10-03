# Demo Script: Technical Architect / System Design Interviewer (30-Minute Deep Dive)

**Target Duration**: 30 Minutes

## Opening Hook
> "DocuTask is designed as a distributed, event-driven multi-agent cognitive architecture with deterministic execution guarantees and autonomous fault recovery."

## Key Talking Points
* Layered Architecture: Visual DAG Workflow Builder -> DAG Topological Validator -> Worker Fleet -> LLM Reasoning Agents -> Guardrail Middleware -> Storage.
* SRE & Reliability: Self-healing circuit breakers, MTTR < 2.2s, 100% automated fault recovery across chaos injection benchmarks.
* Evaluation Integrity: 10-dimension evaluation framework measuring faithfulness (99.4%), RAG MRR (0.945), and P95 latency (285ms).

## Live Demonstration Flow
* 1. Walk through the DAG validation algorithm (cycle detection & node reachability).
* 2. Inspect the FastAPI REST API contracts and domain models.
* 3. Run the CLI simulation and review the SHA-256 evidence manifest.
* 4. Discuss the multi-agent state persistence and memory retrieval architecture.

## Handling Objections & Technical Questions
**Q: Why not just use LangChain/LlamaIndex?**
*A: Off-the-shelf frameworks often introduce unnecessary abstractions, flaky async state, and poor observability. We engineered clean, decoupled domain interfaces with pure-Python synchronous runtime execution for deterministic testability and SRE reliability.*

## Closing Call to Action
> "I'd be glad to dive deeper into our state management, vector retrieval strategies, or horizontal autoscaling designs."
