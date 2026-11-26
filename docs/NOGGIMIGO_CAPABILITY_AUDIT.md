# Noggimigo capability audit for RADIANT

**Audit status:** Source-level review of the public `NCCL-Research/noggimigo`
repository at the `main` branch on 2026-11-26. This is not a runtime
benchmark, independent code review, or evaluation of tutoring effectiveness.
Recheck the referenced source before freezing any study configuration.

## Decision summary

Noggimigo is a candidate system under study, but the currently documented
implementation is **not yet eligible for RADIANT's primary reasoning-diagnosis
accuracy comparison**.

The current code supports deterministic answer verification, structured
tutoring feedback, and a separate evidence/inference record. It does not expose
a demonstrated end-to-end contract that maps arbitrary supplied intermediate
work to a frozen RADIANT reference-label taxonomy.

This is an eligibility decision for a specific analysis, not a judgement that
Noggimigo is generally ineffective or that its other capabilities are
uninteresting.

## Source-level findings

| Capability | Source-level observation | RADIANT status |
|---|---|---|
| Deterministic final-answer verification | `answer_verifier.verify_answer(student, expected)` parses a narrow answer format and checks equivalence. | Present; suitable for an answer-verification control, not a reasoning diagnosis. |
| Separate intermediate-work input | `NoggimigoSession.submit(answer)` accepts one response string and passes it to the verifier and optional tutor. The session API shown does not expose a distinct `intermediate_work` argument. | Not demonstrated in the session interface. |
| Optional language-model tutoring | `hf_provider.build_messages` receives the prompt and learner response and requests a student-facing message, pedagogical action, and up to three misconception-candidate strings. | Present as candidate tutoring text; not a validated diagnosis output. |
| Authoritative diagnosis label | The session validates and returns the student-facing message and pedagogical action. The inspected session path does not return a protocol-defined diagnosis label. | Not demonstrated. |
| Evidence provenance | `reasoning_evidence.py` distinguishes OBSERVED, VERIFIED, INFERRED, and UNKNOWN records; inferences must cite evidence. | Useful evidence representation; not itself a taxonomy or diagnosis classifier. |
| Domain-specialist analysis | `MathAnswerSpecialist` compares a response with an expected answer and explicitly records that the underlying reasoning is unknown. | Answer-checking baseline; not reasoning diagnosis. |
| Abstention / insufficient evidence | `SpecialistResult` includes `INSUFFICIENT_EVIDENCE`; the answer specialist uses it for missing expected answers or uninterpretable answers. | Partial capability; must be mapped to a frozen RADIANT output contract before scoring. |
| Exact evidence spans | Evidence records can store supplied text and source references, but the reviewed session path does not emit an aligned evidence-span diagnosis for each attempt. | Not demonstrated end-to-end. |
| Reproducible version/configuration | Repository version, model identifier, prompt, provider, and runtime configuration can in principle be recorded, but an evaluation adapter and frozen run manifest are not yet implemented here. | Requires a separate run-capture implementation. |

## Implications for RADIANT

Until the missing interface is implemented and tested:

1. Include Noggimigo in the system capability audit and report its current
   supported functions.
2. It may be evaluated as an answer-verification or tutoring-feedback
   condition under a separately specified outcome.
3. Do not score its answer-verification result as a reasoning diagnosis.
4. Do not treat free-text `misconception_candidates` as reference labels or
   validated diagnoses.
5. Do not convert an UNKNOWN reasoning record into a guessed label.
6. Do not infer learner traits or cognitive states from its outputs.
7. Keep deterministic and model-assisted Noggimigo conditions separate.

## Adapter requirements before diagnostic-accuracy eligibility

A future adapter must not manufacture missing information. It should:

- preserve the exact task prompt and learner-supplied intermediate work as
  separate fields;
- capture the raw system response and the exact Noggimigo revision/config;
- map only an explicitly documented, taxonomy-compatible label to
  `Diagnosis.label`;
- map an explicit insufficient-evidence result to abstention;
- preserve evidence spans only when they can be traced to the supplied work;
- leave unsupported fields absent or null rather than infer them;
- reject malformed or unsupported outputs with a recorded adapter error;
- include contract tests for correct, incorrect, ambiguous, insufficient, and
  unsupported cases.

The adapter must be tested against fixtures before any live system evaluation.
Passing adapter tests establishes interface behaviour only, not diagnostic
validity.

## Re-audit triggers

Repeat this audit if the Noggimigo session API, reasoning-evidence module,
specialist interfaces, model output schema, or supported curriculum changes.
Record the exact commit SHA and source paths in the frozen RADIANT run manifest.

## Reviewed source paths

- `noggimigo/answer_verifier.py`
- `noggimigo/session.py`
- `noggimigo/hf_provider.py`
- `noggimigo/reasoning_evidence.py`
- `noggimigo/specialists.py`
- `tests/test_reasoning_evidence.py`
- `tests/test_adversarial_integrity.py`
- `README.md`

This audit records source-level capabilities only. It does not report model
performance, user outcomes, or empirical evidence that Noggimigo diagnoses
mathematical reasoning accurately.
