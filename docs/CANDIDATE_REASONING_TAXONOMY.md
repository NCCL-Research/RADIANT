# RADIANT candidate reasoning taxonomy

**Version:** 0.1 (provisional literature-grounded draft)  
**Status:** Research-design proposal. Not a validated taxonomy, frozen annotation rubric, or completed literature review.

## 1. Purpose and constraint

RADIANT needs labels assignable from the *observable work supplied to a system*. An incorrect final answer alone is not evidence of a particular misconception.

The initial literature supports analysing mathematical errors as potentially meaningful reasoning patterns, while distinguishing systematic errors from slips and recognizing that categories depend on topic and evidence:

- Sleeman (1984), studying 24 students' algebra work, used categories including manipulative, parsing, clerical, and random errors. Follow-up interviews exposed misunderstandings missed by the tutoring system's initial analysis.
- Movshovitz-Hadar, Zaslavsky, and Inbar (1987), as summarized by Schnepper and McCoy, classified errors including misused data, invalid translation from verbal to mathematical form, logically invalid inference, improper use of a definition or theorem, answering the wrong question, and basic-skill errors.
- Mathaba et al. (2024) report Grade 9 algebra patterns including conjoining, cancellation, and problem-solving errors, and distinguish slips from systematic errors.
- Makhubele (2021) reports Grade 8 fraction errors associated with prerequisite concepts, prior knowledge, misconceptions, and misapplied rules.

These sources do **not** establish one universal taxonomy for all mathematics topics. RADIANT should use a small cross-topic coding framework with topic-specific subcodes, and freeze operational definitions only after review and piloting.

## 2. Keep three questions separate

1. **Outcome correctness:** Is the final answer correct?
2. **Observable reasoning:** What does the supplied intermediate work demonstrate?
3. **Evidence sufficiency:** Is there enough visible evidence to assign a reasoning label?

A wrong answer may have insufficient reasoning evidence. A correct answer may contain invalid reasoning that happens to produce the right result. Neither should be collapsed into a simple correct/incorrect diagnosis.

Do not infer a stable learner trait from one isolated attempt. Prefer "the work exhibits..." over "the learner believes..." unless repeated, independently supported evidence and the protocol justify the stronger inference.

## 3. Candidate cross-topic error families

These are candidate families for protocol development, not approved production labels. Each needs topic-specific inclusion, exclusion, and boundary examples before annotation begins.

| Candidate family | Working description | Minimum evidence required |
|---|---|---|
| CONCEPT_OR_REPRESENTATION | Incorrect meaning of a mathematical object, relation, operation, or representation is visible in the work. | A visible statement, diagram, or transformation conflicts with the task's defined mathematical meaning. |
| RULE_MISAPPLICATION | A rule, property, or procedure is applied outside valid conditions or generalized to an incompatible case. | The rule use and the condition making it invalid are both visible. |
| SYMBOL_PARSING_OR_TRANSLATION | Mathematical notation or verbal information is interpreted or translated inconsistently with the task. | A visible parse, substitution, or translation step demonstrates the mismatch. |
| INVALID_INFERENCE_OR_STRATEGY | A conclusion does not follow from preceding statements, or the selected strategy does not address the stated problem. | The relevant premise and conclusion or strategy are visible. |
| PROCEDURAL_TRANSFORMATION | A mathematical operation or transformation is invalid even though the underlying objects appear to be understood. | The specific invalid transformation is identifiable in the written steps. |
| EXECUTION_OR_ARITHMETIC | The reasoning plan is plausibly appropriate, but a local computation or execution step is incorrect. | Enough preceding work is visible to distinguish a local execution error from a conceptual or rule error. |
| TASK_MISMATCH_OR_OFF_TASK | The response solves a different problem, omits the required target, or is not responsive to the task. | The task requirement and response can be directly compared. |

### Distinctions and cautions

- Do not label an isolated arithmetic slip as a misconception.
- Do not classify a step as procedural if the evidence instead shows misunderstanding of the mathematical object or operation.
- Do not infer a parsing error when notation or intermediate work is absent.
- One attempt may contain multiple observable errors. The protocol must decide whether multiple labels are allowed or whether a primary label plus secondary notes is used. The current scalar reference_label field must not silently dictate the research ontology.
- Do not use "random" as a catch-all for unexplained work. If evidence does not support an interpretation, use insufficient evidence.

## 4. Evidence-status coding

Evidence status is separate from the error-family label.

| Status | Meaning | Annotation action |
|---|---|---|
| SUFFICIENT | Work contains the evidence required by an operational definition. | Assign supported label(s) and cite exact evidence spans. |
| AMBIGUOUS | Two or more interpretations remain plausible. | Record alternatives; do not force a single diagnosis. |
| INSUFFICIENT | Work does not expose enough reasoning to support a diagnosis. | Abstain from assigning an error-family label. |
| OUT_OF_SCOPE | Task or reasoning pattern is outside the frozen taxonomy or domain. | Apply a pre-specified exclusion rule and report the count. |

A correct final answer with no working may be INSUFFICIENT for reasoning diagnosis. An incorrect final answer with no interpretable working may also be INSUFFICIENT. These are evidence limitations, not automatically model failures.

## 5. Topic-specific subcodes to investigate

### Fractions

Review these subdomains separately: fraction meaning and representation; part-whole, measurement, quotient, and operator interpretations; magnitude and comparison; equivalence; and operation-specific reasoning.

Makhubele (2021) reports errors associated with prerequisite concepts, prior knowledge, misconceptions, and misapplied rules in Grade 8 fraction tasks. Lee and Boyadzhiev (2020) report difficulties involving fraction definitions, common denominators/least common multiples, and order of operations in a remedial college sample. These findings motivate topic-specific review; they do not justify assuming every incorrect fraction operation reflects the same misconception.

Author candidate examples only after documenting the relevant concept and boundary conditions. Each example needs intended evidence and at least one plausible competing interpretation.

### Introductory algebra

Review separately: interpretation of variables and notation; translation between verbal and symbolic forms; equivalence-preserving transformations; combining or simplifying expressions; application of definitions and properties; and selection and execution of a solution strategy.

Sleeman (1984) provides evidence that parsing and manipulative errors can be distinct in algebra and that interviews can reveal misunderstandings not visible to a system. Mathaba et al. (2024) report conjoining, cancellation, and problem-solving errors in Grade 9 algebra. Exact operational definitions must be checked against the full studies and the tasks RADIANT actually includes.

### Patterns and sequences

**Not yet specified.** This draft's source set is insufficient to propose reliable sequence-specific misconception labels. Do not include sequence cases in a confirmatory taxonomy until a focused literature review and operational definitions are completed.

## 6. Annotation rules to carry into the protocol

1. Annotators see the task prompt and supplied work, but not model identity or model output.
2. Reference labels are assigned independently of every system being evaluated.
3. Every non-abstained label cites an exact span or step where possible.
4. Annotators record the evidence rule satisfied, not merely a label name.
5. Annotators distinguish direct evidence from inference and note plausible alternatives.
6. Ambiguous and insufficient-evidence cases remain explicit categories, not silently discarded.
7. Independent annotation and adjudication occur before model evaluation. The protocol specifies annotator count, qualifications, training, agreement statistic, and adjudication.
8. Taxonomy changes after annotation starts are versioned, justified, and followed by a documented re-annotation decision.

The current reference_evidence_spans field checks whether a span occurs in intermediate_work. That mechanical check establishes traceability to supplied text, not that the span supports the label. Semantic evidence quality needs a separate human-reviewed rubric.

## 7. Open decisions before taxonomy freeze

- Which two topic areas belong in the first benchmark release? Fractions and introductory algebra have a stronger source base in this draft than patterns/sequences.
- Is the annotation unit one attempt or one reasoning step?
- Are multiple simultaneous error-family labels allowed?
- Does the primary label represent the earliest error, the most consequential error, or the error most directly relevant to the task objective?
- How are correct answers reached through invalid reasoning coded?
- How are contradictory work and self-correction represented?
- Which agreement statistic fits the final label structure and prevalence?
- What independent review assesses mathematical and pedagogical plausibility of synthetic cases?

Do not label confirmatory cases until these decisions are resolved in a versioned annotation manual.

## 8. Source register

1. Sleeman, D. (1984). *An Attempt to Understand Students' Understanding of Basic Algebra*. Stanford University, Heuristic Programming Project. ERIC ED258847. https://files.eric.ed.gov/fulltext/ED258847.pdf
2. Movshovitz-Hadar, N., Zaslavsky, O., & Inbar, S. (1987). An empirical classification model for errors in high school mathematics. *Journal for Research in Mathematics Education*, 18(1), 3–14. https://doi.org/10.2307/749532
3. Schnepper, L. C., & McCoy, L. P. (2013; journal issue published 2017). *Analysis of Misconceptions in High School Mathematics*. *Networks: An Online Journal for Teacher Research*, 15(1), Article 7. https://doi.org/10.4148/2470-6353.1066
4. Makhubele, Y. E. (2021). The Analysis of Grade 8 Fractions Errors Displayed by Learners Due to Deficient Mastery of Prerequisite Concepts. *International Electronic Journal of Mathematics Education*, 16(3), em0645. https://doi.org/10.29333/iejme/11004
5. Lee, H.-J., & Boyadzhiev, I. (2020). Underprepared College Students' Understanding of and Misconceptions with Fractions. *International Electronic Journal of Mathematics Education*, 15(3), em0583. https://doi.org/10.29333/iejme/7835
6. Mathaba, P. N., Bayaga, A., Tîrnovan, D., & Bossé, M. J. (2024). Error Analysis in Algebra Learning: Exploring Misconceptions and Cognitive Levels. *Journal on Mathematics Education*, 15(2), 575–592. https://doi.org/10.22342/jme.v15i2.pp575-592

### Source-use limitations

This is a preliminary source register, not a systematic review. The 1987 classification is cited through Schnepper and McCoy; the original article must be obtained and checked before taxonomy freeze. Study populations, curricula, and task formats differ, so reported categories are not universal prevalence estimates. No numerical prevalence claims are made here.
