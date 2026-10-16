# Publication dataset (60 transcripts)

This directory contains **only** the 60 transcripts and 60 reference keys used
in the finalized study. Unused files from the larger 180-file generation pool
are not included.

## Splits

| Split | n | Role |
| --- | --- | --- |
| `mixed_validation/` | 12 | Stage 1 prompt comparison and Stage 2 model selection |
| `mixed_reserved/` | 18 | Stage 3 final mixed-convention evaluation |
| `single_convention_reserved/` | 30 | Stage 3 final single-convention evaluation (10 conventions × 3 difficulties) |

Seed 42 defined the mixed validation/reserved split. The 12 validation families
and 18 reserved families do not overlap.

## Mixed-convention source

Mixed files are **V3.1**. Older mixed files that still exist in some private
working copies have different SHA-256 hashes and must not be substituted.

## Reference keys

Keys were **AI-generated and then reviewed and corrected by the author**. They
are not independently human-annotated gold standards.

SHA-256 checksums for every file are in `MANIFEST.json`.
