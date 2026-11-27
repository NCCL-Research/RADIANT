import pytest

from radiant.metrics import (
    accuracy,
    counterfactual_response_rate,
    coverage,
    macro_f1,
    paraphrase_invariance,
    per_class_metrics,
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


def test_coverage_rejects_non_boolean_flags() -> None:
    with pytest.raises(TypeError, match="booleans"):
        coverage([False, 0, True])  # type: ignore[list-item]


def test_per_class_metrics_reports_precision_recall_f1_and_support() -> None:
    result = per_class_metrics(["a", "a", "b"], ["a", "b", "b"])
    assert result["a"] == {
        "precision": pytest.approx(1.0),
        "recall": pytest.approx(0.5),
        "f1": pytest.approx(2 / 3),
        "support": 2,
    }
    assert result["b"] == {
        "precision": pytest.approx(0.5),
        "recall": pytest.approx(1.0),
        "f1": pytest.approx(2 / 3),
        "support": 1,
    }


def test_per_class_metrics_preserves_explicit_labels_with_zero_support() -> None:
    result = per_class_metrics(["a"], ["a"], labels=["a", "b"])
    assert result["b"] == {
        "precision": pytest.approx(0.0),
        "recall": pytest.approx(0.0),
        "f1": pytest.approx(0.0),
        "support": 0,
    }


def test_per_class_metrics_rejects_empty_or_mismatched_data() -> None:
    with pytest.raises(ValueError):
        per_class_metrics([], [])
    with pytest.raises(ValueError):
        per_class_metrics(["a"], ["a", "b"])



def test_multilabel_exact_match_compares_complete_label_sets() -> None:
    from radiant.metrics import multilabel_exact_match

    assert multilabel_exact_match(
        [("a", "b"), (), ("c",)],
        [("b", "a"), (), ("a",)],
    ) == pytest.approx(2 / 3)


def test_multilabel_per_class_metrics_uses_one_vs_rest_counts() -> None:
    from radiant.metrics import multilabel_per_class_metrics

    result = multilabel_per_class_metrics(
        [("a", "b"), ("a",), ()],
        [("a",), ("a", "b"), ("b",)],
    )
    assert result["a"] == {
        "precision": pytest.approx(1.0),
        "recall": pytest.approx(1.0),
        "f1": pytest.approx(1.0),
        "support": 2,
    }
    assert result["b"] == {
        "precision": pytest.approx(0.5),
        "recall": pytest.approx(0.5),
        "f1": pytest.approx(0.5),
        "support": 1,
    }


def test_multilabel_metrics_reject_strings_and_duplicate_labels() -> None:
    from radiant.metrics import multilabel_exact_match

    with pytest.raises(TypeError, match="not a string"):
        multilabel_exact_match([("a",)], ["a"])  # type: ignore[list-item]
    with pytest.raises(ValueError, match="duplicate"):
        multilabel_exact_match([("a", "a")], [("a",)])
