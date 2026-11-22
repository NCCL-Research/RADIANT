import pytest

from radiant.metrics import (
    accuracy,
    counterfactual_response_rate,
    coverage,
    macro_f1,
    paraphrase_invariance,
    selective_accuracy,
)


def test_accuracy() -> None:
    assert accuracy(["a", "b", "a"], ["a", "a", "a"]) == pytest.approx(2 / 3)


def test_macro_f1_uses_unweighted_label_average() -> None:
    assert macro_f1(["a", "a", "b"], ["a", "b", "b"]) == pytest.approx(2 / 3)


def test_coverage_and_selective_accuracy() -> None:
    abstained = [False, True, False, False]
    assert coverage(abstained) == pytest.approx(0.75)
    assert selective_accuracy(["x", "y", "x", "z"], ["x", None, "wrong", "z"]) == pytest.approx(2 / 3)


def test_paraphrase_invariance_counts_abstention_as_non_invariant() -> None:
    assert paraphrase_invariance(["a", "b", None], ["a", "c", "d"]) == pytest.approx(1 / 3)


def test_counterfactual_response_rate() -> None:
    assert counterfactual_response_rate([True, False, True], [True, False, False]) == pytest.approx(2 / 3)


def test_metrics_reject_mismatched_lengths() -> None:
    with pytest.raises(ValueError):
        accuracy(["a"], ["a", "b"])


def test_selective_accuracy_rejects_all_abstentions() -> None:
    with pytest.raises(ValueError):
        selective_accuracy(["a"], [None])
