"""Small, dependency-free metrics for RADIANT.

Metric definitions are deliberately explicit. These functions compute
descriptive quantities; they do not establish that a dataset, label taxonomy,
or experimental design is valid.
"""
from __future__ import annotations

from collections.abc import Sequence


def accuracy(y_true: Sequence[str], y_pred: Sequence[str]) -> float:
    """Return exact-match accuracy for equally sized, non-empty sequences."""
    _validate_equal_nonempty(y_true, y_pred)
    return sum(a == b for a, b in zip(y_true, y_pred, strict=True)) / len(y_true)


def macro_f1(y_true: Sequence[str], y_pred: Sequence[str]) -> float:
    """Return unweighted F1 averaged over labels present in y_true or y_pred."""
    _validate_equal_nonempty(y_true, y_pred)
    labels = sorted(set(y_true) | set(y_pred))
    scores: list[float] = []
    for label in labels:
        tp = sum(a == label and b == label for a, b in zip(y_true, y_pred, strict=True))
        fp = sum(a != label and b == label for a, b in zip(y_true, y_pred, strict=True))
        fn = sum(a == label and b != label for a, b in zip(y_true, y_pred, strict=True))
        denominator = 2 * tp + fp + fn
        scores.append(0.0 if denominator == 0 else (2 * tp) / denominator)
    return sum(scores) / len(scores)


def coverage(abstained: Sequence[bool]) -> float:
    """Fraction of examples receiving a non-abstaining prediction."""
    if not abstained:
        raise ValueError("abstained must not be empty")
    return sum(not value for value in abstained) / len(abstained)


def selective_accuracy(y_true: Sequence[str], y_pred: Sequence[str | None]) -> float:
    """Accuracy among non-abstained predictions; error if all predictions abstain."""
    _validate_equal_nonempty(y_true, y_pred)
    accepted = [(truth, pred) for truth, pred in zip(y_true, y_pred, strict=True) if pred is not None]
    if not accepted:
        raise ValueError("selective accuracy is undefined when every prediction abstains")
    return sum(truth == pred for truth, pred in accepted) / len(accepted)


def paraphrase_invariance(
    labels_a: Sequence[str | None], labels_b: Sequence[str | None]
) -> float:
    """Fraction of paired paraphrases receiving the same non-abstention label.

    Pairs where either output abstains are counted as non-invariant. Report
    coverage alongside this metric so abstention cannot be hidden.
    """
    _validate_equal_nonempty(labels_a, labels_b)
    return sum(
        a is not None and b is not None and a == b
        for a, b in zip(labels_a, labels_b, strict=True)
    ) / len(labels_a)


def counterfactual_response_rate(
    observed_change: Sequence[bool], expected_change: Sequence[bool]
) -> float:
    """Fraction of pairs where the observed change/no-change matches expectation."""
    _validate_equal_nonempty(observed_change, expected_change)
    return sum(
        observed == expected
        for observed, expected in zip(observed_change, expected_change, strict=True)
    ) / len(observed_change)


def _validate_equal_nonempty(first: Sequence[object], second: Sequence[object]) -> None:
    if not first or not second:
        raise ValueError("input sequences must not be empty")
    if len(first) != len(second):
        raise ValueError("input sequences must have equal lengths")
