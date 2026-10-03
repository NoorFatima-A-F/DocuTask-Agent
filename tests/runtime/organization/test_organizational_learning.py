"""
Test Suite: Organizational Learning & Department Memory
Validates department knowledge accumulation, retrospective self-critique, and enterprise learning synthesis.
"""
from app.runtime.org_learning.department_memory import DepartmentMemoryManager
from app.runtime.org_learning.department_reflection import DepartmentReflectionEngine
from app.runtime.org_learning.organizational_learning import OrganizationalLearningSynthesizer


def test_department_memory_manager():
    mgr = DepartmentMemoryManager()
    
    item = mgr.add_knowledge(
        department_id="dept_ocr",
        category="HEURISTIC",
        title="Adaptive Thresholding on Watermarks",
        content="Apply Otsu binarization when background noise > 0.4.",
        accuracy_delta=0.025,
        confidence=0.97,
    )

    assert item.department_id == "dept_ocr"
    assert item.accuracy_delta == 0.025
    assert len(mgr.get_department_knowledge("dept_ocr")) >= 2


def test_department_reflection_retrospectives():
    retro_ocr = DepartmentReflectionEngine.conduct_department_retrospective("dept_ocr")
    assert retro_ocr.department_id == "dept_ocr"
    assert retro_ocr.self_evaluation_score >= 0.90
    assert len(retro_ocr.bottlenecks_identified) >= 1
    assert len(retro_ocr.proposed_learning_actions) >= 1


def test_organizational_learning_synthesis():
    summary = OrganizationalLearningSynthesizer.get_organization_learning_summary()
    assert summary["total_versioned_knowledge_rules"] >= 3
    assert summary["cumulative_accuracy_improvement_pct"] > 0.0
    assert summary["learning_cycle_status"] == "CONTINUOUS_SYNTHESIS_ACTIVE"
    assert len(summary["recent_retrospectives"]) >= 3
