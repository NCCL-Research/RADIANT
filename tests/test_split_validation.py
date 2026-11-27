import pytest

from radiant.datasets import load_attempts_jsonl, write_attempts_jsonl
from radiant.schema import StudentAttempt
from radiant.split_validation import validate_split_assignments


def attempt(attempt_id: str, split_group_id: str | None = None) -> StudentAttempt:
    return StudentAttempt(
        task_id="fractions-001",
        attempt_id=attempt_id,
        prompt="A task prompt",
        final_answer="1/2",
        intermediate_work="A worked explanation",
        split_group_id=split_group_id,
    )


def test_related_variants_must_remain_in_one_split() -> None:
    cases = [
        attempt("original", "source-1"),
        attempt("paraphrase", "source-1"),
        attempt("counterfactual", "source-1"),
        attempt("independent", "source-2"),
    ]
    validate_split_assignments(cases, {
        "original": "development",
        "paraphrase": "development",
        "counterfactual": "development",
        "independent": "test",
    })


def test_split_validator_rejects_source_group_leakage() -> None:
    cases = [attempt("original", "source-1"), attempt("variant", "source-1")]
    with pytest.raises(ValueError, match="source groups"):
        validate_split_assignments(cases, {"original": "development", "variant": "test"})


def test_split_validator_requires_exact_assignment_coverage() -> None:
    cases = [attempt("a1"), attempt("a2")]
    with pytest.raises(ValueError, match="missing assignments"):
        validate_split_assignments(cases, {"a1": "train"})
    with pytest.raises(ValueError, match="unknown attempt IDs"):
        validate_split_assignments(cases, {"a1": "train", "a2": "test", "extra": "test"})


def test_split_validator_rejects_duplicate_attempt_ids() -> None:
    cases = [attempt("a1"), attempt("a1")]
    with pytest.raises(ValueError, match="unique"):
        validate_split_assignments(cases, {"a1": "train"})


def test_split_group_id_is_validated_and_round_trips(tmp_path) -> None:
    case = attempt("a1", "source-1")
    path = tmp_path / "cases.jsonl"
    write_attempts_jsonl([case], path)
    assert load_attempts_jsonl(path) == [case]
    with pytest.raises(ValueError, match="split_group_id"):
        StudentAttempt("t", "a", "p", "f", "w", split_group_id=" ")
