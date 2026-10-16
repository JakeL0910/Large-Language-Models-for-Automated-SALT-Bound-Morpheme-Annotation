# Stage 1 final-prompt freeze — proposed 2026-10-14

Status: **review branch; freeze after approval/merge**. Do not alter V1–V5 during Stage 1 or select changes in response to Stage 1 results.

## Intent

Compare **five complete prompting formulations** against the **same ten Standard SALT bound-morpheme categories**:
- V1: linguistic-expert persona / holistic instructions
- V2: ordered stepwise workflow
- V3: independent labeled rule blocks
- V4: IF/THEN decision trees
- V5: extensive rule instructions with six worked demonstrations (few-shot)

These variants have different instruction lengths, examples, and structure. This is a **prompt-version comparison, not an isolated causal ablation** of persona, stepwise, decision-tree, or few-shot components.

## Surgical corrections to ensure the same target task

- V1: allow predicative nominal possessives; use the same aspectual KEEP/START -ing rule as V2–V5; acknowledge regular -ed participles in HAVE/HAS/HAD perfect constructions.
- V2: acknowledge regular -ed participles in HAVE/HAS/HAD perfect constructions instead of requiring finite simple past only.
- V3: unchanged.
- V4: unchanged.
- V5: remove unsupported special exception for a bare plural noun in utterance-initial position; permit regular -ed participles under HAVE/HAS/HAD, consistent with the worked examples and V3/V4.

The source SALT manual is the **October 2020 Standard SALT Conventions**, Section 9, especially regular plural /S, /ED, /EN, and contracted forms. Existing gold keys count regular -ed in HAVE perfect; all five prompt versions must use the same rule.

## Frozen file identities (Git blob SHA)

| File | Blob SHA (this branch) |
| --- | --- |
| `prompts/10 Final/v1 Final.txt` | `da864fc6dc9a36f54d84038f832b42251ec19fc5` |
| `prompts/10 Final/v2 Final.txt` | `fee043a4208410542af74d0b8c39fea85a24c428` |
| `prompts/10 Final/v3 Final.txt` | `d8b1ba0f328c0e45bb8d3db8568e39e1d61e6c28` |
| `prompts/10 Final/v4 Final.txt` | `92973d4e4b57caf4df9cba43a83b616081ac12f6` |
| `prompts/10 Final/v5 Final.txt` | `30cf1cea8e31928bdd84eb6b1b5fc924fa1bb81d` |

Save the exact prompts, code revision, dataset manifest, and model/API settings in each Stage 1 run log. Validate the local Cursor files against this commit prior to paid evaluation. **Do not run Stage 1 until the user's approval.**

## Preliminary experiment relationship

The preliminary batch-versus-one-by-one experiment already ran using the then-current local V5 prompt (its logged SHA-256 was `c0c66401176f56ec1655b7c863ba863f68be0562724e028232f75a5a15500ef6`). The initial prompt is a historical processing-mode pilot artifact and must not be silently represented as the identical Stage 1 frozen V5. Existing pilot scores remain historical observations and need no paid rerun just to freeze Stage 1 prompts.

## Manuscript wording (one surgical change; not applied here)

The existing text describes V5 as `concise` and as clarifying `the accent`. That does not accurately describe the current V5 file, which is around 31,000 characters with six worked examples and no accent-standardization instruction. Describe it as **detailed rule-based instructions with six few-shot worked examples**.

Similarly, report that `V5 achieved the highest F1 among the five versions`, not that few-shot prompting alone caused any observed performance improvement.
