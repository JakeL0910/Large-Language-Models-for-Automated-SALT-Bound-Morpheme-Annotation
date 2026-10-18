# SALT bound-morpheme annotation with large language models

**Reproducibility materials for a 60-transcript synthetic SALT annotation study.**
This branch accompanies the manuscript *Large Language Models for Automated
Systematic Analysis of Language Transcripts (SALT) Bound Morpheme Annotation*.

**Repository status:** This is the **public, clean-history publication
repository** for the finalized 60-transcript study. The unrelated historical
180-file research workspace is preserved separately in a private archive.
No manuscript DOI or versioned GitHub release has been assigned yet.

## Study at a glance

The study compares five prompts, nine full-validation model configurations, and
two finalists using exact-match annotated-token micro F1. **All transcripts and
reference keys are synthetic**; initial keys were model-generated and then
reviewed/corrected by the author, with no independent expert reliability study.

| Dataset partition | Files | Use |
| --- | ---: | --- |
| Mixed-convention validation, revised V3.1 | 12 | Stages 1–2 |
| Mixed-convention reserved, revised V3.1 | 18 | Stage 3 |
| Single-convention-designated reserved | 30 | Stage 3 |
| **Total distinct transcript families** | **60** | 60 reference keys |

There are **30 distinct mixed-convention families**, not 60: the V3.1 files are
revisions of the older mixed transcripts, not independent extra samples.
The 30 reserved single-convention files were sampled from a pool of 150
(10 conventions × 3 difficulties × 5 candidates, seed 42).

Single-convention-designated transcripts **emphasize** one morphological category,
but may contain others. The **same full ten-convention V5 prompt** was used on
every Stage 3 file, not a specialized single-convention V5 prompt.

The frozen V5 SHA-256 is:

`f554bf77a9e8dbe0963425ef54e35f78619d8cdfb333151202a514597b2eede7`

## Experimental stages

1. **Stage 1:** Prompt versions V1–V5 × GPT-4o/GPT-5.6 Luna × 12 mixed validation files: **120 evaluations**. V5 achieved **88.79%** pooled F1 across the two models.
2. **Stage 2:** V5 with model/inference-setting screening; **nine configurations** have complete 12-file validation results. GPT-5.6 Sol (medium reasoning, **97.83%**) and Gemini 3.6 Flash (medium thinking, **97.62%**) advanced.
3. **Stage 3:** Each finalist annotated 18 mixed reserved and 30 single reserved files, one full-transcript request per file: **96 first attempts**. Original failed outputs remain failures.

## Stage 3 results and scoring provenance

**Mixed-convention** evaluation includes all ten SALT bound-morpheme categories.
The strict first-attempt scores were **97.81% Sol** and **90.60% Gemini**
(18/18 and 16/18 structurally valid files, respectively). On the same 16
mixed files parsed by Gemini, the matched-file F1s were **97.72% Sol**
and **97.97% Gemini**.

**Single-convention-designated** transcripts were **originally scored over all
categories** because the model used the full V5 prompt. Those original archival
scores were **99.68% Sol** and **97.02% Gemini**. Following review of the
intended target-category question, the saved outputs were **rescored post hoc**
using only the convention designated for each transcript. This is a
**post hoc correction/analysis**, not a prespecified single-category run.

| Stage 3 set / strict first attempt | Sol F1 | Gemini F1 |
| --- | ---: | ---: |
| Mixed 18 — all-category (primary) | **97.81%** | **90.60%** |
| Single 30 — **post hoc designated-category** | **99.59%** | **97.30%** |
| Single 29 successfully parsed by Gemini — designated-category, matched files | **99.57%** | **99.57%** |

Designated-category first-attempt totals:
- Sol: **604 TP / 5 FP / 0 FN**, 30/30 structurally valid transcripts.
- Gemini: **577 TP / 5 FP / 27 FN**, 29/30 structurally valid transcripts.
- Of 1,545 reference-marked tokens in single-convention-designated files,
  **604 (39.1%)** belonged to each file's designated target category.
- All **27 Gemini target-category FN** in this split arise from the
  structurally invalid `NEG_hard_04` response.

Gemini's other two failures were mixed-convention files
`hard_03` and `medium_02`. No failing output was silently repaired or
excluded in strict-score reporting. **Do not combine mixed all-category F1 with
single designated-category F1 into an overall F1**; those are different scoring
scopes.

The original pre-correction tables are preserved in
[`experiments/stage3_finalists/STAGE3_RESULTS.md`](experiments/stage3_finalists/STAGE3_RESULTS.md)
as **archival evidence** and must not be mistaken for corrected
designated-category results.

## Offline reproducibility (no API key required)

Python 3.11+; these scripts use the Python standard library.

```bash
git clone https://github.com/JakeL0910/Large-Language-Models-for-Automated-SALT-Bound-Morpheme-Annotation.git
cd Large-Language-Models-for-Automated-SALT-Bound-Morpheme-Annotation
# The published 60-transcript snapshot is already on main

python scripts/verify_publication_dataset.py
python scripts/reproduce_published_scores.py
python scripts/reproduce_designated_category_scores.py
```

The verification script checks 60 transcripts, 60 keys, held-out split isolation,
and the frozen V5 hash. The mixed scorer checks the archived mixed Stage 3
TP/FP/FN and F1; the new designated-category scorer checks the post hoc
single-convention TP/FP/FN, the matched 29-file comparison, and difficulty
breakdown using the **unchanged frozen cell responses**.

You do **not** need API keys or paid inference to verify either score.

## Repository layout

```text
dataset/          60 synthetic transcripts and author-reviewed reference keys
prompts/10 Final/ Frozen mixed-convention V1–V5 prompts and freeze records
prompts/generation/  Generation prompt for synthetic transcripts
experiments/      Stage 1–3 plans, historical summaries and score tables
results/          Frozen response cells and annotation strings
scoring/          Exact-match multiset token evaluation
scripts/          Offline dataset checks and F1 reproduction
```

The unused focused-prompt variants, SALTee implementation, original 180-file
pool, internal notes, and legacy Streamlit UI are **not** part of this
public repository. Historical research files and history are kept in a
separate private archive.

## Scope and limitations

These scores measure exact match to author-reviewed **synthetic** reference
annotations, not accuracy on naturalistic clinical transcripts. No independent
human inter-annotator reliability study was performed. The generation model
(GPT-5.6 Sol) was also evaluated; the direction and size of any resulting
bias have not been established.

## License and citation

This repository currently retains **all rights reserved**. Public viewing and
reproduction of the reported results do not imply permission to redistribute
or modify these materials. No manuscript DOI or release tag has been assigned.
Cite the accompanying manuscript and link to this repository when referencing
these materials.
