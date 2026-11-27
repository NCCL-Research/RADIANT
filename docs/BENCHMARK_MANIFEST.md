# Benchmark manifest

RADIANT benchmark releases should include a manifest that makes provenance,
versioning, split structure, and data-governance status inspectable.

- `BENCHMARK_MANIFEST_TEMPLATE.json` is a draft template, not metadata for an
  existing release.
- `benchmark-manifest.schema.json` defines the structural contract.
- A manifest validates metadata shape only. It does not validate the
  mathematical correctness of cases, reference labels, or pair manipulations.
- Record a SHA-256 checksum for each published split file. Do not invent a
  checksum before the exact artifact exists.
- Keep all related paraphrase and counterfactual variants in the same split
  unless the frozen protocol explicitly justifies another design.
- Record the real source type and permissions. Do not label data
  researcher-authored synthetic if it was adapted from learner records.
- Update privacy-review fields whenever the source or processing changes.

## Release checklist

1. Freeze the casebook and label protocol versions.
2. Confirm that every case has a stable unique attempt ID.
3. Check that paired variants do not leak across splits.
4. Generate checksums from the final files.
5. Confirm the license and provenance statements.
6. Review privacy and permissions before publishing any non-synthetic data.
7. Preserve the manifest with the exact release artifacts.

The template is intentionally incomplete. Empty split lists and null metadata
must be replaced with verified values before a release is described as frozen.
