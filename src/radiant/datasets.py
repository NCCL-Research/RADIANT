"""JSONL input/output for researcher-authored RADIANT benchmark cases.

This module validates record structure only. It does not validate the
scientific correctness of reference labels or the validity of case pairs.
"""
from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import asdict
from pathlib import Path

from radiant.schema import ReferenceDiagnosis, StudentAttempt

_ALLOWED_FIELDS = {
    "task_id",
    "attempt_id",
    "prompt",
    "final_answer",
    "intermediate_work",
    "reference_label",
    "split_group_id",
    "reference_evidence_spans",
    "reference_diagnoses",
    "primary_label",
    "evidence_status",
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

            optional_fields = {
                "reference_label",
                "split_group_id",
                "reference_evidence_spans",
                "reference_diagnoses",
                "primary_label",
                "evidence_status",
            }
            missing = _ALLOWED_FIELDS - optional_fields - set(record)
            if missing:
                names = ", ".join(sorted(missing))
                raise ValueError(f"{source}:{line_number}: missing required field(s): {names}")

            if "reference_evidence_spans" in record:
                spans = record["reference_evidence_spans"]
                if not isinstance(spans, list):
                    raise TypeError("reference_evidence_spans must be a JSON array")
                record["reference_evidence_spans"] = tuple(spans)

            if "reference_diagnoses" in record:
                diagnoses = record["reference_diagnoses"]
                if not isinstance(diagnoses, list):
                    raise TypeError("reference_diagnoses must be a JSON array")
                normalized = []
                for item in diagnoses:
                    if not isinstance(item, dict):
                        raise TypeError("each reference diagnosis must be a JSON object")
                    if set(item) != {"label", "evidence_spans"}:
                        raise ValueError(
                            "each reference diagnosis must contain exactly "
                            "label and evidence_spans"
                        )
                    spans = item["evidence_spans"]
                    if not isinstance(spans, list):
                        raise TypeError("diagnosis evidence_spans must be a JSON array")
                    normalized.append(
                        ReferenceDiagnosis(label=item["label"], evidence_spans=tuple(spans))
                    )
                record["reference_diagnoses"] = tuple(normalized)

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

    with destination.open("w", encoding="utf-8", newline="\\n") as stream:
        for attempt in attempts:
            if not isinstance(attempt, StudentAttempt):
                raise TypeError("all records must be StudentAttempt instances")
            if attempt.attempt_id in seen_ids:
                raise ValueError(f"duplicate attempt_id {attempt.attempt_id!r}")
            seen_ids.add(attempt.attempt_id)
            stream.write(json.dumps(asdict(attempt), ensure_ascii=False) + "\\n")
