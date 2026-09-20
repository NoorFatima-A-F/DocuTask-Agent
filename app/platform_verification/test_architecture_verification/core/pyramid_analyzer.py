"""
Test Pyramid and Directory Structure Analyzer.
"""
from typing import Dict, List
from app.platform_verification.test_architecture_verification.domain.models import (
    TestPyramidReport,
    TestPyramidDistribution,
    TestArchitectureLayer,
)
from app.platform_verification.test_architecture_verification.domain.interfaces import IPyramidAnalyzer


class PyramidAnalyzer(IPyramidAnalyzer):
    """Analyzes test distribution across the canonical test pyramid layers."""

    REQUIRED_LAYERS = {
        TestArchitectureLayer.UNIT.value,
        TestArchitectureLayer.INTEGRATION.value,
        TestArchitectureLayer.E2E.value,
        TestArchitectureLayer.AI_EVALUATION.value,
        TestArchitectureLayer.SECURITY.value,
        TestArchitectureLayer.REGRESSION.value,
    }

    def analyze_pyramid(self, test_manifest: Dict[str, List[str]]) -> TestPyramidReport:
        missing_layers: List[str] = []
        issues: List[str] = []

        for req in self.REQUIRED_LAYERS:
            if req not in test_manifest or len(test_manifest[req]) == 0:
                missing_layers.append(req)
                issues.append(f"Missing mandatory test layer: '{req}'")

        counts = {
            "unit": len(test_manifest.get("unit", [])),
            "component": len(test_manifest.get("component", [])),
            "integration": len(test_manifest.get("integration", [])),
            "api": len(test_manifest.get("api", [])),
            "e2e": len(test_manifest.get("e2e", [])),
            "performance": len(test_manifest.get("performance", [])),
            "security": len(test_manifest.get("security", [])),
            "ai_evaluation": len(test_manifest.get("ai_evaluation", [])),
            "regression": len(test_manifest.get("regression", [])),
        }
        total = sum(counts.values())
        total_safe = max(total, 1)

        unit_ratio = (counts["unit"] + counts["component"]) / total_safe
        integration_ratio = (counts["integration"] + counts["api"]) / total_safe
        e2e_ratio = counts["e2e"] / total_safe

        distribution = TestPyramidDistribution(
            unit_count=counts["unit"],
            component_count=counts["component"],
            integration_count=counts["integration"],
            api_count=counts["api"],
            e2e_count=counts["e2e"],
            performance_count=counts["performance"],
            security_count=counts["security"],
            ai_evaluation_count=counts["ai_evaluation"],
            regression_count=counts["regression"],
            total_tests=total,
            unit_ratio=round(unit_ratio, 3),
            integration_ratio=round(integration_ratio, 3),
            e2e_ratio=round(e2e_ratio, 3),
        )

        score = 100.0
        # Check inverted pyramid (e.g. e2e > unit)
        if counts["e2e"] > (counts["unit"] + counts["component"]) and counts["e2e"] > 0:
            score -= 35.0
            issues.append("Inverted test pyramid detected: E2E tests exceed Unit tests")

        if unit_ratio < 0.50:
            score -= 15.0
            issues.append(f"Unit test ratio ({unit_ratio:.1%}) below target (60-70%)")

        score -= (len(missing_layers) * 10.0)
        score = max(0.0, min(100.0, score))
        status = "PASS" if score >= 80.0 else "FAIL"

        return TestPyramidReport(
            status=status,
            distribution=distribution,
            missing_required_layers=missing_layers,
            pyramid_health_score=round(score, 2),
            issues=issues,
        )
