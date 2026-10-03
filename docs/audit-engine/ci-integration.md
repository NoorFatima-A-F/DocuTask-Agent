# CI/CD Integration & Automated Verification Gates

## GitHub Actions Workflow (`.github/workflows/audit.yml`)

The Enterprise Audit Engine integrates into GitHub Actions to execute on every push and Pull Request to `main`.

```yaml
name: Automated Evidence Audit

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

permissions:
  contents: read

jobs:
  evidence-audit:
    name: Run Enterprise Evidence Collectors
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Execute Evidence Verification Platform
        run: |
          python -m enterprise_audit_engine.cli.main run-all --repo-root . --output-dir audit_output

      - name: Enforce Release Gate
        run: |
          python -m enterprise_audit_engine.cli.main verify-gate --repo-root .

      - name: Archive Audit Evidence & Reports
        uses: actions/upload-artifact@v4
        with:
          name: audit-artifacts
          path: audit_output/
```
