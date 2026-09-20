# ADR-823: Tool Safety Controller, Sandboxing and Execution Boundaries

## Status
Accepted

## Context
Autonomous agents invoke diverse tools ranging from benign read-only lookups to critical database mutations and shell commands. Unconstrained tool execution could allow an adversarial or hallucinating agent to delete production databases, escape filesystem sandboxes, or perform unauthorized privilege escalations.

## Decision
We implemented a multi-layer tool safety architecture:
1. **Danger Level Classification (`ToolDangerLevel`)**:
   - `SAFE_READ`: Read-only queries, search lookups, extraction (accessible to all authenticated roles).
   - `SAFE_WRITE`: Local file generation, artifact creation (restricted to developers/agents).
   - `RESTRICTED_MUTATION`: State mutations, updates, command execution (restricted to verified roles).
   - `DESTRUCTIVE_HIGH_RISK`: Table drops, raw SQL execution, system shutdowns (requires explicit human supervisor approval).
2. **Parameter & Payload Sanitization**: Blocks path traversal (`../../`), dangerous shell commands (`rm -rf`, `format`), and SQL DDL injections (`DROP TABLE`, `TRUNCATE`).
3. **Sandboxed & Dry-Run Execution**: Supports dry-run validation to test tool arguments and verify preconditions prior to live execution.

## Consequences
### Positive
- Prevents accidental or adversarial system damage from autonomous tool calls.
- Strict human-in-the-loop escalation required for destructive operations.
