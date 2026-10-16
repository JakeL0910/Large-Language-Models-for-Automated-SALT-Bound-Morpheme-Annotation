# Public-release notes

This branch is a **clean-history snapshot** of the finalized 60-transcript study.
It is not a rewrite of `main` or of the private research branches.

## Included

- 60 transcripts + 60 author-reviewed reference keys (V3.1 mixed files; reserved single-convention files)
- Frozen mixed prompts V1–V5 and the transcript-generation prompt
- Stage 1–3 manifests, summaries, tables, and saved cells (raw model responses)
- Offline hash verification and F1 reproduction scripts

## Excluded (and why)

| Material | Reason |
| --- | --- |
| 120 unused generation-pool transcripts/keys | Not evaluated in the finalized 60-transcript study |
| Older mixed files currently on `main` | SHA-256 differs from V3.1; Stage 3 forbids substitution |
| Streamlit lab, 180-file Super Mode runners | Superseded experimental pipeline |
| SALTee 180-file baseline outputs | Tied to the unused 180 corpus |
| `.env`, provider secrets, lock files | Credentials / local process state |
| `writing/`, `archive/`, internal notes | Not for public distribution |
| Stage 2 `recovery/` working archives | Operational debris, not publication records |
| Copyrighted SALT manuals / PDFs | No redistribution permission |
| Clinical or laboratory transcripts | None are in this study; none are published |

## History warning

`origin/main` still contains the 180-file tree. Making **that** default branch public would expose unused transcripts through Git history even if the tip is later slimmed. Prefer this clean branch or a new public repository. Do not rewrite existing history without a separate approval.

## Pending author decisions

1. Select a public license (current file still says all rights reserved).
2. Approve pushing this branch and/or creating a new public GitHub repository.
3. Do **not** flip the existing private repository to public until that history question is decided.
