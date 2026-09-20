"""
Research Validation & Independent Scientific Verification Framework (RVISF)
Phase 36: Public Benchmark Dataset Suite

Provides standard schemas, evaluation protocols, ground truth loaders, and metrics
for canonical public document processing datasets:
- FUNSD (Form Understanding in Noisy Scanned Documents)
- CORD (Consolidated Receipt Dataset)
- SROIE (Scanned Receipts OCR and Information Extraction)
- DocVQA (Document Visual Question Answering)
- RVL-CDIP (Ryerson Vision Lab Complex Document Information Processing)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class DatasetType(str, Enum):
    FUNSD = "FUNSD"
    CORD = "CORD"
    SROIE = "SROIE"
    DOCVQA = "DocVQA"
    RVL_CDIP = "RVL-CDIP"


@dataclass(frozen=True)
class BoundingBox:
    """Normalized or pixel bounding box [x0, y0, x1, y1]."""
    x0: float
    y0: float
    x1: float
    y1: float

    def area(self) -> float:
        return max(0.0, self.x1 - self.x0) * max(0.0, self.y1 - self.y0)

    def iou(self, other: BoundingBox) -> float:
        """Calculate Intersection over Union (IoU) with another bounding box."""
        ix0 = max(self.x0, other.x0)
        iy0 = max(self.y0, other.y0)
        ix1 = min(self.x1, other.x1)
        iy1 = min(self.y1, other.y1)

        intersection_w = max(0.0, ix1 - ix0)
        intersection_h = max(0.0, iy1 - iy0)
        intersection = intersection_w * intersection_h

        union = self.area() + other.area() - intersection
        return intersection / union if union > 0.0 else 0.0


@dataclass
class GroundTruthItem:
    """A single annotated entity or field in a document dataset."""
    item_id: str
    label: str
    text: str
    bbox: Optional[BoundingBox] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PublicDatasetCard:
    """Research dataset card compliant with MLCommons and Data Cards Playbook."""
    dataset_name: str
    dataset_type: DatasetType
    version: str
    homepage: str
    citation: str
    license_type: str
    num_samples_test: int
    num_samples_train: int
    primary_task: str
    primary_metric: str  # e.g., "Entity F1", "ANLS", "Top-1 Accuracy"
    supported_languages: List[str]
    ethical_risk_level: str


@dataclass
class DatasetBenchmarkEvaluation:
    """Results of evaluating an engine against a public benchmark dataset."""
    dataset_name: str
    dataset_type: DatasetType
    total_samples: int
    precision: float
    recall: float
    f1_score: float
    exact_match_ratio: float
    anls_score: Optional[float] = None  # Average Normalized Levenshtein Similarity (for DocVQA)
    status: str = "PASS"
    details: Dict[str, Any] = field(default_factory=dict)


class PublicBenchmarkSuite:
    """
    Standardized suite of public document understanding benchmark datasets.
    """

    DATASET_CARDS: Dict[DatasetType, PublicDatasetCard] = {
        DatasetType.FUNSD: PublicDatasetCard(
            dataset_name="FUNSD: Form Understanding in Noisy Scanned Documents",
            dataset_type=DatasetType.FUNSD,
            version="1.0",
            homepage="https://guillaumejaume.github.io/FUNSD/",
            citation="Jaume et al., ICDAR-W 2019",
            license_type="CC BY-NC-SA 4.0",
            num_samples_test=50,
            num_samples_train=149,
            primary_task="Key-Value Extraction & Form Layout Analysis",
            primary_metric="Entity F1",
            supported_languages=["en"],
            ethical_risk_level="LOW"
        ),
        DatasetType.CORD: PublicDatasetCard(
            dataset_name="CORD: Consolidated Receipt Dataset for Post-OCR Parsing",
            dataset_type=DatasetType.CORD,
            version="1.0",
            homepage="https://github.com/clovaai/cord",
            citation="Park et al., NeurIPS-W 2019",
            license_type="CC BY-NC 4.0",
            num_samples_test=100,
            num_samples_train=800,
            primary_task="Receipt Key Information Extraction",
            primary_metric="Entity F1",
            supported_languages=["id", "en"],
            ethical_risk_level="LOW"
        ),
        DatasetType.SROIE: PublicDatasetCard(
            dataset_name="SROIE: Scanned Receipts OCR and Information Extraction",
            dataset_type=DatasetType.SROIE,
            version="2019",
            homepage="https://rrc.cvc.uab.es/?ch=13",
            citation="Huang et al., ICDAR 2019 Competition",
            license_type="Academic Research Only",
            num_samples_test=347,
            num_samples_train=626,
            primary_task="4-Field Extraction (Company, Date, Address, Total)",
            primary_metric="Entity F1",
            supported_languages=["en"],
            ethical_risk_level="LOW"
        ),
        DatasetType.DOCVQA: PublicDatasetCard(
            dataset_name="DocVQA: Document Visual Question Answering",
            dataset_type=DatasetType.DOCVQA,
            version="1.0",
            homepage="https://www.docvqa.org/",
            citation="Mathew et al., WACV 2021",
            license_type="CC BY 4.0",
            num_samples_test=5188,
            num_samples_train=39463,
            primary_task="Question Answering on Document Images",
            primary_metric="ANLS",
            supported_languages=["en"],
            ethical_risk_level="LOW"
        ),
        DatasetType.RVL_CDIP: PublicDatasetCard(
            dataset_name="RVL-CDIP: Complex Document Information Processing",
            dataset_type=DatasetType.RVL_CDIP,
            version="1.0",
            homepage="https://www.cs.cmu.edu/~aharley/rvl-cdip/",
            citation="Harley et al., ICDAR 2015",
            license_type="Public Domain / Academic",
            num_samples_test=40000,
            num_samples_train=320000,
            primary_task="16-Class Document Image Classification",
            primary_metric="Top-1 Accuracy",
            supported_languages=["en"],
            ethical_risk_level="LOW"
        ),
    }

    @classmethod
    def get_dataset_card(cls, dataset_type: DatasetType) -> PublicDatasetCard:
        if dataset_type not in cls.DATASET_CARDS:
            raise KeyError(f"Unknown dataset type: {dataset_type}")
        return cls.DATASET_CARDS[dataset_type]

    @staticmethod
    def calculate_anls(prediction: str, ground_truth: str, threshold: float = 0.5) -> float:
        """
        Calculate Normalized Levenshtein Similarity (NLS) for DocVQA:
        NLS = 1 - d(pred, gt) / max(|pred|, |gt|) if d/max < threshold else 0.0
        """
        p = prediction.strip().lower()
        g = ground_truth.strip().lower()
        if p == g:
            return 1.0
        if not p or not g:
            return 0.0

        # Levenshtein distance calculation
        len_p, len_g = len(p), len(g)
        dp = [[0] * (len_g + 1) for _ in range(len_p + 1)]
        for i in range(len_p + 1):
            dp[i][0] = i
        for j in range(len_g + 1):
            dp[0][j] = j

        for i in range(1, len_p + 1):
            for j in range(1, len_g + 1):
                cost = 0 if p[i - 1] == g[j - 1] else 1
                dp[i][j] = min(
                    dp[i - 1][j] + 1,      # deletion
                    dp[i][j - 1] + 1,      # insertion
                    dp[i - 1][j - 1] + cost # substitution
                )

        dist = dp[len_p][len_g]
        max_len = max(len_p, len_g)
        norm_dist = dist / max_len

        return 1.0 - norm_dist if norm_dist < threshold else 0.0

    @classmethod
    def evaluate_predictions(
        cls,
        dataset_type: DatasetType,
        predictions: List[Dict[str, str]],
        ground_truth: List[Dict[str, str]]
    ) -> DatasetBenchmarkEvaluation:
        """
        Evaluate predictions against ground truth pairs.
        Each item is a dict of {field_name: text_value}.
        """
        if len(predictions) != len(ground_truth):
            raise ValueError(f"Length mismatch: {len(predictions)} predictions vs {len(ground_truth)} truth items")

        if not ground_truth:
            return DatasetBenchmarkEvaluation(
                dataset_name=dataset_type.value,
                dataset_type=dataset_type,
                total_samples=0,
                precision=0.0,
                recall=0.0,
                f1_score=0.0,
                exact_match_ratio=0.0,
                status="INSUFFICIENT_EVIDENCE"
            )

        tp = 0
        fp = 0
        fn = 0
        exact_matches = 0
        anls_scores: List[float] = []

        for pred_dict, gt_dict in zip(predictions, ground_truth):
            sample_exact = True
            all_keys = set(pred_dict.keys()).union(set(gt_dict.keys()))

            for k in all_keys:
                p_val = pred_dict.get(k, "").strip().lower()
                g_val = gt_dict.get(k, "").strip().lower()

                if p_val and g_val:
                    if p_val == g_val:
                        tp += 1
                    else:
                        fp += 1
                        fn += 1
                        sample_exact = False
                    if dataset_type == DatasetType.DOCVQA:
                        anls_scores.append(cls.calculate_anls(p_val, g_val))
                elif p_val and not g_val:
                    fp += 1
                    sample_exact = False
                elif not p_val and g_val:
                    fn += 1
                    sample_exact = False

            if sample_exact:
                exact_matches += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        emr = exact_matches / len(ground_truth) if ground_truth else 0.0
        mean_anls = sum(anls_scores) / len(anls_scores) if anls_scores else None

        return DatasetBenchmarkEvaluation(
            dataset_name=dataset_type.value,
            dataset_type=dataset_type,
            total_samples=len(ground_truth),
            precision=precision,
            recall=recall,
            f1_score=f1,
            exact_match_ratio=emr,
            anls_score=mean_anls,
            status="PASS" if f1 >= 0.80 else "VALIDATION_FAILED",
            details={"tp": tp, "fp": fp, "fn": fn, "exact_matches": exact_matches}
        )
