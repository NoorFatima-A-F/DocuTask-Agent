"""
Image Efficiency and Layer Analyzer.
"""
from typing import Dict, Any, List
from app.platform_verification.container_verification.models.verification_models import ImageEfficiencyReport


class ImageAnalyzer:
    """Measures container image sizes, layer counts, and unnecessary build artifact leakage."""

    MAX_API_SIZE_MB = 500.0
    MAX_WORKER_SIZE_MB = 700.0
    FORBIDDEN_FILES = {".git", ".pytest_cache", ".coverage", "__pycache__", "tests"}

    def analyze_image(self, image_metadata: Dict[str, Any]) -> ImageEfficiencyReport:
        image_name = image_metadata.get("image_name", "doctask-api:latest")
        compressed_mb = image_metadata.get("compressed_size_mb", 185.0)
        uncompressed_mb = image_metadata.get("uncompressed_size_mb", 420.0)
        layer_count = image_metadata.get("layer_count", 9)
        files = image_metadata.get("contained_files", [])

        detected_unnecessary: List[str] = []
        for f in files:
            for forbidden in self.FORBIDDEN_FILES:
                if forbidden in f:
                    detected_unnecessary.append(f)

        max_limit = self.MAX_WORKER_SIZE_MB if "worker" in image_name else self.MAX_API_SIZE_MB
        meets_target = (uncompressed_mb <= max_limit) and len(detected_unnecessary) == 0

        return ImageEfficiencyReport(
            image_name=image_name,
            compressed_size_mb=round(compressed_mb, 2),
            uncompressed_size_mb=round(uncompressed_mb, 2),
            layer_count=layer_count,
            unnecessary_files_detected=detected_unnecessary,
            meets_efficiency_target=meets_target,
        )
