import json

import pytest

from radiant.datasets import load_attempts_jsonl, write_attempts_jsonl
from radiant.schema import StudentAttempt


def attempt(attempt_id: str = "a1") -> StudentAttempt:
    return StudentAttempt(
        task_id="fractions-001",
        attempt_id=attempt_id,
        prompt="A task prompt",
        final_answer="1/2",
        intermediate_work="A worked explanation",
        reference_label="provisional_label",
    )


def test_jsonl_round_trip(tmp_path) -> None:
    path = tmp_path / "attempts.jsonl"
    expected = [attempt(), attempt("a2")]
    write_attempts_jsonl(expected, path)
    assert load_attempts_jsonl(path) == expected


def test_loader_rejects_invalid_json_with_line_number(tmp_path) -> None:
    path = tmp_path / "bad.jsonl"
    path.write_text('{"task_id": }\n', encoding="utf-8")
    with pytest.raises(ValueError, match="bad.jsonl:1: invalid JSON"):
        load_attempts_jsonl(path)


def test_loader_rejects_unknown_fields(tmp_path) -> None:
    record = {
        "task_id": "t1",
        "attempt_id": "a1",
        "prompt": "Prompt",
        "final_answer": "answer",
        "intermediate_work": "work",
        "private_student_name": "Example",
    }
    path = tmp_path / "unknown.jsonl"
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unknown field"):
        load_attempts_jsonl(path)


def test_loader_rejects_duplicate_attempt_ids(tmp_path) -> None:
    path = tmp_path / "duplicate.jsonl"
    record = {
        "task_id": "t1",
        "attempt_id": "a1",
        "prompt": "Prompt",
        "final_answer": "answer",
        "intermediate_work": "work",
    }
    path.write_text(
        json.dumps(record) + "\n" + json.dumps(record) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate attempt_id"):
        load_attempts_jsonl(path)


def test_loader_rejects_non_object_records(tmp_path) -> None:
    path = tmp_path / "array.jsonl"
    path.write_text('[]\n', encoding="utf-8")
    with pytest.raises(TypeError, match="JSON object"):
        load_attempts_jsonl(path)


def test_reference_evidence_spans_round_trip_as_json_arrays(tmp_path) -> None:
    case = StudentAttempt(
        task_id="fractions-001",
        attempt_id="a1",
        prompt="A task prompt",
        final_answer="1/2",
        intermediate_work="divide the numerator and denominator by two",
        reference_evidence_spans=("divide the numerator and denominator by two",),
    )
    path = tmp_path / "evidence.jsonl"
    write_attempts_jsonl([case], path)
    assert load_attempts_jsonl(path) == [case]


def test_loader_rejects_non_array_reference_evidence_spans(tmp_path) -> None:
    record = {
        "task_id": "t1",
        "attempt_id": "a1",
        "prompt": "Prompt",
        "final_answer": "answer",
        "intermediate_work": "work",
        "reference_evidence_spans": "work",
    }
    path = tmp_path / "bad-evidence.jsonl"
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="reference_evidence_spans"):
        load_attempts_jsonl(path)
