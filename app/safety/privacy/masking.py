"""PII Masking Engine (Partial Obfuscation)."""

from .pii_detector import PIIDetector, PIIType


class DataMasker:
    """Partially masks detected PII while retaining format context."""

    def __init__(self, detector: PIIDetector = None):
        self.detector = detector or PIIDetector()

    def mask_value(self, pii_type: PIIType, value: str) -> str:
        """Applies format-preserving partial masking to a single PII string."""
        if not value:
            return value

        if pii_type == PIIType.SSN:
            # e.g. 123-45-6789 -> ***-**-6789
            clean = value.replace("-", "").replace(" ", "")
            if len(clean) >= 4:
                return f"***-**-{clean[-4:]}"
            return "***-**-****"

        elif pii_type == PIIType.CREDIT_CARD:
            # e.g. 4111 2222 3333 4444 -> ****-****-****-4444
            clean = value.replace("-", "").replace(" ", "")
            if len(clean) >= 4:
                return f"****-****-****-{clean[-4:]}"
            return "****-****-****-****"

        elif pii_type == PIIType.EMAIL:
            # e.g. john.doe@example.com -> j***e@example.com
            parts = value.split("@")
            if len(parts) == 2:
                name, domain = parts
                if len(name) > 2:
                    masked_name = f"{name[0]}***{name[-1]}"
                else:
                    masked_name = f"{name[0]}***"
                return f"{masked_name}@{domain}"
            return "******@***.***"

        elif pii_type == PIIType.PHONE:
            # e.g. +1 555-123-4567 -> +1 (***) ***-4567
            clean = "".join([c for c in value if c.isdigit()])
            if len(clean) >= 4:
                return f"***-***-{clean[-4:]}"
            return "***-***-****"

        elif pii_type in [PIIType.API_KEY, PIIType.AWS_KEY, PIIType.JWT_TOKEN, PIIType.PASSWORD]:
            # e.g. sk-1234567890abcdef -> sk-****...***
            if len(value) > 8:
                return f"{value[:3]}****...{value[-3:]}"
            return "********"

        elif pii_type == PIIType.IP_ADDRESS:
            parts = value.split(".")
            if len(parts) == 4:
                return f"{parts[0]}.{parts[1]}.***.***"
            return "***.***.***.***"

        return "********"

    def mask_text(self, text: str) -> str:
        """Finds and partially masks all detected PII in the text string."""
        if not text:
            return text

        matches = self.detector.detect(text)
        if not matches:
            return text

        # Replace matches in reverse order so string indices remain valid
        result = text
        for match in reversed(matches):
            masked = self.mask_value(match.pii_type, match.raw_value)
            result = result[:match.start] + masked + result[match.end:]

        return result
