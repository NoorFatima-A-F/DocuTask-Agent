"""
Test Suite: Hackathon Demo Engine Execution
Validates 1-click end-to-end hackathon demo step sequences, live telemetry snapshots, and mission summaries.
"""
from app.runtime.demo_engine.demo_engine import HackathonDemoEngine


def test_demo_engine_step_generation():
    steps = HackathonDemoEngine.get_canonical_demo_steps()
    
    assert len(steps) == 5
    # Verify all 5 steps have proper sequencing and telemetry
    for i, step in enumerate(steps, start=1):
        assert step["step_index"] == i
        assert "step_name" in step
        assert "narration" in step
        assert "active_worker" in step
        assert "telemetry_snapshot" in step
        assert "latency_ms" in step["telemetry_snapshot"]
