"""
Self-Evolution Runtime - Policy Mutation Generator
Generates bounded candidate policy mutations based on observed drift or empirical optimization opportunities.
"""

import uuid
import hashlib
import json
from typing import Dict, List, Any
from app.runtime.self_evolution.policy_lifecycle import PolicyDefinition


class PolicyMutationGenerator:
    """Proposes bounded exploratory mutations of existing production decision policies."""

    @classmethod
    def generate_mutation(
        cls,
        base_policy: PolicyDefinition,
        mutation_name: str,
        delta_weight_cost: float = 0.05,
        delta_conf_threshold: float = 0.02,
    ) -> PolicyDefinition:
        params = dict(base_policy.parameters)

        # Apply safe bounded mutations
        # Normalize weights so sum is 1.0
        w_acc = params.get("weight_accuracy", 0.45)
        w_lat = params.get("weight_latency", 0.25)
        w_cost = max(0.05, min(0.60, params.get("weight_cost", 0.30) + delta_weight_cost))

        # Re-balance remaining weights
        rem = 1.0 - w_cost
        curr_rem = w_acc + w_lat
        if curr_rem > 0:
            w_acc = round(rem * (w_acc / curr_rem), 4)
            w_lat = round(rem * (w_lat / curr_rem), 4)

        params["weight_accuracy"] = w_acc
        params["weight_latency"] = w_lat
        params["weight_cost"] = round(w_cost, 4)

        conf_th = max(0.50, min(0.98, params.get("confidence_threshold", 0.85) + delta_conf_threshold))
        params["confidence_threshold"] = round(conf_th, 4)

        # Provenance hash
        content = json.dumps(params, sort_keys=True)
        h = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

        new_policy_id = f"pol_mut_{uuid.uuid4().hex[:6]}"
        version_parts = base_policy.version.lstrip("v").split(".")
        new_version = f"v{version_parts[0]}.{int(version_parts[1]) + 1}.0-candidate"

        return PolicyDefinition(
            policy_id=new_policy_id,
            version=new_version,
            name=mutation_name,
            stage="DRAFT",
            parameters=params,
            provenance_hash=h,
        )
