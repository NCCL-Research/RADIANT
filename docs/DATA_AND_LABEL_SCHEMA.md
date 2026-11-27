# Data and label schema

This document defines the minimum structure expected by the software. It does
not define the research label taxonomy. The taxonomy, annotation rubric,
adjudication process, and evidence rules must be justified in the study
protocol before evaluation begins.

## Unit of analysis

The primary record is one student attempt at one mathematical task. Keep the
task prompt, final answer, and intermediate work as separate fields. Do not
infer intermediate reasoning from the final answer.

## Required fields

| Field | Meaning |
|---|---|
| task_id | Stable identifier for the mathematical task |
| attempt_id | Unique identifier for this attempt |
| prompt | Exact task wording presented to the learner |
| final_answer | Learner's submitted final answer |
| intermediate_work | Learner's supplied working or explanation |
| reference_label | Protocol-defined reference diagnosis; may be absent until annotation |
| split_group_id | Optional shared source-case ID for related variants; records without one are treated as independent for split validation |
| reference_evidence_spans | Optional exact quotations from intermediate_work that support the independently assigned reference label |

Use the same split_group_id for an original case and every paraphrase or counterfactual derived from it. Run validate_split_assignments() before evaluation to reject groups spanning multiple splits. Model outputs should be stored separately from reference annotations. A
Diagnosis record contains the predicted label, optional confidence,
evidence spans, explanation, abstention state, and optional run metadata. A
missing diagnosis label must be represented as an explicit abstention; a
non-abstaining diagnosis must carry a label.

## Data protection

- Do not commit names, email addresses, school identifiers, or other direct
  identifiers.
- Do not commit identifiable student work without the required permissions.
- Use study-specific IDs rather than names.
- Keep consent records and any re-identification key outside this repository.
- Document data source, permissions, transformations, exclusions, and retention
  decisions before using any non-synthetic learner data.

## Annotation quality

Before calculating model metrics, specify:

1. The diagnosis categories and operational definitions.
2. What evidence is sufficient for each category.
3. How ambiguous, mixed, and unclassifiable attempts are handled.
4. Whether annotators work independently and how disagreements are resolved.
5. How annotator agreement will be reported.

Evidence spans must be exact substrings of intermediate_work; they record traceable support, not proof that the reference label is correct. Do not treat a model-generated label as ground truth.
