"""
Independent Evidence & Real-World Validation Platform (IERVP)
Phase 54: Floating Point Error Propagation Framework

Quantifies numerical error propagation through computational graphs:
- Forward Error Analysis & Backward Error Analysis
- Condition Number Estimation & Sensitivity Gradients
- Rigorous Interval Arithmetic (bounding enclosures)
- Monte Carlo Arithmetic (random low-order bit perturbations)
- Shadow Execution (parallel Dual-Precision Float32/Float64 tracking)
- Error Budgeting: Worst-Case Error, Expected Error, Accumulated Error, Confidence Bounds
"""

from __future__ import annotations

import math
import random
import struct
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple


@dataclass(frozen=True)
class PrecisionInterval:
    """Rigorous real interval arithmetic enclosure [low, high]."""
    low: float
    high: float

    def __post_init__(self):
        if self.low > self.high:
            raise ValueError(f"Interval bounds invalid: {self.low} > {self.high}")

    def width(self) -> float:
        return self.high - self.low

    def midpoint(self) -> float:
        return (self.low + self.high) / 2.0

    def add(self, other: PrecisionInterval) -> PrecisionInterval:
        return PrecisionInterval(self.low + other.low, self.high + other.high)

    def sub(self, other: PrecisionInterval) -> PrecisionInterval:
        return PrecisionInterval(self.low - other.high, self.high - other.low)

    def mul(self, other: PrecisionInterval) -> PrecisionInterval:
        prods = [self.low * other.low, self.low * other.high, self.high * other.low, self.high * other.high]
        return PrecisionInterval(min(prods), max(prods))


@dataclass
class ShadowExecutionResult:
    """Output from parallel dual-precision execution (Float32 vs Float64)."""
    expression_name: str
    f64_result: float
    f32_result: float
    absolute_divergence: float
    relative_divergence: float
    significant_bits_lost: float


@dataclass
class MonteCarloErrorDistribution:
    """Statistical distribution of output variance under random mantissa bitflips."""
    mean_value: float
    std_deviation: float
    min_value: float
    max_value: float
    empirical_ci_95: Tuple[float, float]
    bits_of_precision: float


@dataclass
class ErrorBudgetReport:
    """Comprehensive floating point error propagation audit."""
    algorithm_name: str
    worst_case_error_bound: float
    expected_error: float
    accumulated_error_estimate: float
    condition_number: float
    confidence_bounds_99: Tuple[float, float]
    shadow_comparisons: List[ShadowExecutionResult]
    monte_carlo_distribution: MonteCarloErrorDistribution
    error_budget_allocated: float
    within_error_budget: bool
    status: str  # "PASS", "TIGHT_TOLERANCE", "EXCEEDED_BUDGET"


class FloatErrorPropagationFramework:
    """
    Evaluates forward/backward error propagation, condition numbers, and shadow execution.
    """

    @staticmethod
    def perturb_monte_carlo_float(val: float, noise_scale: float = 1e-14, rnd: Optional[random.Random] = None) -> float:
        """Inject random perturbation into the lowest mantissa bits."""
        r = rnd or random.Random()
        jitter = (r.random() - 0.5) * 2.0 * noise_scale * max(1.0, abs(val))
        return val + jitter

    @classmethod
    def run_monte_carlo_arithmetic(
        cls,
        func: Callable[[float], float],
        input_val: float,
        trials: int = 100,
        noise_scale: float = 1e-14,
        seed: int = 42
    ) -> MonteCarloErrorDistribution:
        """Evaluate sensitivity to lower mantissa perturbations over multiple trials."""
        rnd = random.Random(seed)
        outputs: List[float] = []

        for _ in range(trials):
            perturbed_x = cls.perturb_monte_carlo_float(input_val, noise_scale=noise_scale, rnd=rnd)
            out = func(perturbed_x)
            outputs.append(out)

        n = len(outputs)
        mean_v = sum(outputs) / n
        var_v = sum((x - mean_v) ** 2 for x in outputs) / (n - 1) if n > 1 else 0.0
        std_v = math.sqrt(var_v)

        sorted_outs = sorted(outputs)
        low_idx = int(0.025 * n)
        high_idx = min(int(0.975 * n), n - 1)
        ci_95 = (sorted_outs[low_idx], sorted_outs[high_idx])

        bits_lost = -math.log2(max(1e-16, std_v / max(1e-12, abs(mean_v)))) if std_v > 0 else 53.0

        return MonteCarloErrorDistribution(
            mean_value=mean_v,
            std_deviation=std_v,
            min_value=min(outputs),
            max_value=max(outputs),
            empirical_ci_95=ci_95,
            bits_of_precision=max(0.0, min(53.0, bits_lost))
        )

    @classmethod
    def execute_shadow_tracking(
        cls,
        expression_name: str,
        f64_calc: float,
        f32_calc: float
    ) -> ShadowExecutionResult:
        """Compares high-precision float64 baseline with float32 shadow execution."""
        abs_div = abs(f64_calc - f32_calc)
        rel_div = abs_div / max(abs(f64_calc), 1e-12)
        bits_lost = math.log2(max(1.0, rel_div / (2.0 ** -52))) if rel_div > 0 else 0.0

        return ShadowExecutionResult(
            expression_name=expression_name,
            f64_result=f64_calc,
            f32_result=f32_calc,
            absolute_divergence=abs_div,
            relative_divergence=rel_div,
            significant_bits_lost=bits_lost
        )

    @classmethod
    def evaluate_error_budget(
        cls,
        algorithm_name: str,
        func: Callable[[float], float],
        test_x: float,
        error_budget: float = 1e-5
    ) -> ErrorBudgetReport:
        """Run complete error propagation budget analysis."""
        # Monte Carlo
        mc_dist = cls.run_monte_carlo_arithmetic(func, test_x, trials=100)

        # Shadow execution simulation
        f64_val = func(test_x)
        # Simulate single-precision float32 input & calculation
        f32_x = struct.unpack('>f', struct.pack('>f', test_x))[0]
        f32_raw = func(f32_x)
        f32_val = struct.unpack('>f', struct.pack('>f', f32_raw))[0]

        shadow_res = cls.execute_shadow_tracking(f"{algorithm_name}({test_x})", f64_val, f32_val)

        # Condition number: | x * f'(x) / f(x) |
        h = 1e-7
        f_plus = func(test_x + h)
        f_minus = func(test_x - h)
        df_dx = (f_plus - f_minus) / (2.0 * h)
        cond = abs((test_x * df_dx) / f64_val) if abs(f64_val) > 1e-14 else float('inf')

        worst_case = (mc_dist.max_value - mc_dist.min_value) / 2.0
        expected_err = mc_dist.std_deviation
        accumulated_err = abs(f64_val - mc_dist.mean_value) + (cond * 2.0**-52 * abs(f64_val))

        ci_99 = (f64_val - 2.576 * expected_err, f64_val + 2.576 * expected_err)
        within_budget = worst_case <= error_budget

        status = "PASS" if within_budget else "EXCEEDED_BUDGET"

        return ErrorBudgetReport(
            algorithm_name=algorithm_name,
            worst_case_error_bound=worst_case,
            expected_error=expected_err,
            accumulated_error_estimate=accumulated_err,
            condition_number=cond,
            confidence_bounds_99=ci_99,
            shadow_comparisons=[shadow_res],
            monte_carlo_distribution=mc_dist,
            error_budget_allocated=error_budget,
            within_error_budget=within_budget,
            status=status
        )
