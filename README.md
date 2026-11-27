# RADIANT

**RADIANT — Reasoning Analysis and Diagnostic Investigation for Advanced Neural-informed Tutoring**

A research software project investigating whether AI tutoring systems diagnose mathematical reasoning from students' intermediate work, rather than relying only on final answers.

## Research question

When two learners give the same final answer using different reasoning, does an AI tutor diagnose them differently for the right reasons?

## Research dimensions

The software is being structured to support separate evaluation of:

- Diagnosis accuracy against protocol-defined reference labels.
- Counterfactual diagnostic sensitivity to controlled changes in relevant evidence.
- Paraphrase invariance when the underlying reasoning is unchanged.
- Abstention, coverage, and selective accuracy.
- Evidence spans and explanations, kept distinct from label correctness.
- Feedback quality, evaluated separately from diagnosis accuracy.

The final taxonomy, hypotheses, sampling plan, annotation rubric, and confirmatory analysis must be specified and justified in the research protocol before evaluation.

## Repository structure

```text
src/radiant/
  schema.py       Typed records for attempts, diagnoses, and paired conditions
  datasets.py     Strict JSONL loading and export for benchmark attempts
  metrics.py      Dependency-free metrics, including confusion matrices
  evaluation.py   Pair-aware metrics operating on typed diagnosis records
tests/
  test_package.py
  test_schema.py
  test_metrics.py
  test_evaluation.py
  test_datasets.py
docs/
  DATA_AND_LABEL_SCHEMA.md
  METRIC_DEFINITIONS.md
  EXPERIMENT_LOG_TEMPLATE.md
  RESEARCH_PROTOCOL_TEMPLATE.md
  EXPERIMENT_DESIGN_DRAFT.md
  IMPLEMENTATION_ROADMAP.md
  NOGGIMIGO_CAPABILITY_AUDIT.md
```

## Setup

Requires Python 3.11 or newer.

```bash
python -m pip install -e ".[dev]"
python -m pytest
ruff check src tests
```

GitHub Actions runs the test and lint commands on pushes and pull requests.

## Current implementation status

The repository contains typed research records, baseline metrics, pair-aware evaluation helpers, and JSONL dataset I/O with structural validation.

The JSONL validator checks record shape, required fields, unknown fields, and duplicate attempt identifiers. It does **not** establish that a reference label is scientifically correct or that a paired manipulation is valid.

The benchmark casebook, finalized reasoning taxonomy, model adapter, and real model evaluation are not yet complete. No diagnostic performance results are claimed.

See [the implementation roadmap](docs/IMPLEMENTATION_ROADMAP.md) for planned milestones and research-integrity gates.

## Research integrity and data protection

- Keep research questions, hypotheses, procedures, and analysis decisions explicit.
- Separate synthetic tests, oracle tests, and real model evaluations.
- Record dataset provenance, permissions, annotation decisions, exclusions, and deviations.
- Report denominators, uncertainty, negative findings, and limitations.
- Do not commit identifiable student data or consent records.
