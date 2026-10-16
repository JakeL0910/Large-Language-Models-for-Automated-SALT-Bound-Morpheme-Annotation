# Stage 1 frozen mixed-convention prompts

Status: **FROZEN for Stage 1.** Do not edit V1–V5 during Stage 1 or in response to Stage 1 results.

Frozen at (UTC): `2026-10-14T22:33:09Z`

V1, V2, and V5 received the exact rule corrections from GitHub PR #4 (`research/stage1-prompt-freeze-v1`). V3 and V4 were already identical to that branch and were not edited.

Source: https://github.com/JakeL0910/SALT-AI-Prompt-Project/pull/4

| Version | Path | SHA-256 | Strategy |
| --- | --- | --- | --- |
| V1 | `prompts/10 Final/v1 Final.txt` | `6e6ee89af369c78952f85b552d9c980da4404a14a22dd20f5aa7b92698a3f278` | persona / holistic expert |
| V2 | `prompts/10 Final/v2 Final.txt` | `3122c18068e1db6b2981f026e07e092395d58a2b502418107da93fcdb0ad5979` | ordered stepwise workflow |
| V3 | `prompts/10 Final/v3 Final.txt` | `f02b14f6486231a01435c78c49978710cbdd8522527c75a499654764d0806035` | independent labeled rule blocks |
| V4 | `prompts/10 Final/v4 Final.txt` | `d92be4588fe5bf5b5d7e70ed4430513824fcb215c2a38ac84749a6c9156ca65a` | IF/THEN decision trees |
| V5 | `prompts/10 Final/v5 Final.txt` | `f554bf77a9e8dbe0963425ef54e35f78619d8cdfb333151202a514597b2eede7` | detailed rules with six few-shot examples |

All five files cover the ten SALT bound-morpheme categories (S, Z, 3S, ING, ED, EN, BE, MODAL, OTHER, NEG).
Aligned with V3.1 gold: mark utterance-initial regular plurals; mark regular `/ed` in HAVE/HAS/HAD perfect; leave `don't` / `won't` / `ain't` unmarked.

Do not change these files without a new freeze.
