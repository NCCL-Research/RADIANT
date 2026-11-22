"""Typed records used by the RADIANT evaluation pipeline.

These records describe evaluation inputs and model outputs. They do not
prescribe a diagnosis taxonomy; that taxonomy must be defined and justified
in the research protocol before data collection.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class StudentAttempt:
    """One student's worked attempt at a mathematical task."""

    task_id: str
    attempt_id: str
    prompt: str
    final_answer: str
    intermediate_work: str
    reference_label: str | None = None

    def __post_init__(self) -> None:
        for field_name in ("task_id", "attempt_id", "prompt"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must not be empty")


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
        if not self.attempt_id.strip():
            raise ValueError("attempt_id must not be empty")
        if self.confidence is not None and not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.abstained and self.label is not None:
            raise ValueError("an abstained diagnosis must not include a label")


@dataclass(frozen=True, slots=True)
class ParaphrasePair:
    """Two equivalent presentations of the same underlying reasoning."""

    pair_id: str
    original: Diagnosis
    paraphrased: Diagnosis

    def __post_init__(self) -> None:
        if not self.pair_id.strip():
            raise ValueError("pair_id must not be empty")
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
        if not self.pair_id.strip():
            raise ValueError("pair_id must not be empty")
        if self.baseline.attempt_id == self.counterfactual.attempt_id:
            raise ValueError("counterfactual attempts must have distinct IDs")
