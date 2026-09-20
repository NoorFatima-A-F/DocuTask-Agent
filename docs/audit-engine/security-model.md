# Audit Engine Defensive Security Model

## 1. Threat Model & Design Goals
The audit engine executes across untrusted codebases, PRs, and external contributions. It must resist:
1. **Malicious Artifact Payloads**: Attempted arbitrary code execution during evidence extraction.
2. **Directory Traversal**: Path traversal attacks attempting to read or overwrite system files outside `repo_root`.
3. **Unsafe Serialization**: Remote code execution via unsafe deserializers.
4. **Command Injection**: Subprocess shell injection attacks.

## 2. Guardrails & Hardening

| Vector | Mitigation Enforced |
| :--- | :--- |
| Deserialization | `json.loads` strictly enforced; `pickle` prohibited across engine codebase. |
| Subprocess Calls | `subprocess.run(..., shell=False, timeout=N)` mandatory. |
| Artifact Storage | Max artifact limit 50MB per collector output. |
| Dynamic Eval | `eval()` and `exec()` disallowed in audit evaluation logic. |
| Path Traversal | Canonical `.resolve()` paths bounded strictly within repository root. |

## 3. Automated Self-Audit
The `EngineSecurityValidator` runs during every certification cycle:
```bash
python -m enterprise_audit_engine.cli.main enterprise-certify
```
If any pattern violation is discovered in the audit engine, certification is rejected with exit code 1.
