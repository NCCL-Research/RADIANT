import math

import pytest

from radiant.schema import CounterfactualPair, Diagnosis, ParaphrasePair, StudentAttempt


def test_student_attempt_requires_identifiers_and_prompt() -> None:
    with pytest.raises(ValueError):
        StudentAttempt("", "attempt-1", "Solve x + 1 = 2", "1", "x = 1")


def test_student_attempt_rejects_non_string_required_text() -> None:
    with pytest.raises(TypeError):
        StudentAttempt("task-1", "attempt-1", "Prompt", None, "work")  # type: ignore[arg-type]


@pytest.mark.parametrize("confidence", [-0.01, 1.01, math.nan, math.inf, -math.inf, True])
def test_diagnosis_rejects_invalid_confidence(confidence: float) -> None:
    with pytest.raises(ValueError):
        Diagnosis("attempt-1", "sign_error", confidence)


def test_diagnosis_validates_abstention_and_label() -> None:
    with pytest.raises(ValueError):
        Diagnosis("attempt-1", "sign_error", 0.8, abstained=True)
    with pytest.raises(ValueError):
        Diagnosis("attempt-1", "  ", 0.8)


def test_diagnosis_rejects_malformed_evidence_spans() -> None:
    with pytest.raises(ValueError):
        Diagnosis("attempt-1", "sign_error", 0.8, evidence_spans=("",))


def test_paraphrase_pair_requires_distinct_attempts() -> None:
    first = Diagnosis("same", "sign_error", 0.8)
    with pytest.raises(ValueError):
        ParaphrasePair("pair-1", first, first)


def test_counterfactual_pair_requires_distinct_attempts() -> None:
    first = Diagnosis("same", "sign_error", 0.8)
    with pytest.raises(ValueError):
        CounterfactualPair("pair-1", first, first, expected_change=True)


def test_counterfactual_pair_requires_boolean_expectation() -> None:
    first = Diagnosis("baseline", "sign_error", 0.8)
    second = Diagnosis("changed", "conceptual_error", 0.8)
    with pytest.raises(TypeError):
        CounterfactualPair("pair-1", first, second, expected_change=1)  # type: ignore[arg-type]


def test_diagnosis_without_label_must_explicitly_abstain() -> None:
    with pytest.raises(ValueError, match="must be marked as abstained"):
        Diagnosis("attempt-1", None, None)


def test_abstained_diagnosis_may_omit_label() -> None:
    diagnosis = Diagnosis("attempt-1", None, None, abstained=True)
    assert diagnosis.abstained is True
    assert diagnosis.label is None
