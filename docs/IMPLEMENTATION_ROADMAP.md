# RADIANT implementation roadmap

**Current repository stage:** research-software scaffold with typed records,
baseline metrics, pair-aware evaluation helpers, and tests. The project has
not yet produced model-evaluation results.

## Milestone 1 — trustworthy benchmark data handling

- [x] Define typed attempt and diagnosis records.
- [x] Define baseline classification and pair-aware metrics.
- [x] Add strict JSONL dataset loading and export.
- [ ] Add schema validation tests to continuous integration.
- [ ] Document a versioned benchmark manifest and provenance fields.
- [ ] Create a small researcher-authored pilot casebook after the label
  taxonomy and annotation rules have been specified.

## Milestone 2 — research protocol

- [ ] Review relevant mathematics-education and intelligent-tutoring
  literature to define the scope and candidate reasoning categories.
- [ ] Write operational label definitions with positive, negative, boundary,
  ambiguous, and insufficient-evidence examples.
- [ ] Define independent annotation and adjudication procedures.
- [ ] Freeze the held-out split and prevent paired variants from crossing splits.
- [ ] Specify primary outcomes, uncertainty estimates, and exclusions before
  confirmatory evaluation.

## Milestone 3 — model adapter and reproducible runs

- [ ] Define a versioned adapter contract for structured diagnosis outputs.
- [ ] Implement a scripted fixture adapter for software tests only.
- [ ] Add at least one real model adapter only after its capability audit.
- [ ] Record provider/model identifier, revision where available, prompt
  version, parameters, timestamp, software version, and raw response.
- [ ] Keep fixture outputs clearly separated from real model outputs.

## Milestone 4 — analysis and reporting

- [ ] Add per-class metrics, confusion matrices, coverage, and selective
  accuracy reports.
- [ ] Add pair-level summaries with uncertainty methods appropriate to the
  sampling design.
- [ ] Keep diagnosis correctness, evidence support, explanation quality, and
  feedback usefulness as separate outcomes.
- [ ] Generate a reproducible report from a frozen run manifest.

## Research integrity gates

1. No model performance claims from scripted fixtures or synthetic unit tests.
2. No reference labels derived from model predictions.
3. No real learner data in the repository without the applicable permissions
   and privacy review.
4. No human-participant study, including recruitment of minors, before the
   applicable ethics review, permissions, assent, and fair rules are checked.
5. No generalisation beyond the mathematical topics, systems, prompts, and
   versions actually evaluated.

The roadmap records planned work, not completed results.
