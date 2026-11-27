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
    if any(not isinstance(value, bool) for value in abstained):
        raise TypeError("abstained values must be booleans")
    return sum(not value for value in abstained) / len(abstained)


def selective_accuracy(y_true: Sequence[str], y_pred: Sequence[str | None]) -> float:
    """Accuracy among non-abstained predictions; error if all predictions abstain."""
    _validate_equal_nonempty(y_true, y_pred)
    accepted = [(truth, pred) for truth, pred in zip(y_true, y_pred, strict=True) if pred is not None]
    if not accepted:
        raise ValueError("selective accuracy is undefined when every prediction abstains")
    return sum(truth == pred for truth, pred in accepted) / len(accepted)


def paraphrase_invariance(
    labels_a: Sequence[str | tuple[str, ...] | None], labels_b: Sequence[str | tuple[str, ...] | None]
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



def confusion_matrix(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    labels: Sequence[str] | None = None,
) -> dict[str, dict[str, int]]:
    """Return counts indexed by true label, then predicted label.

    If labels is supplied, its order is preserved and observations outside
    that label set are rejected. Otherwise, the sorted union is used.
    """
    _validate_equal_nonempty(y_true, y_pred)
    observed = (*y_true, *y_pred)
    if any(not isinstance(value, str) or not value.strip() for value in observed):
        raise ValueError("labels must contain non-empty strings")
    selected = list(labels) if labels is not None else sorted(set(observed))
    if not selected or len(selected) != len(set(selected)):
        raise ValueError("labels must be non-empty and unique")
    if any(not isinstance(value, str) or not value.strip() for value in selected):
        raise ValueError("labels must contain non-empty strings")
    allowed = set(selected)
    if not set(y_true).issubset(allowed) or not set(y_pred).issubset(allowed):
        raise ValueError("observed labels must be included in labels")
    matrix = {truth: {pred: 0 for pred in selected} for truth in selected}
    for truth, pred in zip(y_true, y_pred, strict=True):
        matrix[truth][pred] += 1
    return matrix


def _validate_equal_nonempty(first: Sequence[object], second: Sequence[object]) -> None:
    if not first or not second:
        raise ValueError("input sequences must not be empty")
    if len(first) != len(second):
        raise ValueError("input sequences must have equal lengths")


def per_class_metrics(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    labels: Sequence[str] | None = None,
) -> dict[str, dict[str, float | int]]:
    """Return precision, recall, F1, and support for each requested label."""
    matrix = confusion_matrix(y_true, y_pred, labels=labels)
    results: dict[str, dict[str, float | int]] = {}
    for label, row in matrix.items():
        true_positive = row[label]
        false_positive = sum(
            matrix[other][label] for other in matrix if other != label
        )
        false_negative = sum(
            count for predicted, count in row.items() if predicted != label
        )
        support = sum(row.values())
        precision_denominator = true_positive + false_positive
        recall_denominator = true_positive + false_negative
        precision = (
            true_positive / precision_denominator if precision_denominator else 0.0
        )
        recall = true_positive / recall_denominator if recall_denominator else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall
            else 0.0
        )
        results[label] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": support,
        }
    return results
