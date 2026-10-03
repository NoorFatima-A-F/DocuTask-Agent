# Phase 25.0 — 4-Tier Memory Intelligence Engine Report

## 1. Objective & Scope

The 4-Tier Memory System provides differentiated memory retention and retrieval for autonomous agents, ensuring immediate variables, session context, past historical episodes, and permanent domain facts are segregated yet accessible via a unified multi-factor ranking formula.

---

## 2. Architectural Tiers

```
┌─────────────────────────────────────────────────────────────┐
│                       4-Tier Memory                         │
├──────────────────────┬──────────────────────────────────────┤
│ Tier 1: Short-Term   │ Volatile scratchpad, tokens, TTL     │
├──────────────────────┼──────────────────────────────────────┤
│ Tier 2: Working      │ Active session, goal/task pointers   │
├──────────────────────┼──────────────────────────────────────┤
│ Tier 3: Episodic     │ Run histories, past corrections      │
├──────────────────────┼──────────────────────────────────────┤
│ Tier 4: Semantic     │ Permanent facts, schemas, vendor IDs │
└──────────────────────┴──────────────────────────────────────┘
```

### 2.1 Tier 1: Short-Term Memory (`ShortTermMemory`)
- Ephemeral in-memory key-value scratchpad for transient step outputs and token buffers.
- Features configurable capacity with LRU eviction and TTL expirations.

### 2.2 Tier 2: Working Memory (`WorkingMemory`)
- Maintains current active goal state, DAG task pointers, accumulated entity findings, and runtime error logs for an active session.

### 2.3 Tier 3: Episodic Memory (`EpisodicMemory`)
- Stores complete episode records (`EpisodeRecord`) encompassing goal description, task name, agent used, outcome (`SUCCESS`, `FAILURE`, `RECOVERED`), and reflection notes.
- Enables autonomous agents to learn from past trajectories and avoid repeating past errors.

### 2.4 Tier 4: Semantic Memory (`SemanticMemory`)
- Long-term declarative knowledge store holding `SemanticFact` objects across domains (Financial, Compliance, Tax, Legal).
- Seeded with baseline enterprise rules (e.g. `subtotal + tax = total`, SOX 7-year retention).

---

## 3. Multi-Factor Retrieval Scoring Formula

Memory search in Episodic and Semantic tiers uses a unified relevance score:

$$\text{Score} = w_1 \cdot \text{Similarity} + w_2 \cdot \text{Importance} + w_3 \cdot \text{Recency} + w_4 \cdot \text{TaskRelevance}$$

Where:
- $w_1 = 0.35$ (Jaccard token overlap between query terms and memory content)
- $w_2 = 0.25$ (Normalized importance $[0.0, 1.0]$)
- $w_3 = 0.20$ (Exponential recency decay: $\exp(-\lambda \cdot \Delta t)$)
- $w_4 = 0.20$ (Task tag overlap ratio $[0.0, 1.0]$)

---

## 4. Verification Evidence

- **Tests:** 45 passing unit tests in `tests/agents/intelligence/test_memory_intelligence.py`.
- **Cross-Tier Promotion:** Verified `finalize_and_learn` promoting working memory findings into Episodic and Semantic memory tiers.
- **Context Bundle Assembly:** Verified unified bundle generation containing working context, top episodic matches, and top semantic facts.
