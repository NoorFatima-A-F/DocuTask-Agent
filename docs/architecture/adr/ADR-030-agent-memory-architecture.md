# ADR-030: Hierarchical 8-Tier Enterprise Memory Architecture

## Status
Accepted

## Context
Simple chat history buffers or single-vector databases are inadequate for complex enterprise multi-agent operations. Autonomous agents require separation between temporary working context, cross-session long-term memory, learned procedures, episodic case studies, domain knowledge, and tenant-wide organization conventions.

## Decision
We implement `EnterpriseMemoryPlatform` structured into 8 distinct memory tiers:
1. `Working Memory`: Current task/turn execution scope.
2. `Short-Term Memory`: Active session context.
3. `Long-Term Memory`: Durable cross-session storage.
4. `Semantic Memory`: Conceptual embeddings, facts, and entity relations.
5. `Procedural Memory`: Learned workflows, routines, and tool call patterns.
6. `Episodic Memory`: Historical case studies and past incident reflections.
7. `Knowledge Memory`: Enterprise reference documentation and knowledge bases.
8. `Organization Memory`: Tenant-wide policies, compliance conventions, and global rules.

The platform manages memory lifecycles (`NEW` -> `ACTIVE` -> `SUMMARIZED` -> `COMPRESSED` -> `ARCHIVED` -> `DELETED`), automated promotion/demotion, importance scoring, and TTL expiration.

## Consequences
- Clean separation of memory concerns prevents context pollution and token budget exhaustion.
- Enables multi-agent knowledge sharing within tenant boundaries while enforcing namespace isolation.
