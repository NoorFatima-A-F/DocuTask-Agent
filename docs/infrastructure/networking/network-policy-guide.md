# Declarative Network Policy & Multi-Tenant Segmentation Guide

## 1. Network Policy Architecture
Policies define bidirectional traffic rules:
- **Ingress**: Controls inbound traffic allowed into target services.
- **Egress**: Controls outbound connections from internal services to external services.

## 2. Defining Declarative Ingress Rules
```python
from app.infrastructure.networking.policies import NetworkPolicy, NetworkPolicyRule, NetworkPolicyEngine, NetworkPolicyType
from app.infrastructure.networking.control_plane import ZeroTrustAction

engine = NetworkPolicyEngine()
policy = NetworkPolicy(
    policy_id="pol-isolated-tenant-finance",
    name="Finance Tenant Ingress Policy",
    target_service="*",
    namespace="tenant-finance-ns",
    policy_types=[NetworkPolicyType.INGRESS],
    ingress_rules=[
        NetworkPolicyRule(
            rule_id="r1",
            direction=NetworkPolicyType.INGRESS,
            allowed_namespaces=["tenant-finance-ns", "system-gateway"],
            allowed_ports=[8443],
            allowed_protocols=["https", "grpc"],
            action=ZeroTrustAction.ALLOW,
        )
    ]
)
engine.add_policy(policy)
```

## 3. Restricting Outbound Egress
```python
from app.infrastructure.networking.policies import EgressPolicyManager

egress_mgr = EgressPolicyManager(engine)
egress_mgr.allow_domain("api.openai.com")
assert egress_mgr.is_domain_allowed("api.openai.com") is True
```
