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
    paraphrase_invariance,
    selective_accuracy,
)
from radiant.split_validation import validate_split_assignments
from radiant.schema import (
    CounterfactualPair,
    Diagnosis,
    ParaphrasePair,
    StudentAttempt,
)

__version__ = "0.1.0"

__all__ = [
    "CounterfactualPair",
    "Diagnosis",
    "ParaphrasePair",
    "StudentAttempt",
    "accuracy",
    "confusion_matrix",
    "counterfactual_pair_response_rate",
    "counterfactual_response_rate",
    "coverage",
    "macro_f1",
    "paraphrase_invariance",
    "paraphrase_pair_invariance",
    "selective_accuracy",
    "validate_split_assignments",
]
