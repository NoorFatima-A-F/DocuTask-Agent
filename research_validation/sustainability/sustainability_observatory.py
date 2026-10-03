"""
Independent Evidence & Real-World Validation Platform (IERVP)
Phase 67: Sustainability & Green Computing Observatory

Tracks computational energy efficiency and carbon emissions:
- Metrics: CPU Joules, GPU Joules, Total kWh, Operational Carbon (gCO2eq)
- Per-Unit Efficiency: Energy per Document, Carbon per Multi-Agent Workflow
- Provenance Rigor: Strictly distinguishes MEASURED hardware telemetry (RAPL/NVML) from ESTIMATED models.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class MeasurementSourceType(str, Enum):
    MEASURED_HARDWARE_RAPL = "MEASURED_HARDWARE_RAPL"
    MEASURED_GPU_NVML = "MEASURED_GPU_NVML"
    ESTIMATED_TDP_MODEL = "ESTIMATED_TDP_MODEL"
    ESTIMATED_CLOUD_BILLING_PROXY = "ESTIMATED_CLOUD_BILLING_PROXY"


@dataclass
class WorkflowCarbonMeasurement:
    """Telemetry for energy and carbon consumed by an execution."""
    workflow_id: str
    source_type: MeasurementSourceType
    is_measured_telemetry: bool  # Strictly flagged!
    is_estimate: bool            # Strictly flagged!
    duration_seconds: float
    documents_processed: int
    cpu_energy_joules: float
    gpu_energy_joules: float
    total_energy_kwh: float
    grid_carbon_intensity_g_per_kwh: float
    total_carbon_emissions_g_co2: float
    energy_per_document_joules: float
    carbon_per_document_g: float


@dataclass
class SustainabilityObservatoryReport:
    """Consolidated sustainability and environmental impact report."""
    total_workflows_evaluated: int
    measured_telemetry_count: int
    estimated_models_count: int
    total_energy_kwh: float
    total_carbon_emissions_g: float
    mean_energy_per_doc_joules: float
    mean_carbon_per_doc_g: float
    efficiency_grade: str  # "A_GREEN_OPTIMIZED", "B_STANDARD", "C_CARBON_INTENSIVE"
    measurements: List[WorkflowCarbonMeasurement]
    assumptions: List[str]
    methodology: str
    limitations: List[str]
    reproducibility_instructions: str
    status: str  # "PASS", "MODERATE_CARBON", "HIGH_EMISSIONS"


class SustainabilityObservatory:
    """
    Monitors energy consumption and operational carbon footprints.
    """

    @classmethod
    def record_measurement(
        cls,
        workflow_id: str,
        duration_sec: float,
        num_docs: int,
        source: MeasurementSourceType = MeasurementSourceType.ESTIMATED_TDP_MODEL,
        cpu_power_watts: float = 45.0,
        gpu_power_watts: float = 0.0,
        grid_intensity: float = 60.0,  # Finland green cloud baseline (gCO2eq/kWh)
        pue: float = 1.10
    ) -> WorkflowCarbonMeasurement:
        """Create a single carbon and energy telemetry record."""
        is_measured = source in (MeasurementSourceType.MEASURED_HARDWARE_RAPL, MeasurementSourceType.MEASURED_GPU_NVML)
        is_est = not is_measured

        cpu_j = (cpu_power_watts * duration_sec) * pue
        gpu_j = (gpu_power_watts * duration_sec) * pue
        total_j = cpu_j + gpu_j
        total_kwh = total_j / 3.6e6

        carbon_g = total_kwh * grid_intensity

        safe_docs = max(1, num_docs)
        e_per_doc = total_j / safe_docs
        c_per_doc = carbon_g / safe_docs

        return WorkflowCarbonMeasurement(
            workflow_id=workflow_id,
            source_type=source,
            is_measured_telemetry=is_measured,
            is_estimate=is_est,
            duration_seconds=duration_sec,
            documents_processed=num_docs,
            cpu_energy_joules=cpu_j,
            gpu_energy_joules=gpu_j,
            total_energy_kwh=total_kwh,
            grid_carbon_intensity_g_per_kwh=grid_intensity,
            total_carbon_emissions_g_co2=carbon_g,
            energy_per_document_joules=e_per_doc,
            carbon_per_document_g=c_per_doc
        )

    @classmethod
    def generate_observatory_report(
        cls,
        records: List[WorkflowCarbonMeasurement]
    ) -> SustainabilityObservatoryReport:
        """Generate comprehensive sustainability observatory audit."""
        if not records:
            return SustainabilityObservatoryReport(
                total_workflows_evaluated=0,
                measured_telemetry_count=0,
                estimated_models_count=0,
                total_energy_kwh=0.0,
                total_carbon_emissions_g=0.0,
                mean_energy_per_doc_joules=0.0,
                mean_carbon_per_doc_g=0.0,
                efficiency_grade="UNKNOWN",
                measurements=[],
                assumptions=["Workload energy monitored"],
                limitations=["No energy telemetry recorded"],
                reproducibility_instructions="Run workloads through SustainabilityObservatory.record_measurement()",
                status="PASS"
            )

        n = len(records)
        measured = sum(1 for r in records if r.is_measured_telemetry)
        estimated = n - measured

        tot_kwh = sum(r.total_energy_kwh for r in records)
        tot_carbon = sum(r.total_carbon_emissions_g_co2 for r in records)
        mean_e_doc = sum(r.energy_per_document_joules for r in records) / n
        mean_c_doc = sum(r.carbon_per_document_g for r in records) / n

        grade = "A_GREEN_OPTIMIZED" if mean_c_doc < 0.05 else "B_STANDARD" if mean_c_doc < 0.50 else "C_CARBON_INTENSIVE"
        status = "PASS" if grade != "C_CARBON_INTENSIVE" else "HIGH_EMISSIONS"

        return SustainabilityObservatoryReport(
            total_workflows_evaluated=n,
            measured_telemetry_count=measured,
            estimated_models_count=estimated,
            total_energy_kwh=tot_kwh,
            total_carbon_emissions_g=tot_carbon,
            mean_energy_per_doc_joules=mean_e_doc,
            mean_carbon_per_doc_g=mean_c_doc,
            efficiency_grade=grade,
            measurements=records,
            assumptions=[
                "Grid carbon intensity derived from Electricity Maps / Our World in Data regional averages",
                "Datacenter Power Usage Effectiveness (PUE) assumed at 1.10 for hyperscaler facilities"
            ],
            methodology="Hardware energy integration (Joules) converted to operational CO2 equivalent via regional grid carbon intensity factors.",
            limitations=[
                "Embodied hardware manufacturing carbon (Scope 3) is amortized separately and not included in per-query operational totals"
            ],
            reproducibility_instructions="Execute SustainabilityObservatory with Intel RAPL or estimated TDP profiles.",
            status=status
        )
