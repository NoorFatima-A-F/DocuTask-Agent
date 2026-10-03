# Plugin Development Guide

All plugins must implement `VerificationPluginInterface` and provide:
1. `plugin_name` (unique string)
2. `capabilities` (list of strings)
3. `execute_verification(definition, env_profile, dataset)` returning `{"metrics": [...], "raw_evidence": {...}}`.
4. Sandboxed execution with zero core platform mutation.
