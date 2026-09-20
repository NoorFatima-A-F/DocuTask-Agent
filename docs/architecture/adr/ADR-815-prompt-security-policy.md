# ADR-815: Prompt Security Scanner & Static/Dynamic Vulnerability Analysis

## Status
Accepted

## Context
Prompts are vulnerable to adversarial jailbreak attempts, delimiter injection, system prompt extraction, and accidental hardcoded credential or secret leakage.

## Decision
We enforce mandatory static and dynamic security scanning:
- `PromptInjectionScanner`: Scans templates and runtime inputs for prompt injection phrases, jailbreaks (e.g. DAN, mode switches), and system override commands.
- `PromptLeakageScanner`: Scans templates for hardcoded API keys, database connection strings, passwords, and bearer tokens.
- `PromptSecurityValidator`: Combines injection and leakage scanners into a gatekeeper that runs automatically before prompt registration, version creation, and production deployment.

## Consequences
- **Positive**: Prevents injection and secret leaks before prompts reach production; guarantees enterprise security compliance.
- **Negative**: Adds scanning overhead during prompt creation and version updates.
