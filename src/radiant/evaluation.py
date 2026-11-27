"""Pair-aware evaluation helpers built on validated RADIANT records."""
from __future__ import annotations

from collections.abc import Sequence

from radiant.metrics import counterfactual_response_rate, paraphrase_invariance
from radiant.schema import CounterfactualPair, ParaphrasePair


def _validate_unique_pair_ids(pairs: Sequence[ParaphrasePair | CounterfactualPair]) -> None:
    pair_ids = [pair.pair_id for pair in pairs]
    if len(pair_ids) != len(set(pair_ids)):
        raise ValueError("pair IDs must be unique")


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
            tuple(sorted(pair.paraphrased.normalized_labels)) if not pair.paraphrased.abstained else None
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
