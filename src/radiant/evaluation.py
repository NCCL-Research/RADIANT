"""Pair-aware evaluation helpers built on validated RADIANT records."""
from __future__ import annotations

from collections.abc import Sequence

from radiant.metrics import counterfactual_response_rate, paraphrase_invariance
from radiant.schema import CounterfactualPair, ParaphrasePair


def paraphrase_pair_invariance(pairs: Sequence[ParaphrasePair]) -> float:
    """Compute invariance directly from paired Diagnosis records."""
    if not pairs:
        raise ValueError("pairs must not be empty")
    return paraphrase_invariance(
        [
            pair.original.label if not pair.original.abstained else None
            for pair in pairs
        ],
        [
            pair.paraphrased.label if not pair.paraphrased.abstained else None
            for pair in pairs
        ],
    )


def counterfactual_pair_response_rate(pairs: Sequence[CounterfactualPair]) -> float:
    """Compare observed label/abstention changes with each pair's expectation."""
    if not pairs:
        raise ValueError("pairs must not be empty")
    observed = [
        (pair.baseline.label, pair.baseline.abstained)
        != (pair.counterfactual.label, pair.counterfactual.abstained)
        for pair in pairs
    ]
    expected = [pair.expected_change for pair in pairs]
    return counterfactual_response_rate(observed, expected)
