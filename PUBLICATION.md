# Public-release notes

This public repository's default `main` branch is an independent,
**clean-history snapshot** of the finalized 60-transcript study.
The earlier research workspace and its Git history remain separately private.

## Included

- 60 transcripts + 60 author-reviewed reference keys (V3.1 mixed files; reserved single-convention files)
- Frozen mixed prompts V1–V5 and the transcript-generation prompt
- Stage 1–3 manifests, summaries, tables, and saved cells (raw model responses)
- Offline hash verification, original mixed-convention F1 reproduction, and the post hoc designated-category single-convention scoring script

## Excluded (and why)

| Material | Reason |
| --- | --- |
| 120 unused generation-pool transcripts/keys | Not evaluated in the finalized 60-transcript study |
| Older mixed-file revisions retained only in the private research archive | SHA-256 differs from V3.1; Stage 3 forbids substitution |
| Streamlit lab, 180-file Super Mode runners | Superseded experimental pipeline |
| SALTee 180-file baseline outputs | Tied to the unused 180 corpus |
| `.env`, provider secrets, lock files | Credentials / local process state |
| `writing/`, `archive/`, internal notes | Not for public distribution |
| Stage 2 `recovery/` working archives | Operational debris, not publication records |
| Original 180-transcript generation-settings document | Historical design notes for a superseded pool, not the frozen 60-transcript evaluation |
| Copyrighted SALT manuals / PDFs | No redistribution permission |
| Clinical or laboratory transcripts | None are in this study; none are published |


## Scoring correction for the paper

The first Stage 3 evaluation used the same full V5 prompt and **all-category scoring** on both mixed and single-convention-designated transcripts. The frozen all-category single results (Sol 99.68%, Gemini 97.02%) are retained in the **archival** Stage 3 tables. After recognizing that the single-convention files were designed to emphasize one specified target, a **post hoc designated-category reanalysis** was calculated from the exact same saved responses and keys. Results: **Sol 99.59%** (604 TP, 5 FP, 0 FN), **Gemini 97.30%** (577 TP, 5 FP, 27 FN); on the 29 valid matched files both scored **99.57%**.

The original mixed all-category primary results (97.81% and 90.60%) are unchanged. The two scoring scopes should not be merged into one overall F1. The new offline script is `scripts/reproduce_designated_category_scores.py`.

## Public-release status and provenance

The public repository was created from the clean, independent publication
snapshot. It includes only the current 60-transcript dataset and its recorded
experiment artifacts; historical 180-file SALTee research is not part of this
repository or its initial Git history. The private historical research
repository is maintained separately.

The current public `main` branch contains the manuscript-supporting materials.
There is no need to check out a separate publication branch.

## Pending author decisions

1. Decide whether to keep the **all rights reserved** notice or add an explicit
   reuse license. Public availability alone does not grant redistribution rights.
2. Create an immutable GitHub release tag and/or archive DOI once the manuscript
   and the reproducibility checks are finalized.
