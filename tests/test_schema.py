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
def test_student_attempt_evidence_spans_must_be_exact_work_substrings() -> None:
    attempt = StudentAttempt(
        "task-1", "attempt-1", "Prompt", "answer", "first step; second step",
        reference_evidence_spans=("first step", "second step"),
    )
    assert attempt.reference_evidence_spans == ("first step", "second step")
    with pytest.raises(ValueError, match="must occur in intermediate_work"):
        StudentAttempt(
            "task-1", "attempt-2", "Prompt", "answer", "first step",
            reference_evidence_spans=("invented evidence",),
        )
    with pytest.raises(ValueError, match="non-empty strings"):
        StudentAttempt(
            "task-1", "attempt-3", "Prompt", "answer", "work",
            reference_evidence_spans=("",),
        )


from radiant.schema import ReferenceDiagnosis


def test_reference_diagnoses_support_multiple_labels_with_label_specific_evidence() -> None:
    attempt = StudentAttempt(
        "fractions-001",
        "attempt-multi",
        "Simplify 2/4",
        "1/2",
        "I add 2 + 4 to get 6; then write 1/2.",
        reference_diagnoses=(
            ReferenceDiagnosis("invalid_operation", ("I add 2 + 4 to get 6",)),
            ReferenceDiagnosis("unsupported_conclusion", ("then write 1/2",)),
        ),
        primary_label="invalid_operation",
        evidence_status="sufficient",
    )
    assert attempt.reference_labels == ("invalid_operation", "unsupported_conclusion")
    assert attempt.primary_label == "invalid_operation"


def test_reference_diagnosis_requires_evidence_from_attempt_work() -> None:
    with pytest.raises(ValueError, match="must occur in intermediate_work"):
        StudentAttempt(
            "fractions-001",
            "attempt-bad-evidence",
            "Simplify 2/4",
            "1/2",
            "I add 2 + 4.",
            reference_diagnoses=(
                ReferenceDiagnosis("invalid_operation", ("I multiply 2 by 4",)),
            ),
        )


def test_primary_label_must_be_one_of_reference_labels() -> None:
    with pytest.raises(ValueError, match="primary_label must be one"):
        StudentAttempt(
            "algebra-001",
            "attempt-primary",
            "Solve x + 1 = 2",
            "x = 1",
            "Subtract one from both sides.",
            reference_diagnoses=(
                ReferenceDiagnosis("valid_transformation", ("Subtract one from both sides",)),
            ),
            primary_label="unrelated_label",
        )


def test_insufficient_evidence_cannot_carry_a_reference_diagnosis() -> None:
    with pytest.raises(ValueError, match="must not have reference diagnoses"):
        StudentAttempt(
            "algebra-001",
            "attempt-insufficient",
            "Solve x + 1 = 2",
            "1",
            "placeholder",
            reference_diagnoses=(
                ReferenceDiagnosis("sign_error", ("placeholder",)),
            ),
            evidence_status="insufficient",
        )


def test_legacy_single_label_is_exposed_as_one_reference_label() -> None:
    attempt = StudentAttempt("t1", "a1", "Prompt", "answer", "work", reference_label="legacy")
    assert attempt.reference_labels == ("legacy",)
