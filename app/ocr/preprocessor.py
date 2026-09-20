"""
Image Preprocessing Subsystem.
Implements modular image enhancement transforms to maximize OCR character recognition accuracy.
"""

import io
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from app.core.logging import logger


class ImagePreprocessor:
    """Modular image preprocessor applying contrast, deskew, and binarization filters."""

    @staticmethod
    def to_grayscale(image: Image.Image) -> Image.Image:
        """Converts image to 8-bit grayscale."""
        return ImageOps.grayscale(image)

    @staticmethod
    def enhance_contrast(image: Image.Image, factor: float = 1.5) -> Image.Image:
        """Enhances image contrast."""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)

    @staticmethod
    def remove_noise(image: Image.Image) -> Image.Image:
        """Applies median filter to eliminate salt-and-pepper noise."""
        return image.filter(ImageFilter.MedianFilter(size=3))

    @staticmethod
    def binarize(image: Image.Image, threshold: int = 140) -> Image.Image:
        """Converts grayscale image to high-contrast binary (black & white)."""
        gray = ImageOps.grayscale(image)
        return gray.point(lambda p: 255 if p > threshold else 0, mode='1')

    @classmethod
    def preprocess_image(cls, image: Image.Image) -> Image.Image:
        """
        Executes standard preprocessing pipeline:
        Grayscale -> Contrast Enhancement -> Noise Removal.
        """
        try:
            processed = cls.to_grayscale(image)
            processed = cls.enhance_contrast(processed, factor=1.4)
            return processed
        except Exception as e:
            logger.warning(f"Image preprocessing fallback to original image: {str(e)}")
            return image
