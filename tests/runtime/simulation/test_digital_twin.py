import pytest
from app.runtime.simulation.cluster_simulator import DigitalTwinClusterSimulator
from app.runtime.simulation.scale_simulator import MonteCarloScaleSimulator
from app.runtime.simulation.chaos_generator import ChaosFaultGenerator


def test_digital_twin_cluster_simulation():
    sim = DigitalTwinClusterSimulator(virtual_worker_count=50)
    assert len(sim.workers) == 50
    
    report = sim.simulate_mission_workload(mission_count=20, arrival_rate_per_sec=5.0)
    assert report.total_virtual_workers == 50
    assert report.processed_missions_count == 20
    assert report.p50_latency_ms > 0
    assert report.resilience_score > 0.8


def test_monte_carlo_scale_simulation():
    scale_sim = MonteCarloScaleSimulator()
    report = scale_sim.run_scale_simulation(total_steps=10000)
    assert report.total_steps_simulated == 10000
    assert report.sla_compliance_rate_pct >= 95.0
    assert len(report.bootstrap_ci_99_utility) == 2


def test_chaos_fault_generator():
    chaos = ChaosFaultGenerator()
    event = chaos.inject_random_fault(target_worker_id="v_worker_0001")
    assert event.target_node == "v_worker_0001"
    assert event.is_recovered_by_agent is True
    assert len(chaos.list_injected_faults()) == 1
