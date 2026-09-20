# ADR-037: Enterprise AI Safety & Guardrails Runtime Layer

## Status
Accepted

## Context
Autonomous agents interact with user inputs, third-party documents, external web APIs, and tool parameters. Without active safety guardrails, agents are vulnerable to prompt injections, indirect prompt injections embedded in uploaded PDFs/emails, jailbreaks, PII leakage, and unauthorized tool execution.

## Decision
We implement `AISafetyLayer` providing defense-in-depth across the cognitive lifecycle:
1. `Input Scanning`: Regex and semantic pattern matching detecting direct prompt injections, jailbreak instructions, and roleplay bypasses.
2. `Indirect Injection Defense`: Sanitizing untrusted document content retrieved from external sources.
3. `PII & Secret Protection`: Automated detection and masking of emails, phone numbers, SSNs, and API keys (`[REDACTED_EMAIL]`, `[REDACTED_SECRET]`).
4. `Output Validation`: Verifying that generated text does not contain leaked credentials or prohibited responses.

## Consequences
- Protects agents from malicious external manipulation.
- Prevents accidental leakage of confidential employee, customer, or financial data.
