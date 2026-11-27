import pytest

from radiant.evaluation import (
    counterfactual_pair_response_rate,
    paraphrase_pair_invariance,
)
from radiant.metrics import confusion_matrix
from radiant.schema import CounterfactualPair, Diagnosis, ParaphrasePair


def diagnosis(attempt_id: str, label: str | None, abstained: bool = False) -> Diagnosis:
    return Diagnosis(attempt_id=attempt_id, label=label, confidence=None, abstained=abstained)


def test_confusion_matrix_uses_true_rows_and_predicted_columns() -> None:
    assert confusion_matrix(["a", "a", "b"], ["a", "b", "b"]) == {
        "a": {"a": 1, "b": 1},
        "b": {"a": 0, "b": 1},
    }


def test_confusion_matrix_preserves_explicit_label_order_and_zeroes() -> None:
    assert confusion_matrix(["b"], ["b"], labels=["b", "a"]) == {
        "b": {"b": 1, "a": 0},
        "a": {"b": 0, "a": 0},
    }


def test_confusion_matrix_rejects_unknown_label() -> None:
    with pytest.raises(ValueError):
        confusion_matrix(["a"], ["b"], labels=["a"])


def test_pairwise_paraphrase_invariance_uses_records() -> None:
    pairs = [
        ParaphrasePair("p1", diagnosis("a1", "sign_error"), diagnosis("a2", "sign_error")),
        ParaphrasePair("p2", diagnosis("b1", "fraction_error"), diagnosis("b2", "sign_error")),
        ParaphrasePair("p3", diagnosis("c1", None, True), diagnosis("c2", "other")),
    ]
    assert paraphrase_pair_invariance(pairs) == pytest.approx(1 / 3)


def test_pairwise_counterfactual_response_rate_uses_label_and_abstention() -> None:
    pairs = [
        CounterfactualPair("c1", diagnosis("a", "sign_error"), diagnosis("b", "fraction_error"), True),
        CounterfactualPair("c2", diagnosis("c", "sign_error"), diagnosis("d", "sign_error"), False),
        CounterfactualPair("c3", diagnosis("e", "sign_error"), diagnosis("f", None, True), False),
    ]
    assert counterfactual_pair_response_rate(pairs) == pytest.approx(2 / 3)


def test_pair_metrics_reject_empty_input() -> None:
    with pytest.raises(ValueError):
        paraphrase_pair_invariance([])
    with pytest.raises(ValueError):
        counterfactual_pair_response_rate([])


def test_pair_metrics_reject_duplicate_pair_ids() -> None:
    first = diagnosis("a", "sign_error")
    second = diagnosis("b", "sign_error")
    duplicate_paraphrases = [
        ParaphrasePair("same-pair", first, second),
        ParaphrasePair("same-pair", diagnosis("c", "x"), diagnosis("d", "x")),
    ]
    duplicate_counterfactuals = [
        CounterfactualPair("same-pair", first, second, False),
        CounterfactualPair("same-pair", diagnosis("c", "x"), diagnosis("d", "y"), True),
    ]
    with pytest.raises(ValueError, match="pair IDs must be unique"):
        paraphrase_pair_invariance(duplicate_paraphrases)
    with pytest.raises(ValueError, match="pair IDs must be unique"):
        counterfactual_pair_response_rate(duplicate_counterfactuals)


def test_paraphrase_invariance_compares_complete_unordered_label_sets() -> None:
    first = Diagnosis(
        "multi-a", None, 0.8, labels=("invalid_operation", "unsupported_conclusion")
    )
    second = Diagnosis(
        "multi-b", None, 0.8, labels=("unsupported_conclusion", "invalid_operation")
    )
    assert paraphrase_pair_invariance([ParaphrasePair("multi-pair", first, second)]) == 1.0


def test_counterfactual_pair_detects_multilabel_set_change() -> None:
    baseline = Diagnosis("multi-base", None, 0.8, labels=("invalid_operation",))
    changed = Diagnosis(
        "multi-changed", None, 0.8, labels=("invalid_operation", "unsupported_conclusion")
    )
    pair = CounterfactualPair("multi-cf", baseline, changed, expected_change=True)
    assert counterfactual_pair_response_rate([pair]) == 1.0


def test_predicted_evidence_spans_must_occur_in_the_attempt_work() -> None:
    from radiant.evaluation import validate_diagnosis_evidence
    from radiant.schema import LabelEvidence, StudentAttempt

    attempt = StudentAttempt(
        "task-1", "attempt-1", "Simplify 2/4", "1/2",
        "I add the numerator and denominator: 2 + 4 = 6.",
    )
    diagnosis = Diagnosis(
        "attempt-1", None, 0.8,
        labels=("invalid_operation",),
        label_evidence=(
            LabelEvidence("invalid_operation", ("2 + 4 = 6",)),
        ),
    )
    validate_diagnosis_evidence(attempt, diagnosis)


def test_predicted_evidence_rejects_spans_not_in_attempt_work() -> None:
    from radiant.evaluation import validate_diagnosis_evidence
    from radiant.schema import LabelEvidence, StudentAttempt

    attempt = StudentAttempt(
        "task-1", "attempt-1", "Simplify 2/4", "1/2",
        "I add the numerator and denominator.",
    )
    diagnosis = Diagnosis(
        "attempt-1", None, 0.8,
        labels=("invalid_operation",),
        label_evidence=(
            LabelEvidence("invalid_operation", ("I multiplied 2 by 4",)),
        ),
    )
    with pytest.raises(ValueError, match="must occur in intermediate_work"):
        validate_diagnosis_evidence(attempt, diagnosis)


def test_predicted_evidence_rejects_mismatched_attempt_ids() -> None:
    from radiant.evaluation import validate_diagnosis_evidence
    from radiant.schema import StudentAttempt

    attempt = StudentAttempt("task-1", "attempt-1", "Prompt", "answer", "work")
    diagnosis = Diagnosis("different-attempt", None, None, abstained=True)
    with pytest.raises(ValueError, match="must match"):
        validate_diagnosis_evidence(attempt, diagnosis)


def test_predicted_legacy_evidence_spans_are_also_validated() -> None:
    from radiant.evaluation import validate_diagnosis_evidence
    from radiant.schema import StudentAttempt

    attempt = StudentAttempt("task-1", "attempt-1", "Prompt", "answer", "submitted work")
    diagnosis = Diagnosis(
        "attempt-1", "some_label", 0.7, evidence_spans=("invented span",)
    )
    with pytest.raises(ValueError, match="must occur in intermediate_work"):
        validate_diagnosis_evidence(attempt, diagnosis)
