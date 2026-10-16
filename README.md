# SALT-AI: Prompted LLM Annotation of Bound Morphemes

This repository accompanies a study of large language models as annotators of
**SALT bound-morpheme slash codes** on **synthetic** child–adult play transcripts.

The finalized experiment used **exactly 60 distinct transcripts** (and 60
reference keys). It does not evaluate the older 180-file generation pool.

## Research objective

Compare prompt designs and model configurations for automatic bound-morpheme
annotation, then evaluate two frozen finalists on a held-out reserved set.
The primary metric is pooled bag-of-morphemes **micro F1**. Word-level
accuracy (WLA) is not used.

## Dataset (60 transcripts)

| Split | n | Used in |
| --- | --- | --- |
| Mixed-convention **validation** (V3.1) | 12 | Stage 1 and Stage 2 |
| Mixed-convention **reserved** (V3.1) | 18 | Stage 3 only |
| Single-convention **reserved** | 30 | Stage 3 only |
| **Total** | **60** | |

The 12 validation families and 18 reserved mixed families are disjoint
(seed 42). Mixed files are the V3.1 versions used in the completed runs;
older mixed files with different hashes are not this dataset.

**Reference annotations were AI-generated and then reviewed and corrected by
the author. They are not independently human-annotated gold standards.**

Checksums: [`dataset/MANIFEST.json`](dataset/MANIFEST.json).

### Ten bound-morpheme conventions

| Convention | Code | Example mark |
| --- | --- | --- |
| Regular plural | S | `/s` |
| Possessive | Z | `/z` |
| 3rd-person singular | 3S | `/3s` |
| Progressive | ING | `/ing` |
| Regular past | ED | `/ed` |
| Past participle | EN | `/en` |
| Contracted BE | BE | `/'s` `/'re` `/'m` |
| Contracted modals | MODAL | `/'ll` `/'d` |
| Other contractions | OTHER | `/'ve` `/h's` … |
| Negation | NEG | `/n't` `/'t` |

`MIXED_FINAL` means mixed-convention transcripts, not an 11th convention.

## Prompt-engineering strategies (V1–V5)

Stage 1 compared five mixed-convention prompt versions on the 12 validation
transcripts. Frozen files live in [`prompts/10 Final/`](prompts/10%20Final/).

| Version | Strategy |
| --- | --- |
| V1 | Persona / holistic expert |
| V2 | Ordered stepwise workflow |
| V3 | Independent labeled rule blocks |
| V4 | IF/THEN decision trees |
| V5 | Detailed rules with few-shot examples |

The Stage 3 prompt is **V5**. SHA-256:

`f554bf77a9e8dbe0963425ef54e35f78619d8cdfb333151202a514597b2eede7`

Do not edit these files if the goal is to match the published scores.

## Experimental stages

Processing was full-transcript JSON batching (one transcript per request).

### Stage 1 — Prompt comparison

- Prompts V1–V5
- Models: GPT-4o and GPT-5.6 Luna
- 12 validation transcripts
- **120** model–prompt–transcript evaluations

V5 was the strongest pooled prompt (micro F1 88.79% across both models on the
24 V5 cells).

### Stage 2 — Model selection

- 13 base model/reasoning configurations were considered
- Additional inference-setting screening
- **Nine** configurations have complete 12-transcript validation results
- **Seven** distinct model families appear in that ranking: GPT-4o, GPT-5.6 Luna, GPT-5.6 Sol, Gemini 3.6 Flash, DeepSeek V4 Pro, Qwen 3.5 Plus, Claude Sonnet 5

Finalists (V5, 12-file validation micro F1):

- GPT-5.6 Sol, medium reasoning: **97.83%**
- Gemini 3.6 Flash, medium thinking: **97.62%** (tied with think-high; medium was selected)

### Stage 3 — Final evaluation

Each finalist annotated **48 reserved transcripts** (18 mixed + 30 single-convention).
**96** first-attempt API requests.

| Result | Sol medium | Gemini medium |
| --- | --- | --- |
| Mixed 18, **strict first-attempt** micro F1 | **97.81%** | **90.60%** |
| Mixed files successfully parsed | 18/18 | 16/18 |
| Single-convention 30, strict | 99.68% | 97.02% (29/30 parsed) |

Gemini produced **three structurally invalid** transcript responses (`hard_03`,
`medium_02`, `NEG_hard_04`). Those cells remain failures in the strict scores.

On the **16 mixed files Gemini parsed successfully**, matched-file micro F1 was
**97.72% Sol vs 97.97% Gemini**. That subset is not the official 18-file result.

## Installation

Python 3.11+ is sufficient to verify hashes and reproduce F1 from saved cells
(standard library only).

```bash
git clone https://github.com/JakeL0910/SALT-AI-Prompt-Project.git
cd SALT-AI-Prompt-Project
python -m venv .venv
source .venv/bin/activate
```

Provider keys are **not required** to reproduce published scores. If you later
run new paid API jobs, copy `.env.example` to `.env` and keep `.env` uncommitted.

## Reproduce published scores (offline)

No new API calls:

```bash
python scripts/verify_publication_dataset.py
python scripts/reproduce_published_scores.py
```

The first command checks that 60 transcripts, 60 keys, split isolation, and the
V5 hash match the frozen manifests. The second recomputes Stage 3 mixed-convention
micro F1 from saved model outputs.

## Repository structure

```
dataset/          60 transcripts + 60 keys, split into validation / reserved
prompts/          Frozen V1–V5 mixed prompts; generation prompt (synthetic data)
experiments/      Stage 1–3 manifests, tables, and summaries
results/          Saved cells including raw model responses
scoring/          Bag-of-morphemes scorer used for published F1
scripts/          Offline verification and reproduction
```

## Limitations

Transcripts are **synthetic**. They were generated to stress SALT bound-morpheme
conventions and do not represent a clinical corpus. Do not treat scores as
performance on real SALT samples. Do not distribute copyrighted SALT manuals
with this repository.

## License

The current `LICENSE` still reserves all rights (legacy private-project terms).
A public license has not been selected. Ask the author before redistributing.

## Citation

Cite the accompanying manuscript when using this dataset or the published scores.
