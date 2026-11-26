# Metric definitions

The implementation in src/radiant/metrics.py provides transparent baseline
calculations. These definitions should be reviewed against the final protocol
before any confirmatory analysis.

| Metric | Definition | Important caveat |
|---|---|---|
| Accuracy | Correct labels / all labels | Can conceal class imbalance |
| Macro-F1 | Unweighted mean of per-class F1 | Depends on the defined label set |
| Coverage | Non-abstained outputs / all outputs | Must be reported with selective accuracy |
| Selective accuracy | Correct accepted outputs / accepted outputs | Can look high when coverage is low |
| Paraphrase invariance | Equivalent label outputs / all paired paraphrases | Abstentions count as non-invariant in this implementation |
| Counterfactual response rate | Pairs matching the pre-specified change/no-change expectation / all pairs | Validity depends on carefully controlled counterfactual pairs | Confusion matrix | Counts for each true-label / predicted-label combination | Rows are true labels; columns are predicted labels; label order can be specified explicitly |

## Reporting requirements

- Report denominators and sample sizes with every metric.
- Report class counts and the confusion matrix for classification tasks.
- Report coverage beside selective accuracy.
- Report results by relevant task or diagnosis subgroup where sample sizes permit.
- Use uncertainty intervals appropriate to the sampling and pairing design.
- Keep diagnostic accuracy separate from feedback quality.
- Do not treat these descriptive metrics as proof of causal effects.


## Pair-aware implementation

The `radiant.evaluation` module accepts the typed records in
`radiant.schema`:

- `paraphrase_pair_invariance` compares the two diagnosis labels in each
  `ParaphrasePair`. A prediction that abstains is treated as non-invariant;
  report coverage alongside this score.
- `counterfactual_pair_response_rate` compares each pair's observed output
  change with its pre-specified `expected_change`. An output change means a
  change in either the diagnosis label or abstention state.

These helpers measure agreement with the pair annotations. They do not
validate whether the paraphrases are truly equivalent or whether the
counterfactual manipulation isolates the intended diagnostic cue.
