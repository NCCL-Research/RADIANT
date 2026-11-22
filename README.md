# RADIANT

**RADIANT — Reasoning Analysis and Diagnostic Investigation for Advanced Neural-informed Tutoring**

A research software project investigating whether AI tutoring systems diagnose mathematical reasoning from students' intermediate work, rather than relying only on final answers.

## Research status

This repository contains an initial software foundation: typed evaluation records, baseline metric functions, unit tests, and documentation templates. It does not yet contain a validated experimental protocol, a completed dataset, or real model-evaluation results. No performance claims should be inferred from the scaffold or its unit tests.

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
  metrics.py      Dependency-free baseline metrics
tests/
  test_package.py
  test_schema.py
  test_metrics.py
docs/
  DATA_AND_LABEL_SCHEMA.md
  METRIC_DEFINITIONS.md
  EXPERIMENT_LOG_TEMPLATE.md
  RESEARCH_PROTOCOL_TEMPLATE.md
  DEVELOPMENT_LOG.md
AI_ASSISTANCE.md  Development provenance and assistance record
```

## Setup

Requires Python 3.11 or newer.

```bash
python -m pip install -e ".[dev]"
python -m pytest
ruff check src tests
```

GitHub Actions runs the test and lint commands on pushes and pull requests.

## Research integrity and data protection

- Keep research questions, hypotheses, procedures, and analysis decisions explicit.
- Separate synthetic tests, oracle tests, and real model evaluations.
- Record dataset provenance, permissions, annotation decisions, exclusions, and deviations.
- Report denominators, uncertainty, negative findings, and limitations.
- Do not commit identifiable student data or consent records.
- Document AI assistance accurately.

## Development history

This repository is a fresh implementation successor to the earlier RADIANT repository. The predecessor's history is not erased or represented as unaided work. See [AI_ASSISTANCE.md](AI_ASSISTANCE.md) for the provenance record and [docs/DEVELOPMENT_LOG.md](docs/DEVELOPMENT_LOG.md) for verified milestones.
