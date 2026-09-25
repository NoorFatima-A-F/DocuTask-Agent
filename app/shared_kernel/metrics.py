"""
Neutral Metrics Instrumentation Interfaces.
Defines telemetry contracts (Counters, Gauges, Histograms, Timers) without vendor SDK coupling.
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Optional

class MetricType(str, Enum):
    COUNTER = "COUNTER"
    GAUGE = "GAUGE"
    HISTOGRAM = "HISTOGRAM"
    TIMER = "TIMER"
    SUMMARY = "SUMMARY"

class MetricUnit(str, Enum):
    COUNT = "count"
    MILLISECONDS = "ms"
    SECONDS = "s"
    BYTES = "bytes"
    PERCENTAGE = "percent"
    RATIO = "ratio"

class CounterContract(ABC):
    @abstractmethod
    def increment(self, amount: float = 1.0, tags: Optional[Dict[str, str]] = None) -> None:
        pass

class GaugeContract(ABC):
    @abstractmethod
    def set(self, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        pass

class HistogramContract(ABC):
    @abstractmethod
    def record(self, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        pass

class TimerContract(ABC):
    @abstractmethod
    def record_ms(self, duration_ms: float, tags: Optional[Dict[str, str]] = None) -> None:
        pass

class DistributionSummaryContract(ABC):
    @abstractmethod
    def record(self, amount: float, tags: Optional[Dict[str, str]] = None) -> None:
        pass

class MetricsCollectorContract(ABC):
    @abstractmethod
    def counter(self, name: str, description: str = "") -> CounterContract:
        pass

    @abstractmethod
    def gauge(self, name: str, description: str = "") -> GaugeContract:
        pass

    @abstractmethod
    def histogram(self, name: str, unit: MetricUnit = MetricUnit.MILLISECONDS) -> HistogramContract:
        pass

    @abstractmethod
    def timer(self, name: str) -> TimerContract:
        pass
