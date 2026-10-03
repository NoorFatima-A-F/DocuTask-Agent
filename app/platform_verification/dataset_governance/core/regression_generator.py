"""
Automated Defect Regression Dataset Generator.
Transforms production defect tickets and error reports into reproducible regression test samples.
"""
from typing import Any, Dict
from app.platform_verification.dataset_governance.domain.models import (
    DatasetSample, GroundTruthAnnotation, DatasetCategory, DatasetMetadata,
    DatasetLifecycleState, DataSensitivityLevel
)
from app.platform_verification.dataset_governance.core.registry import dataset_registry


class DefectRegressionGenerator:
    def create_regression_sample_from_defect(
        self,
        defect_id: str,
        failing_document_content: str,
        expected_remediation: Dict[str, Any],
        author: str = "Automated SRE Incident Agent"
    ) -> DatasetSample:
        sample = DatasetSample(
            sample_id=f"reg_smp_{defect_id}",
            content=failing_document_content,
            metadata={"defect_id": defect_id, "origin": "PRODUCTION_INCIDENT", "author": author},
            partition="eval"
        )
        annotation = GroundTruthAnnotation(
            sample_id=sample.sample_id,
            expected_output=expected_remediation,
            annotator=author,
            label="REGRESSION_FIX"
        )
        # Append to regression suite in registry
        reg_suite = dataset_registry.get_dataset("ds_regression_defects", "1.0.0")
        if reg_suite:
            current_samples = dataset_registry.get_samples("ds_regression_defects", "1.0.0")
            current_annotations = dataset_registry.get_annotations("ds_regression_defects", "1.0.0")
            current_samples.append(sample)
            current_annotations.append(annotation)
            reg_suite.sample_count = len(current_samples)
            reg_suite.ground_truth_count = len(current_annotations)

        return sample


regression_generator = DefectRegressionGenerator()
