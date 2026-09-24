"""
Workforce Verification Scorer.
Executes all 20 verification engines, aggregates assertions, and calculates composite readiness score and indices.
"""

import time
from typing import Dict, Any
from ..domain.models import (
    WorkforceReadinessScorecard,
    PartVerificationResult,
)
from ..registry.registry_verifier import WorkforceRegistryVerifier
from ..capabilities.capabilities_verifier import CapabilitiesVerifier
from ..hierarchy.hierarchy_verifier import HierarchyVerifier
from ..teams.team_formation_verifier import TeamFormationVerifier
from ..marketplace.marketplace_verifier import MarketplaceVerifier
from ..negotiation.negotiation_verifier import NegotiationVerifier
from ..collaboration.collaboration_verifier import CollaborationVerifier
from ..management.management_verifier import ManagementVerifier
from ..council.council_verifier import CouncilVerifier
from ..economics.economics_verifier import EconomicsVerifier
from ..hiring.hiring_verifier import HiringVerifier
from ..career.career_verifier import CareerVerifier
from ..scheduler.scheduler_verifier import SchedulerVerifier
from ..conflict.conflict_verifier import ConflictVerifier
from ..memory.memory_verifier import CollectiveMemoryVerifier
from ..trust.trust_verifier import TrustVerifier
from ..security.security_verifier import WorkforceSecurityVerifier
from ..scalability.scalability_verifier import ScalabilityVerifier
from ..benchmarks.benchmark_verifier import BenchmarkVerifier
from ..dashboards.dashboard_verifier import DashboardVerifier


class WorkforceScorer:
    """Executes all workforce verifiers, aggregates empirical results, and produces the complete WorkforceReadinessScorecard."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.verifiers = [
            WorkforceRegistryVerifier(self.config),
            CapabilitiesVerifier(self.config),
            HierarchyVerifier(self.config),
            TeamFormationVerifier(self.config),
            MarketplaceVerifier(self.config),
            NegotiationVerifier(self.config),
            CollaborationVerifier(self.config),
            ManagementVerifier(self.config),
            CouncilVerifier(self.config),
            EconomicsVerifier(self.config),
            HiringVerifier(self.config),
            CareerVerifier(self.config),
            SchedulerVerifier(self.config),
            ConflictVerifier(self.config),
            CollectiveMemoryVerifier(self.config),
            TrustVerifier(self.config),
            WorkforceSecurityVerifier(self.config),
            ScalabilityVerifier(self.config),
            BenchmarkVerifier(self.config),
            DashboardVerifier(self.config),
        ]

    def run_all(self) -> WorkforceReadinessScorecard:
        start_time = time.perf_counter()
        part_results: Dict[str, PartVerificationResult] = {}
        total_assertions = 0
        passed_assertions = 0

        for verifier in self.verifiers:
            res = verifier.verify()
            part_results[res.part_id.value] = res
            total_assertions += res.total_assertions_count
            passed_assertions += res.passed_assertions_count

        total_elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # Calculate composite score
        total_weight = sum(p.weight for p in part_results.values())
        weighted_score = sum(p.score * p.weight for p in part_results.values()) / max(0.001, total_weight)

        grade = "A+" if weighted_score >= 95.0 else ("A" if weighted_score >= 90.0 else "B")

        # Calculate Pillar Indices
        indices = {
            "registry_and_capabilities_index": (part_results["PART_01_REGISTRY"].score + part_results["PART_02_CAPABILITIES"].score) / 2.0,
            "hierarchy_and_teams_index": (part_results["PART_03_HIERARCHY"].score + part_results["PART_04_TEAMS"].score) / 2.0,
            "marketplace_and_negotiation_index": (part_results["PART_05_MARKETPLACE"].score + part_results["PART_06_NEGOTIATION"].score) / 2.0,
            "collaboration_and_management_index": (part_results["PART_07_COLLABORATION"].score + part_results["PART_08_MANAGEMENT"].score) / 2.0,
            "council_and_economics_index": (part_results["PART_09_COUNCIL"].score + part_results["PART_10_ECONOMICS"].score) / 2.0,
            "hiring_and_career_index": (part_results["PART_11_HIRING"].score + part_results["PART_12_CAREER"].score) / 2.0,
            "scheduler_and_conflict_index": (part_results["PART_13_SCHEDULER"].score + part_results["PART_14_CONFLICT"].score) / 2.0,
            "memory_and_trust_index": (part_results["PART_15_MEMORY"].score + part_results["PART_16_TRUST"].score) / 2.0,
            "security_and_scalability_index": (part_results["PART_17_SECURITY"].score + part_results["PART_18_SCALABILITY"].score) / 2.0,
            "benchmarking_and_dashboards_index": (part_results["PART_19_BENCHMARKS"].score + part_results["PART_20_DASHBOARDS"].score) / 2.0,
        }

        return WorkforceReadinessScorecard(
            parts=part_results,
            indices=indices,
            composite_score=weighted_score,
            grade=grade,
            total_assertions=total_assertions,
            passed_assertions=passed_assertions,
            production_ready=(weighted_score >= 95.0 and passed_assertions == total_assertions),
            total_execution_time_ms=total_elapsed_ms,
        )
