# Feature Flags & Progressive Rollouts Guide

## 1. Concepts
Feature flags decouple code deployment from feature release:
- **Tenant Targeting**: Enable features for specific beta or enterprise tenants.
- **Percentage Rollout**: Deterministically enable features for a percentage of requests (e.g. 10%).
- **Emergency Kill Switch**: Disable any feature globally in milliseconds without code deployment.

## 2. Managing Feature Flags
```python
from app.infrastructure.deployment.features import FeatureRolloutManager, RolloutRule

mgr = FeatureRolloutManager()
flag = mgr.create_flag("new_ocr_layout_v2", name="New OCR Layout Engine", default_enabled=True)

# Target specific tenant and 20% of general traffic
flag.rules = [
    RolloutRule(target_tenants=["tenant-alpha"], percentage=100.0),
    RolloutRule(percentage=20.0),
]

# Check flag status
is_on = mgr.is_feature_enabled("new_ocr_layout_v2", tenant_id="tenant-beta", environment="prod")

# Activate emergency kill switch if needed
mgr.set_kill_switch("new_ocr_layout_v2", active=True)
```
