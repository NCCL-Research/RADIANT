import pytest

from radiant.schema import CounterfactualPair, Diagnosis, ParaphrasePair, StudentAttempt


def test_student_attempt_requires_identifiers_and_prompt() -> None:
    with pytest.raises(ValueError):
        StudentAttempt("", "attempt-1", "Solve x + 1 = 2", "1", "x = 1")


def test_diagnosis_validates_confidence_and_abstention() -> None:
    with pytest.raises(ValueError):
        Diagnosis("attempt-1", "sign_error", 1.2)
    with pytest.raises(ValueError):
        Diagnosis("attempt-1", "sign_error", 0.8, abstained=True)


def test_paraphrase_pair_requires_distinct_attempts() -> None:
    first = Diagnosis("same", "sign_error", 0.8)
    with pytest.raises(ValueError):
        ParaphrasePair("pair-1", first, first)


def test_counterfactual_pair_requires_distinct_attempts() -> None:
    first = Diagnosis("same", "sign_error", 0.8)
    with pytest.raises(ValueError):
        CounterfactualPair("pair-1", first, first, expected_change=True)
