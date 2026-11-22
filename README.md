# RADIANT-Research

**RADIANT — Reasoning Analysis and Diagnostic Investigation for Advanced Neural-informed Tutoring**

A fresh implementation repository for the RADIANT research programme: investigating whether AI tutoring systems can diagnose mathematical reasoning accurately from students' intermediate work, rather than relying only on final answers.

## Relationship to the predecessor

This repository is an independently developed successor to [Noggin-Labs/RADIANT](https://github.com/Noggin-Labs/RADIANT). It has a separate Git history and is intended for a ground-up implementation. The predecessor remains available as the historical record of earlier development, including AI-assisted contributions. This repository does not erase or replace that history.

The research design and evaluation goals are being carried forward for independent review and refinement. No claim is made that the new implementation has already reproduced earlier results.

## Research status

This repository is an initial scaffold. It does not yet contain a validated experimental implementation or completed model evaluation. Results will be reported only after the relevant experiments have actually been run and independently checked.

## Development principles

- Keep research questions, hypotheses, procedures, and analysis decisions explicit.
- Separate synthetic tests, oracle tests, and real model evaluations.
- Record dataset provenance, annotation decisions, exclusions, and deviations.
- Test metric implementations against controlled examples before using them for claims.
- Preserve negative, null, and inconclusive findings.
- Document AI assistance accurately.

## Repository layout

```text
src/radiant/       Python package
tests/             Automated tests
docs/              Development and reproducibility records
data/              Dataset documentation; do not commit private student data
```

## Development

Requires Python 3.11 or newer.

```bash
python -m pip install -e ".[dev]"
pytest
```

## Provenance and AI assistance

See [AI_ASSISTANCE.md](AI_ASSISTANCE.md) for the relationship to the predecessor and the assistance used to establish this repository.
