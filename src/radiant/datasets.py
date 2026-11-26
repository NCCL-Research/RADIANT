"""JSONL input/output for researcher-authored RADIANT benchmark cases.

This module validates record structure only. It does not validate the
scientific correctness of reference labels or the validity of case pairs.
"""
from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import asdict
from pathlib import Path

from radiant.schema import StudentAttempt

_ALLOWED_FIELDS = {
    "task_id",
    "attempt_id",
    "prompt",
    "final_answer",
    "intermediate_work",
    "reference_label",
    "reference_evidence_spans",
}


def load_attempts_jsonl(path: str | Path) -> list[StudentAttempt]:
    """Load attempts from JSON Lines, rejecting malformed or duplicate records."""
    source = Path(path)
    attempts: list[StudentAttempt] = []
    seen_ids: set[str] = set()

    with source.open("r", encoding="utf-8") as stream:
        for line_number, raw_line in enumerate(stream, start=1):
            if not raw_line.strip():
                continue
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"{source}:{line_number}: invalid JSON: {exc.msg}"
                ) from exc

            if not isinstance(record, dict):
                raise TypeError(f"{source}:{line_number}: each record must be a JSON object")

            unknown = set(record) - _ALLOWED_FIELDS
            if unknown:
                names = ", ".join(sorted(unknown))
                raise ValueError(f"{source}:{line_number}: unknown field(s): {names}")

            missing = _ALLOWED_FIELDS - {"reference_label", "reference_evidence_spans"} - set(record)
            if missing:
                names = ", ".join(sorted(missing))
                raise ValueError(f"{source}:{line_number}: missing required field(s): {names}")

            if "reference_evidence_spans" in record:
                spans = record["reference_evidence_spans"]
                if not isinstance(spans, list):
                    raise TypeError("reference_evidence_spans must be a JSON array")
                record["reference_evidence_spans"] = tuple(spans)

            try:
                attempt = StudentAttempt(**record)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"{source}:{line_number}: {exc}") from exc

            if attempt.attempt_id in seen_ids:
                raise ValueError(
                    f"{source}:{line_number}: duplicate attempt_id "
                    f"{attempt.attempt_id!r}"
                )
            seen_ids.add(attempt.attempt_id)
            attempts.append(attempt)

    return attempts


def write_attempts_jsonl(
    attempts: Iterable[StudentAttempt], path: str | Path
) -> None:
    """Write attempts as UTF-8 JSON Lines, rejecting duplicate attempt IDs."""
    destination = Path(path)
    seen_ids: set[str] = set()

    with destination.open("w", encoding="utf-8", newline="\n") as stream:
        for attempt in attempts:
            if not isinstance(attempt, StudentAttempt):
                raise TypeError("all records must be StudentAttempt instances")
            if attempt.attempt_id in seen_ids:
                raise ValueError(f"duplicate attempt_id {attempt.attempt_id!r}")
            seen_ids.add(attempt.attempt_id)
            stream.write(json.dumps(asdict(attempt), ensure_ascii=False) + "\n")
