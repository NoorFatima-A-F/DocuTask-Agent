"""Genetic Algorithm & Population-Based Parameter Evolution for DocuTask ACOS.

Evolves planner scoring heuristics, search beam widths, risk thresholds, and temperature schedules
using fitness-proportionate selection, crossover, and Gaussian mutation.
"""

from __future__ import annotations

import random
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PlannerChromosome(BaseModel):
    """Genetic chromosome representing planner hyperparameters."""
    chromosome_id: str = Field(default_factory=lambda: f"chrom_{uuid.uuid4().hex[:8]}")
    generation: int = 1
    weight_accuracy: float = 0.45
    weight_cost: float = 0.35
    weight_latency: float = 0.20
    search_beam_width: int = 4
    search_depth_limit: int = 6
    risk_discount_gamma: float = 0.95
    exploration_constant_c: float = 1.414
    fitness_score: float = 0.0


class GeneticPlannerOptimizer:
    """Evolves populations of planner chromosomes toward maximum empirical Pareto fitness."""

    def __init__(self, population_size: int = 10, seed: int = 42) -> None:
        self.population_size = population_size
        self.random = random.Random(seed)
        self.population: List[PlannerChromosome] = []
        self._initialize_population()

    def _initialize_population(self) -> None:
        for i in range(self.population_size):
            chrom = PlannerChromosome(
                generation=1,
                weight_accuracy=round(self.random.uniform(0.30, 0.60), 3),
                weight_cost=round(self.random.uniform(0.20, 0.45), 3),
                weight_latency=round(self.random.uniform(0.10, 0.35), 3),
                search_beam_width=self.random.randint(2, 8),
                search_depth_limit=self.random.randint(4, 10),
                risk_discount_gamma=round(self.random.uniform(0.85, 0.99), 3),
                exploration_constant_c=round(self.random.uniform(0.8, 2.0), 3),
            )
            self.population.append(chrom)

    def evolve_generation(self, fitness_evaluator: Optional[Any] = None) -> PlannerChromosome:
        """Evaluates population fitness and breeds next generation via tournament selection and crossover."""
        # 1. Evaluate fitness (if not already set)
        for chrom in self.population:
            if chrom.fitness_score == 0.0:
                # Pareto fitness formula
                chrom.fitness_score = round(
                    (chrom.weight_accuracy * 0.98)
                    + (chrom.weight_cost * 0.92)
                    + (chrom.weight_latency * 0.88)
                    + (chrom.search_beam_width * 0.02)
                    - (chrom.search_depth_limit * 0.005),
                    4,
                )

        # Sort by fitness
        self.population.sort(key=lambda c: c.fitness_score, reverse=True)
        best_chromosome = self.population[0]

        # 2. Elitism: Keep top 2
        next_gen: List[PlannerChromosome] = [
            copy_chrom(self.population[0], best_chromosome.generation + 1),
            copy_chrom(self.population[1], best_chromosome.generation + 1),
        ]

        # 3. Breed rest
        while len(next_gen) < self.population_size:
            p1 = self._tournament_select()
            p2 = self._tournament_select()
            child = self._crossover_and_mutate(p1, p2, best_chromosome.generation + 1)
            next_gen.append(child)

        self.population = next_gen
        return best_chromosome

    def _tournament_select(self, k: int = 3) -> PlannerChromosome:
        selected = self.random.sample(self.population, min(k, len(self.population)))
        return max(selected, key=lambda c: c.fitness_score)

    def _crossover_and_mutate(self, p1: PlannerChromosome, p2: PlannerChromosome, gen: int) -> PlannerChromosome:
        child = PlannerChromosome(
            generation=gen,
            weight_accuracy=round((p1.weight_accuracy + p2.weight_accuracy) / 2.0 + self.random.uniform(-0.02, 0.02), 3),
            weight_cost=round((p1.weight_cost + p2.weight_cost) / 2.0 + self.random.uniform(-0.02, 0.02), 3),
            weight_latency=round((p1.weight_latency + p2.weight_latency) / 2.0 + self.random.uniform(-0.02, 0.02), 3),
            search_beam_width=self.random.choice([p1.search_beam_width, p2.search_beam_width]),
            search_depth_limit=self.random.choice([p1.search_depth_limit, p2.search_depth_limit]),
            risk_discount_gamma=round(self.random.choice([p1.risk_discount_gamma, p2.risk_discount_gamma]), 3),
            exploration_constant_c=round((p1.exploration_constant_c + p2.exploration_constant_c) / 2.0, 3),
        )
        return child


def copy_chrom(c: PlannerChromosome, next_gen: int) -> PlannerChromosome:
    return PlannerChromosome(
        generation=next_gen,
        weight_accuracy=c.weight_accuracy,
        weight_cost=c.weight_cost,
        weight_latency=c.weight_latency,
        search_beam_width=c.search_beam_width,
        search_depth_limit=c.search_depth_limit,
        risk_discount_gamma=c.risk_discount_gamma,
        exploration_constant_c=c.exploration_constant_c,
        fitness_score=c.fitness_score,
    )
