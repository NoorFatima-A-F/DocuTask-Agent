"""
Statistical Evaluation Domain: Confidence Intervals, Hypothesis Testing, Variance, and Anomaly Detection.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import numpy as np
import uuid


class StatisticalMethod(str, Enum):
    BOOTSTRAP_CONFIDENCE_INTERVAL = "BOOTSTRAP_CONFIDENCE_INTERVAL"
    STUDENT_T_TEST = "STUDENT_T_TEST"
    MANN_WHITNEY_U = "MANN_WHITNEY_U"
    KOLMOGOROV_SMIRNOV = "KOLMOGOROV_SMIRNOV"
    ANOMALY_Z_SCORE = "ANOMALY_Z_SCORE"


class StatisticalAnalysis(BaseModel):
    analysis_id: str = Field(default_factory=lambda: f"stat_{uuid.uuid4().hex[:8]}")
    execution_id: str
    metric_name: str
    method: StatisticalMethod = StatisticalMethod.BOOTSTRAP_CONFIDENCE_INTERVAL
    sample_size: int
    confidence_level: float = 0.95
    mean: float
    variance: float
    standard_deviation: float
    ci_lower: float
    ci_upper: float
    p_value: Optional[float] = None
    is_statistically_significant: bool = True
    drift_detected: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)
    analyzed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @classmethod
    def from_samples(
        cls,
        execution_id: str,
        metric_name: str,
        samples: List[float],
        confidence_level: float = 0.95
    ) -> "StatisticalAnalysis":
        arr = np.array(samples, dtype=float)
        mean_val = float(np.mean(arr))
        var_val = float(np.var(arr, ddof=1)) if len(arr) > 1 else 0.0
        std_val = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
        
        # Simple normal approximation for CI
        margin = 1.96 * (std_val / np.sqrt(len(arr))) if len(arr) > 1 else 0.0
        return cls(
            execution_id=execution_id,
            metric_name=metric_name,
            sample_size=len(arr),
            confidence_level=confidence_level,
            mean=round(mean_val, 4),
            variance=round(var_val, 4),
            standard_deviation=round(std_val, 4),
            ci_lower=round(mean_val - margin, 4),
            ci_upper=round(mean_val + margin, 4)
        )
