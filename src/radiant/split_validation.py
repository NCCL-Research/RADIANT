"""Validation helpers for leakage-safe benchmark split assignments."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence

from radiant.schema import StudentAttempt


def validate_split_assignments(
    attempts: Sequence[StudentAttempt],
    assignments: Mapping[str, str],
) -> None:
    """Reject incomplete assignments and source groups spread across splits.

    Attempts without an explicit split_group_id are treated as independent
    source cases. Related paraphrase/counterfactual variants should share the
    same group ID so they remain together in a held-out split.
    """
    attempt_ids = [attempt.attempt_id for attempt in attempts]
    if len(attempt_ids) != len(set(attempt_ids)):
        raise ValueError("attempt IDs must be unique")

    expected_ids = set(attempt_ids)
    assigned_ids = set(assignments)
    missing = expected_ids - assigned_ids
    unknown = assigned_ids - expected_ids
    if missing or unknown:
        details = []
        if missing:
            details.append("missing assignments: " + ", ".join(sorted(missing)))
        if unknown:
            details.append("unknown attempt IDs: " + ", ".join(sorted(unknown)))
        raise ValueError("; ".join(details))

    groups: dict[str, set[str]] = defaultdict(set)
    for attempt in attempts:
        split_id = assignments[attempt.attempt_id]
        if not isinstance(split_id, str) or not split_id.strip():
            raise ValueError(f"split assignment for {attempt.attempt_id!r} must be non-empty")
        group_id = attempt.split_group_id or attempt.attempt_id
        groups[group_id].add(split_id)

    leaked = sorted(group_id for group_id, split_ids in groups.items() if len(split_ids) > 1)
    if leaked:
        raise ValueError("source groups must not cross dataset splits: " + ", ".join(leaked))
