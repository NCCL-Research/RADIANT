"""RADIANT research framework public API."""

from radiant.evaluation import (
    counterfactual_pair_response_rate,
    paraphrase_pair_invariance,
)
from radiant.metrics import (
    accuracy,
    confusion_matrix,
    counterfactual_response_rate,
    coverage,
    macro_f1,
    multilabel_exact_match,
    multilabel_per_class_metrics,
    paraphrase_invariance,
    per_class_metrics,
    selective_accuracy,
)
from radiant.schema import (
    CounterfactualPair,
    Diagnosis,
    LabelEvidence,
    ParaphrasePair,
    ReferenceDiagnosis,
    StudentAttempt,
)
from radiant.split_validation import validate_split_assignments

__version__ = "0.1.0"

__all__ = [
    "CounterfactualPair",
    "Diagnosis",
    "LabelEvidence",
    "ParaphrasePair",
    "ReferenceDiagnosis",
    "StudentAttempt",
    "accuracy",
    "confusion_matrix",
    "counterfactual_pair_response_rate",
    "counterfactual_response_rate",
    "coverage",
    "macro_f1",
    "multilabel_exact_match",
    "multilabel_per_class_metrics",
    "paraphrase_invariance",
    "paraphrase_pair_invariance",
    "per_class_metrics",
    "selective_accuracy",
    "validate_split_assignments",
]
