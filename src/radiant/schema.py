"""Typed records used by the RADIANT evaluation pipeline.

These records describe evaluation inputs and model outputs. They do not
prescribe a diagnosis taxonomy; that taxonomy must be defined and justified
in the research protocol before data collection.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any


def _require_nonblank(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


@dataclass(frozen=True, slots=True)
class StudentAttempt:
    """One student's worked attempt at a mathematical task."""

    task_id: str
    attempt_id: str
    prompt: str
    final_answer: str
    intermediate_work: str
    reference_label: str | None = None
    split_group_id: str | None = None
    reference_evidence_spans: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("task_id", "attempt_id", "prompt"):
            _require_nonblank(getattr(self, field_name), field_name)
        for field_name in ("final_answer", "intermediate_work"):
            if not isinstance(getattr(self, field_name), str):
                raise TypeError(f"{field_name} must be a string")
        if self.reference_label is not None:
            _require_nonblank(self.reference_label, "reference_label")
        if self.split_group_id is not None:
            _require_nonblank(self.split_group_id, "split_group_id")
        if not isinstance(self.reference_evidence_spans, tuple) or any(
            not isinstance(span, str) or not span.strip()
            for span in self.reference_evidence_spans
        ):
            raise ValueError("reference_evidence_spans must be a tuple of non-empty strings")
        if any(span not in self.intermediate_work for span in self.reference_evidence_spans):
            raise ValueError("each reference evidence span must occur in intermediate_work")


@dataclass(frozen=True, slots=True)
class Diagnosis:
    """A tutor system's structured diagnosis for one student attempt."""

    attempt_id: str
    label: str | None
    confidence: float | None
    evidence_spans: tuple[str, ...] = ()
    explanation: str = ""
    abstained: bool = False
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        _require_nonblank(self.attempt_id, "attempt_id")
        if self.label is not None:
            _require_nonblank(self.label, "label")
        if self.confidence is not None and (
            isinstance(self.confidence, bool)
            or not isinstance(self.confidence, (int, float))
            or not isfinite(self.confidence)
            or not 0.0 <= self.confidence <= 1.0
        ):
            raise ValueError("confidence must be a finite number between 0 and 1")
        if not isinstance(self.evidence_spans, tuple) or any(
            not isinstance(span, str) or not span.strip()
            for span in self.evidence_spans
        ):
            raise ValueError("evidence_spans must be a tuple of non-empty strings")
        if not isinstance(self.explanation, str):
            raise TypeError("explanation must be a string")
        if not isinstance(self.abstained, bool):
            raise TypeError("abstained must be a boolean")
        if self.abstained and self.label is not None:
            raise ValueError("an abstained diagnosis must not include a label")
        if self.metadata is not None and not isinstance(self.metadata, dict):
            raise ValueError("metadata must be a dictionary or None")


@dataclass(frozen=True, slots=True)
class ParaphrasePair:
    """Two equivalent presentations of the same underlying reasoning."""

    pair_id: str
    original: Diagnosis
    paraphrased: Diagnosis

    def __post_init__(self) -> None:
        _require_nonblank(self.pair_id, "pair_id")
        if self.original.attempt_id == self.paraphrased.attempt_id:
            raise ValueError("paraphrase attempts must have distinct IDs")


@dataclass(frozen=True, slots=True)
class CounterfactualPair:
    """A controlled pair differing in a protocol-defined diagnostic cue."""

    pair_id: str
    baseline: Diagnosis
    counterfactual: Diagnosis
    expected_change: bool

    def __post_init__(self) -> None:
        _require_nonblank(self.pair_id, "pair_id")
        if self.baseline.attempt_id == self.counterfactual.attempt_id:
            raise ValueError("counterfactual attempts must have distinct IDs")
        if not isinstance(self.expected_change, bool):
            raise TypeError("expected_change must be a boolean")
