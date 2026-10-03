"""
Autonomous Goal Intelligence & Mission Management System Demonstration
=======================================================================
Demonstrates Stage 1 of the Autonomous Cognition Loop:
Goal -> Goal Intelligence -> Mission Definition -> Validation -> Capability Analysis
-> Risk Assessment -> Resource Planning -> Success Criteria -> Mission Graph -> Ready For Observation
"""

from research_validation.goal.models import (
    GoalType, PriorityLevel, GoalConstraints,
    ConfidenceLevel, ConfidenceThreshold, StoppingConditionType, StoppingCondition,
    Comparator, SuccessCriterion, CapabilityCriticality, CapabilityRequirement
)
from research_validation.goal.interfaces import (
    SystemClock, DeterministicIdGenerator, InMemoryEventBus, DefaultSystemCapabilityProvider
)
from research_validation.goal.repositories import (
    InMemoryGoalRepository, InMemoryMissionRepository
)
from research_validation.goal.services import (
    GoalManager, MissionBuilder, MissionScheduler
)


def main():
    print("=" * 80)
    print(" AUTONOMOUS GOAL INTELLIGENCE & MISSION MANAGEMENT SYSTEM (STAGE 1)")
    print("=" * 80)

    # 1. Setup Infrastructure
    print("\n[Stage 1.0] Initializing Repositories, Event Bus, and Goal Manager...")
    event_bus = InMemoryEventBus()
    event_bus.subscribe("*", lambda e: print(f"  [EventBus] Emitted -> {e.event_type} (Aggregate: {e.aggregate_id})"))
    
    clock = SystemClock()
    id_gen = DeterministicIdGenerator("auton")
    goal_repo = InMemoryGoalRepository()
    mission_repo = InMemoryMissionRepository()

    goal_manager = GoalManager(
        repository=goal_repo,
        event_bus=event_bus,
        id_generator=id_gen,
        clock=clock,
    )

    # 2. Ingest High-Level Scientific Goal
    print("\n[Stage 1.1] Ingesting User Scientific Objective...")
    goal = goal_manager.create_goal(
        title="Cross-Domain Invoice Extraction Generalization",
        description="Quantify token extraction precision and recall across unseen multi-lingual receipt layouts.",
        objective="Achieve token classification F1 >= 0.94 with Wilson 95% confidence bounds and P99 latency <= 35ms.",
        problem_statement="Layout models experience catastrophic precision loss when encountering rotated tables in French receipts.",
        goal_type=GoalType.MODEL_EVALUATION,
        priority=PriorityLevel.CRITICAL,
        owner="LEAD_AI_RESEARCHER",
        confidence_threshold=ConfidenceThreshold(ConfidenceLevel.HIGH),
        success_metrics=[
            SuccessCriterion(
                metric_name="token_f1",
                comparator=Comparator.GREATER_THAN_OR_EQUAL,
                target_value=0.94,
                tolerance=0.005,
                confidence_requirement=0.95,
                minimum_sample_size=50,
            ),
            SuccessCriterion(
                metric_name="latency_p99_ms",
                comparator=Comparator.LESS_THAN_OR_EQUAL,
                target_value=35.0,
                tolerance=2.0,
                confidence_requirement=0.90,
                minimum_sample_size=50,
            ),
        ],
        stopping_conditions=[
            StoppingCondition(
                condition_type=StoppingConditionType.GOAL_ACHIEVED,
                description="Token F1 reaches 0.94 with 95% confidence and P99 latency <= 35ms.",
            ),
            StoppingCondition(
                condition_type=StoppingConditionType.CRITICAL_REGRESSION,
                description="Halt if token F1 degrades by > 5% vs baseline.",
            ),
            StoppingCondition(
                condition_type=StoppingConditionType.MAX_ITERATIONS,
                description="Stop after maximum 50 iterations.",
            ),
        ],
        required_datasets=["funsd", "sroie", "cord"],
        required_models=["document_processor_v2"],
        capability_requirements=[
            CapabilityRequirement("OCR", "MODEL", CapabilityCriticality.MANDATORY),
            CapabilityRequirement("BENCHMARK", "BENCHMARK", CapabilityCriticality.MANDATORY),
            CapabilityRequirement("STORAGE", "STORAGE", CapabilityCriticality.MANDATORY),
            CapabilityRequirement("GPU_ACCELERATION", "HARDWARE", CapabilityCriticality.OPTIONAL),
        ],
        constraints=GoalConstraints(
            max_runtime_hours=24.0,
            max_gpu_hours=8.0,
            max_cost_usd=100.0,
        ),
    )
    print(f"  -> Created Goal ID: {goal.goal_id} | SHA-256 Digest: {goal.cryptographic_digest_sha256[:16]}...")

    # 3. Build Validated Mission
    print("\n[Stage 1.2] Executing Mission Builder Pipeline (Validation -> Capabilities -> Risks -> Budget -> Graph)...")
    mission_builder = MissionBuilder(
        event_bus=event_bus,
        id_generator=id_gen,
        clock=clock,
        capability_provider=DefaultSystemCapabilityProvider(),
    )

    mission = mission_builder.build_mission(goal)
    mission_repo.save_mission(mission)

    # 4. Inspect Mission Graph Hierarchy
    print(f"\n[Stage 1.3] Mission Graph Synthesized (State: {mission.state.value}):")
    print(f"  -> Mission ID: {mission.mission_id} | Version: {mission.version}")
    print(f"  -> Cryptographic Digest: {mission.mission_digest_sha256}")
    print(f"  -> Objectives Count: {len(mission.objectives)}")
    print(f"  -> Total Milestones: {mission.metrics.total_milestones_count} | Tasks: {mission.metrics.total_tasks_count} | Actions: {mission.metrics.total_actions_count}")
    print(f"  -> Graph Depth: {mission.metrics.graph_depth} | Readiness Score: {mission.metrics.readiness_score:.2f}")

    # 5. Risk and Budget Breakdown
    print(f"\n[Stage 1.4] Risk Profile & Budget Estimation:")
    print(f"  -> Overall Risk Score: {mission.risk_profile.overall_risk_score:.2f} ({mission.risk_profile.severity.value})")
    print(f"  -> Has Blocking Risks: {mission.risk_profile.has_blocking_risks}")
    print(f"  -> Estimated Runtime: {mission.execution_budget.expected_runtime_hours:.1f}h (Max: {mission.execution_budget.maximum_runtime_hours:.1f}h)")
    print(f"  -> Estimated Cost: ${mission.execution_budget.resource_budget.cost_usd:.2f} | CPU Hours: {mission.execution_budget.resource_budget.cpu_hours:.1f}")

    # 6. Mission Scheduling
    print(f"\n[Stage 1.5] Mission Scheduler Priority Queue & Activation:")
    scheduler = MissionScheduler(repository=mission_repo, event_bus=event_bus, clock=clock, max_concurrent_missions=4)
    queue = scheduler.get_prioritized_queue()
    print(f"  -> Pending Ready Queue Size: {len(queue)}")
    activated_mission = scheduler.activate_next_mission()
    print(f"  -> Activated Mission ID: {activated_mission.mission_id} (New State: {activated_mission.state.value})")

    print("\n" + "=" * 80)
    print(" STAGE 1 GOAL INTELLIGENCE & MISSION MANAGEMENT COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
