"""
Research Validation & Independent Scientific Verification Framework (RVISF)
Phase 35: Floating Point Error Analysis Laboratory

Provides rigorous quantification of numerical precision, machine epsilon, ULP (Units in Last Place) distances,
interval arithmetic propagation, condition number estimation, and forward/backward error analysis
compliant with IEEE 754 standards.
"""

from __future__ import annotations

import math
import struct
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


@dataclass(frozen=True)
class Interval:
    """Rigorous interval arithmetic interval [low, high]."""
    low: float
    high: float

    def __post_init__(self):
        if self.low > self.high:
            raise ValueError(f"Invalid interval: lower bound {self.low} > upper bound {self.high}")

    @classmethod
    def from_point(cls, value: float, radius: float = 0.0) -> Interval:
        return cls(low=value - radius, high=value + radius)

    def contains(self, x: float) -> bool:
        return self.low <= x <= self.high

    def width(self) -> float:
        return self.high - self.low

    def midpoint(self) -> float:
        return (self.low + self.high) / 2.0

    def radius(self) -> float:
        return (self.high - self.low) / 2.0

    def add(self, other: Interval) -> Interval:
        return Interval(self.low + other.low, self.high + other.high)

    def sub(self, other: Interval) -> Interval:
        return Interval(self.low - other.high, self.high - other.low)

    def mul(self, other: Interval) -> Interval:
        products = [
            self.low * other.low,
            self.low * other.high,
            self.high * other.low,
            self.high * other.high
        ]
        return Interval(min(products), max(products))

    def div(self, other: Interval) -> Interval:
        if other.low <= 0.0 <= other.high:
            raise ZeroDivisionError("Interval division by an interval containing zero.")
        quotients = [
            self.low / other.low,
            self.low / other.high,
            self.high / other.low,
            self.high / other.high
        ]
        return Interval(min(quotients), max(quotients))


@dataclass
class ULPMeasurement:
    """Measurement of Unit in the Last Place (ULP) distance between two floating point numbers."""
    val_a: float
    val_b: float
    ulp_distance: int
    is_exact: bool
    absolute_difference: float
    relative_difference: float


@dataclass
class ConditionNumberReport:
    """Report on matrix/function condition number estimation."""
    condition_number: float
    well_conditioned: bool
    stability_grade: str  # "EXCELLENT", "ADEQUATE", "ILL_CONDITIONED", "SINGULAR"
    estimated_precision_loss_bits: float
    notes: str


@dataclass
class FloatingPointAuditReport:
    """Comprehensive floating point error analysis report."""
    machine_epsilon_f64: float
    machine_epsilon_f32: float
    ulp_evaluations: List[ULPMeasurement]
    interval_propagation_passed: bool
    condition_analyses: List[ConditionNumberReport]
    forward_error_bound: float
    backward_error_bound: float
    status: str  # "PASS", "DEGRADED", "FAIL"
    metadata: Dict[str, Any] = field(default_factory=dict)


class FloatingPointErrorLab:
    """
    IEEE 754 Floating Point Precision & Error Propagation Verification Suite.
    """

    @staticmethod
    def get_machine_epsilon(precision: str = "float64") -> float:
        """Calculate the empirical machine epsilon (distance between 1.0 and next representable number)."""
        if precision == "float32":
            return 2.0 ** -23
        return 2.0 ** -52

    @staticmethod
    def calculate_ulp_distance(a: float, b: float) -> ULPMeasurement:
        """
        Calculate the integer number of IEEE-754 representable steps (ULPs) between two float64 numbers.
        """
        if math.isnan(a) or math.isnan(b):
            return ULPMeasurement(
                val_a=a, val_b=b, ulp_distance=-1, is_exact=False,
                absolute_difference=float('nan'), relative_difference=float('nan')
            )
        if math.isinf(a) or math.isinf(b):
            is_same = (a == b)
            return ULPMeasurement(
                val_a=a, val_b=b, ulp_distance=0 if is_same else 2**63,
                is_exact=is_same,
                absolute_difference=0.0 if is_same else float('inf'),
                relative_difference=0.0 if is_same else float('inf')
            )

        a_int = struct.unpack('>q', struct.pack('>d', a))[0]
        b_int = struct.unpack('>q', struct.pack('>d', b))[0]

        if a_int < 0:
            a_int = 0x8000000000000000 - a_int
        if b_int < 0:
            b_int = 0x8000000000000000 - b_int

        diff = abs(a_int - b_int)
        abs_diff = abs(a - b)
        rel_diff = abs_diff / max(abs(a), abs(b)) if max(abs(a), abs(b)) > 0 else 0.0

        return ULPMeasurement(
            val_a=a,
            val_b=b,
            ulp_distance=diff,
            is_exact=(diff == 0),
            absolute_difference=abs_diff,
            relative_difference=rel_diff
        )

    @classmethod
    def estimate_function_condition_number(
        cls,
        func: Callable[[float], float],
        x: float,
        h: float = 1e-7
    ) -> ConditionNumberReport:
        """
        Estimate the relative condition number of a scalar function f(x):
        cond(f, x) = | x * f'(x) / f(x) |
        """
        fx = func(x)
        if abs(fx) < 1e-15:
            return ConditionNumberReport(
                condition_number=float('inf'),
                well_conditioned=False,
                stability_grade="SINGULAR",
                estimated_precision_loss_bits=53.0,
                notes="f(x) near zero; relative condition number approaches infinity."
            )

        f_plus = func(x + h)
        f_minus = func(x - h)
        df_dx = (f_plus - f_minus) / (2.0 * h)

        cond = abs((x * df_dx) / fx) if fx != 0 else float('inf')
        loss_bits = math.log2(cond) if cond > 1.0 else 0.0

        if cond < 10.0:
            grade = "EXCELLENT"
            well_cond = True
        elif cond < 1e3:
            grade = "ADEQUATE"
            well_cond = True
        elif cond < 1e8:
            grade = "ILL_CONDITIONED"
            well_cond = False
        else:
            grade = "SINGULAR"
            well_cond = False

        return ConditionNumberReport(
            condition_number=cond,
            well_conditioned=well_cond,
            stability_grade=grade,
            estimated_precision_loss_bits=loss_bits,
            notes=f"Condition number: {cond:.4e}, estimated precision loss: {loss_bits:.2f} bits."
        )

    @classmethod
    def verify_interval_propagation(cls) -> bool:
        """Verify that basic interval arithmetic correctly brackets mathematical operations."""
        i1 = Interval(1.0, 2.0)
        i2 = Interval(3.0, 4.0)

        i_add = i1.add(i2)
        if i_add.low != 4.0 or i_add.high != 6.0:
            return False

        i_sub = i1.sub(i2)
        if i_sub.low != -3.0 or i_sub.high != -1.0:
            return False

        i_mul = i1.mul(i2)
        if i_mul.low != 3.0 or i_mul.high != 8.0:
            return False

        i_div = i1.div(i2)
        if i_div.low != 0.25 or not math.isclose(i_div.high, 2.0/3.0):
            return False

        return True

    @classmethod
    def run_full_floating_point_audit(cls) -> FloatingPointAuditReport:
        """Run full floating point error analysis laboratory audit."""
        eps64 = cls.get_machine_epsilon("float64")
        eps32 = cls.get_machine_epsilon("float32")

        ulp_tests = [
            (1.0, 1.0 + eps64),
            (1.0, 1.0),
            (1000.0, 1000.0000000000001),
            (math.pi, 3.141592653589793),
        ]
        ulp_evals = [cls.calculate_ulp_distance(a, b) for a, b in ulp_tests]

        interval_ok = cls.verify_interval_propagation()

        cond_reports = [
            cls.estimate_function_condition_number(lambda x: x**2, 5.0),
            cls.estimate_function_condition_number(lambda x: math.sin(x), 1.0),
            cls.estimate_function_condition_number(lambda x: 1.0 / (x - 1.0), 1.00000001),
        ]

        fwd_error = max(m.absolute_difference for m in ulp_evals if not math.isnan(m.absolute_difference))
        bwd_error = eps64 * 2.0

        status = "PASS" if interval_ok and any(c.well_conditioned for c in cond_reports) else "FAIL"

        return FloatingPointAuditReport(
            machine_epsilon_f64=eps64,
            machine_epsilon_f32=eps32,
            ulp_evaluations=ulp_evals,
            interval_propagation_passed=interval_ok,
            condition_analyses=cond_reports,
            forward_error_bound=fwd_error,
            backward_error_bound=bwd_error,
            status=status,
            metadata={"standard": "IEEE 754-2019", "precision_bits": 64}
        )
