"""
Data Privacy Preservation Engine.
Applies anonymization, PII masking, token redaction, and synthetic replacement.
"""
import re
from app.platform_verification.dataset_governance.domain.models import DatasetSample
from app.platform_verification.dataset_governance.domain.interfaces import DatasetPrivacyEngineInterface


class DatasetPrivacyEngine(DatasetPrivacyEngineInterface):
    def anonymize_sample(self, sample: DatasetSample) -> DatasetSample:
        text = sample.content
        # Mask emails
        text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9\-.]+", "[REDACTED_EMAIL]", text)
        # Mask Phone numbers
        text = re.sub(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[REDACTED_PHONE]", text)
        # Mask SSN / Tax IDs
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", text)
        # Mask Credit Cards
        text = re.sub(r"\b(?:\d{4}[ -]?){3}\d{4}\b", "[REDACTED_CC]", text)

        return DatasetSample(
            sample_id=f"anon_{sample.sample_id}",
            content=text,
            metadata={**sample.metadata, "is_anonymized": True},
            language=sample.language,
            partition=sample.partition
        )


dataset_privacy_engine = DatasetPrivacyEngine()
