"""
Evidence Graph & Lineage Query Engine.
Traverses and proves the complete provenance chain:
Objective -> Definition -> Plan -> DatasetVersion -> ConfigSnapshot -> EnvSnapshot -> Execution -> Evidence -> Metrics -> QualityDecision -> Certification -> Audit
"""
from typing import Any, Dict, List, Optional
from app.platform_verification.domain_model.persistence.repositories.in_memory_repos import verification_domain_repository


class EvidenceGraphEngine:
    def __init__(self, repo=verification_domain_repository):
        self.repo = repo

    def build_provenance_chain(self, certification_id: str) -> Dict[str, Any]:
        cert = self.repo.get_certification(certification_id)
        if not cert:
            raise ValueError(f"Certification '{certification_id}' not found.")

        execution = self.repo.get_execution(cert.execution_id)
        if not execution:
            raise ValueError(f"Execution '{cert.execution_id}' not found.")

        definition = self.repo.get_definition(execution.verification_definition_id)
        plan = self.repo.get_plan(execution.plan_id)
        dver = self.repo.get_dataset_version(execution.dataset_version_id)
        env_snap = self.repo.environment_snapshots.get(execution.environment_snapshot_id)
        cfg_snap = self.repo.configuration_snapshots.get(execution.configuration_snapshot_id)
        evidence = self.repo.get_evidence_for_execution(execution.execution_id)
        metrics = self.repo.get_metrics_for_execution(execution.execution_id)
        decisions = self.repo.quality_decisions.get(execution.execution_id, [])

        return {
            "certification": {
                "certification_id": cert.certification_id,
                "level": cert.level.value if hasattr(cert.level, 'value') else cert.level,
                "composite_quality_score": cert.composite_quality_score,
                "evidence_bundle_hash": cert.evidence_bundle_hash,
                "approved_by": cert.approved_by,
                "issued_at": cert.issued_at
            },
            "verification_definition": {
                "definition_id": definition.definition_id if definition else None,
                "name": definition.name if definition else None,
                "objective": definition.objective if definition else None,
                "category": definition.category.value if (definition and hasattr(definition.category, 'value')) else None
            },
            "verification_plan": {
                "plan_id": plan.plan_id if plan else None,
                "execution_strategy": plan.execution_strategy.value if (plan and hasattr(plan.execution_strategy, 'value')) else None
            },
            "dataset_version": {
                "dataset_version_id": dver.dataset_version_id if dver else None,
                "checksum_sha256": dver.checksum_sha256 if dver else None,
                "item_count": dver.item_count if dver else None
            },
            "configuration_snapshot": {
                "snapshot_id": cfg_snap.snapshot_id if cfg_snap else None,
                "canonical_hash_sha256": cfg_snap.canonical_hash_sha256 if cfg_snap else None
            },
            "environment_snapshot": {
                "snapshot_id": env_snap.snapshot_id if env_snap else None,
                "tier": env_snap.tier.value if (env_snap and hasattr(env_snap.tier, 'value')) else None,
                "git_commit_sha": env_snap.git_commit_sha if env_snap else None
            },
            "execution": {
                "execution_id": execution.execution_id,
                "status": execution.status.value if hasattr(execution.status, 'value') else execution.status,
                "duration_ms": execution.duration_ms,
                "started_at": execution.started_at,
                "completed_at": execution.completed_at
            },
            "evidence_count": len(evidence),
            "evidence_hashes": [e.content_hash_sha256 for e in evidence],
            "metrics_evaluated": [
                {"metric": m.metric_name, "value": m.value, "passed": m.passed} for m in metrics
            ],
            "quality_decisions": [
                {"gate": d.gate_name, "outcome": d.outcome.value if hasattr(d.outcome, 'value') else d.outcome, "score": d.composite_score} for d in decisions
            ],
            "is_provenance_complete": bool(definition and plan and dver and env_snap and cfg_snap and cert and evidence and metrics)
        }


evidence_graph_engine = EvidenceGraphEngine()
