import pytest
from app.runtime.evolution.genetic_optimizer import GeneticPlannerOptimizer
from app.runtime.evolution.bayesian_optimizer import BayesianPlannerOptimizer
from app.runtime.evolution.planner_version_registry import PlannerVersionRegistry
from app.runtime.evolution.planner_evolution_engine import PlannerSelfEvolutionEngine


def test_genetic_planner_optimizer():
    optimizer = GeneticPlannerOptimizer(population_size=6)
    best_chrom = optimizer.evolve_generation()
    assert best_chrom.generation >= 1
    assert best_chrom.fitness_score > 0
    assert best_chrom.search_beam_width >= 2


def test_bayesian_planner_optimizer():
    optimizer = BayesianPlannerOptimizer()
    suggested = optimizer.suggest_next_parameters()
    assert "weight_accuracy" in suggested
    assert "weight_cost" in suggested
    assert "weight_latency" in suggested


def test_planner_version_registry():
    registry = PlannerVersionRegistry()
    gens = registry.list_generations()
    assert len(gens) >= 3
    assert registry.get_active_generation().version_tag == "v3.0.0"
    
    # Test rollback
    rolled_back = registry.rollback_to_previous()
    assert rolled_back is not None
    assert rolled_back.version_tag == "v2.0.0"


def test_planner_self_evolution_cycle():
    registry = PlannerVersionRegistry()
    engine = PlannerSelfEvolutionEngine(registry=registry)
    
    report = engine.run_evolution_cycle(
        weakness_diagnosis="Sub-optimal token allocation in high-noise scans",
        target_simulated_trials=500,
    )
    
    assert report.is_promoted is True
    assert report.utility_gain_pct > 0
    assert registry.get_active_generation().version_tag.startswith("v3.")
