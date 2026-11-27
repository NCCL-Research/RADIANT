"""Pair-aware evaluation helpers built on validated RADIANT records."""
from __future__ import annotations

from collections.abc import Sequence

from radiant.metrics import counterfactual_response_rate, paraphrase_invariance
from radiant.schema import (
    CounterfactualPair,
    Diagnosis,
    ParaphrasePair,
    StudentAttempt,
)


def _validate_unique_pair_ids(pairs: Sequence[ParaphrasePair | CounterfactualPair]) -> None:
    pair_ids = [pair.pair_id for pair in pairs]
    if len(pair_ids) != len(set(pair_ids)):
        raise ValueError("pair IDs must be unique")


def validate_diagnosis_evidence(attempt: StudentAttempt, diagnosis: Diagnosis) -> None:
    """Validate that a diagnosis belongs to an attempt and cites only its submitted work.

    Span matching is exact substring matching against intermediate_work. This
    establishes traceability to the supplied text, not that the span logically
    supports the predicted label.
    """
    if not isinstance(attempt, StudentAttempt):
        raise TypeError("attempt must be a StudentAttempt")
    if not isinstance(diagnosis, Diagnosis):
        raise TypeError("diagnosis must be a Diagnosis")
    if diagnosis.attempt_id != attempt.attempt_id:
        raise ValueError("diagnosis attempt_id must match the supplied attempt")

    spans = list(diagnosis.evidence_spans)
    for item in diagnosis.label_evidence:
        spans.extend(item.evidence_spans)
    if any(span not in attempt.intermediate_work for span in spans):
        raise ValueError("every predicted evidence span must occur in intermediate_work")


def paraphrase_pair_invariance(pairs: Sequence[ParaphrasePair]) -> float:
    """Compute invariance directly from paired Diagnosis records."""
    if not pairs:
        raise ValueError("pairs must not be empty")
    _validate_unique_pair_ids(pairs)
    return paraphrase_invariance(
        [
            tuple(sorted(pair.original.normalized_labels)) if not pair.original.abstained else None
            for pair in pairs
        ],
        [
            tuple(sorted(pair.paraphrased.normalized_labels))
            if not pair.paraphrased.abstained
            else None
            for pair in pairs
        ],
    )


def counterfactual_pair_response_rate(pairs: Sequence[CounterfactualPair]) -> float:
    """Compare observed label/abstention changes with each pair's expectation."""
    if not pairs:
        raise ValueError("pairs must not be empty")
    _validate_unique_pair_ids(pairs)
    observed = [
        (tuple(sorted(pair.baseline.normalized_labels)), pair.baseline.abstained)
        != (tuple(sorted(pair.counterfactual.normalized_labels)), pair.counterfactual.abstained)
        for pair in pairs
    ]
    expected = [pair.expected_change for pair in pairs]
    return counterfactual_response_rate(observed, expected)
