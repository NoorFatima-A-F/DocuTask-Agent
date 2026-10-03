# Golden Baseline Governance & Policy Regression Detection

## Overview
Golden Baselines represent certified release states against which subsequent platform changes are compared to prevent silent quality or security degradation.

## Governance Workflow

1. **Baseline Creation**:
   - Captures exact file hashes of engine source files.
   - Snapshots active policy definitions (minimum EQI, required domains, forbidden critical findings).
   - Generates `GoldenBaselineManifest`.

2. **Regression Detection (`PolicyRegressionDetector`)**:
   - Asserts that proposed policy changes never lower the minimum EQI score.
   - Asserts that required evidence domains are never deleted without explicit board approval.
   - Flags any attempt to disable `forbidden_critical_findings`.
   - Prevents unbacked claims threshold increases.

3. **CLI Operations**:
   ```bash
   python -m enterprise_audit_engine.cli.main compare-baseline --repo-root . --current-report release_audit/verification_certificate.json
   ```
