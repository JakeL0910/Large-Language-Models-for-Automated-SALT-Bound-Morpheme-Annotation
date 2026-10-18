# Stage 3 finalist results — archival original aggregation

> **Archival Stage 3 scoring log (before designated-category reanalysis).**
> The original all-category single-convention scores of **99.68% Sol** and
> **97.02% Gemini**, and the original all-category combined scores, are
> preserved below as historical experiment records. They are **not** the
> manuscript's corrected single-convention-designated results. The post hoc
> designated-category analysis of the same frozen model outputs yields
> **99.59% Sol** (604 TP / 5 FP / 0 FN) and **97.30% Gemini**
> (577 TP / 5 FP / 27 FN); matched 29 valid files: **99.57% for both**.
> This was a **post hoc reanalysis**, not a prespecified evaluation using
> specialized prompts. Reproduce with
> `python scripts/reproduce_designated_category_scores.py`.
> **Do not mix all-category and designated-category counts into one F1.**


Status: **STAGE3_GEMINI_CONTINUATION_COMPLETE.** 96 first-attempt cells on disk.
Gemini has three original structural failures (`hard_03`, `medium_02`, `NEG_hard_04`).
Those cells were not retried or overwritten. No retuning.

Prompt: combined-convention V5 (`prompts/10 Final/v5 Final.txt`), SHA-256
`f554bf77a9e8dbe0963425ef54e35f78619d8cdfb333151202a514597b2eede7`.
Primary metric: pooled bag-of-morphemes micro F1. WLA not computed.

## Execution

| Item | Result |
| --- | --- |
| Planned | 96 |
| Cells on disk | 96 (Sol 48/48 ok; Gemini 45 ok + 3 failed) |
| Continuation | 33/33 Gemini unattempted cells ran |
| New structural failure | `NEG_hard_04` (saved, scored failed, queue continued) |
| Preserved failures | `hard_03`, `medium_02` SHA-256 unchanged |
| Spend | **$5.5485 / $12** |
| Stop | none (continuation completed) |

## 1. Strict first-attempt (archival all-category aggregation)

Structural JSON/ID failures remain failures. Do not drop them from the frozen 18+30 design.

| Model | Split | Files ok | Micro F1 | P | R | Fail | TP/FP/FN |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-5.6 Sol medium | Mixed 18 | 18/18 | **97.81%** | 95.89 | 99.82 | 0/1889 | 1096/47/2 |
| Gemini 3.6 Flash medium | Mixed 18 | 16/18 | 90.60% | 96.21 | 85.61 | 244/1889 | 940/37/158 |
| GPT-5.6 Sol medium | Single 30 | 30/30 | **99.68%** | 99.42 | 99.94 | 0/1800 | 1544/9/1 |
| Gemini 3.6 Flash medium | Single 30 | 29/30 | 97.02% | 99.26 | 94.89 | 81/1800 | 1466/11/79 |
| GPT-5.6 Sol medium | Combined 48 | 48/48 | **98.89%** | 97.92 | 99.89 | 0/3689 | 2640/56/3 |
| Gemini 3.6 Flash medium | Combined 48 | 45/48 | 94.41% | 98.04 | 91.03 | 325/3689 | 2406/48/237 |

Gemini mixed by difficulty (strict): easy 99.62% (6/6); medium 88.89% (5 ok + `medium_02`); hard 86.76% (5 ok + `hard_03`).

Failed families: `hard_03`, `medium_02`, `NEG_hard_04`.

## 2. Parsed-successful annotation (archival all-category subset)

Successfully parsed transcripts only.

| Split | Gemini files | Micro F1 | P | R | Fail | vs Sol on the same files |
| --- | --- | --- | --- | --- | --- | --- |
| Mixed | 16/18 | **97.97%** | 96.21 | 99.79 | 0/1645 | Sol 97.72% |
| Single | 29/30 | **99.56%** | 99.26 | 99.86 | 1/1720 | Sol 99.66% |
| Combined | 45/48 | 98.93% | 98.04 | 99.83 | 1/3365 | — |

Mixed parsed-ok by difficulty: easy 99.62%; medium 97.78% (5 files); hard 97.08% (5 files).
Single parsed-ok: easy 99.68% (one `Z_easy_02` token-drop failure); medium 99.72%; hard 99.37% (9 files).

Most overlapping mixed pairs tie. Small gaps: `medium_06` Gemini +2.97 pp, `hard_05` Gemini +2.38 pp, `medium_01` Sol +1.96 pp. Not a winner rule.

## 3. Offline normalization sensitivity (not a substitute)

| File | Strict | Remap | Diagnostic F1 |
| --- | --- | --- | --- |
| `hard_03` | missing id 60 (`override`) | applicable; 102/5/0 | 97.61% |
| `medium_02` | missing id 99 (`item`) | applicable; 54/4/0 | 96.43% |
| `NEG_hard_04` | invalid JSON at char 5738 | **not applicable** | — |

`NEG_hard_04`: `finish=STOP`, 9,239 of 16,384 tokens. JSON is intact through id 75, then keys corrupt (`" me"` instead of `"id"`), the array does not close, and non-JSON text is appended. Original cell preserved as a first-attempt failure.

## Spend and comparison notes

Cumulative Stage 3 **$5.5485** of $12 (Sol $3.96, Gemini $1.58). Continuation added about $1.00.

Stage 2 mixed validation (different 12 files): Sol 97.83%, Gemini 97.62%. Stage 3 reserved mixed strict: Sol 97.81% (complete); Gemini 90.60% with two mixed structural failures. Parsed-ok Gemini mixed 97.97% is a 16-file subset, not the frozen 18.

The original strict all-category 18+30 comparison is preserved here for provenance, not as the corrected combined figure. Parsed-ok mixed scores are close (Gemini 97.97 vs Sol 97.72 on the same 16 files).

## Artifacts

- Cells: `results/stage3_finalists/cells/` (48 Sol + 48 Gemini)
- Continuation summary: `results/stage3_finalists/summary_gemini_continuation.json`
- Strict / parsed-ok / sensitivity: `experiments/stage3_finalists/summary_strict_first_attempt.json`, `summary_parsed_ok.json`, `sensitivity_offline_normalization.json`
- Tables: `table1_mixed_strict.csv`, `table1_mixed_parsed_ok.csv`, `table6_paired_mixed_strict.csv`, `table6_paired_mixed_parsed_ok.csv`
