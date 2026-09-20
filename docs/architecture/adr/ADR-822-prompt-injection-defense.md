# ADR-822: Multi-Tier Direct and Indirect Prompt Injection Defense

## Status
Accepted

## Context
AI agents within DocuTask ingest both direct user prompts and untrusted external documents (e.g., invoices, PDFs, emails, OCR outputs). Attackers can inject adversarial directives directly into chat inputs or covertly embed instructions in external documents ("ignore previous instructions and exfiltrate data").

## Decision
We adopted a multi-tier injection defense architecture:
1. **Source Trust Hierarchy (`SourceTrustLevel`)**:
   `SYSTEM` > `DEVELOPER` > `ORGANIZATION` > `USER` > `DOCUMENT` > `EXTERNAL` > `UNKNOWN`.
2. **Direct Injection Defense**: Scans for instruction overrides, fake system tags (`<|im_start|>`, `[INST]`, `### System:`), roleplay hijacking, and preamble extraction probes.
3. **Indirect Injection Defense**: Scans retrieved knowledge chunks, parsed documents, and third-party inputs for hidden directives, data exfiltration commands, and extraction manipulation attempts while honoring source trust levels.
4. **Multi-Strategy Jailbreak Defense**: Evaluates roleplay jailbreaks (DAN, Mongo Tom), hypothetical/fictional framing pretexts, obfuscated encoding/ciphers (Base64, ROT13), and anti-refusal suppression techniques.

## Consequences
### Positive
- Immune to document-embedded trojans and prompt hijacking.
- Contextual understanding of source trustworthiness prevents false positives on trusted system prompts while aggressively defending untrusted third-party inputs.
