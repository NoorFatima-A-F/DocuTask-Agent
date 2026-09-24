"""
Tests for Process Health and Existence (Part 2).
"""
from app.platform_verification.liveness.process.process_verifier import ProcessVerifier
from app.platform_verification.liveness.domain.models import ProcessStatus


def test_process_verifier_running():
    verifier = ProcessVerifier()
    report = verifier.verify_processes()

    assert report.total_processes_checked >= 4
    assert report.running_processes_count == report.total_processes_checked
    assert report.zombies_count == 0
    assert report.terminated_count == 0
    assert report.all_processes_alive is True
    assert report.passed is True


def test_process_verifier_details():
    verifier = ProcessVerifier()
    report = verifier.verify_processes()

    api_proc = next((p for p in report.processes if p["service"] == "api"), None)
    assert api_proc is not None
    assert api_proc["state"] == ProcessStatus.RUNNING.value
    assert api_proc["pid"] > 0
