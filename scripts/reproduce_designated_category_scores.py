#!/usr/bin/env python3
"""Reproduce Stage 3 designated-category post hoc scores from frozen saved outputs.

The original experiment used the full V5 prompt on ALL transcripts and
initially counted all 10 morpheme categories in both transcript types.

For the 30 single-convention-designated transcripts, this post hoc analysis
restricts token-level TP/FP/FN to each file's target category. All model
outputs, reference keys, and strict structural failure treatment are unchanged.

No API key or model inference is required.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scoring"))

from annotation_metrics import (  # noqa: E402
    CONVENTION_CODE_TUPLES,
    extract_morphemes,
    token_code_tuple,
)

SOL = "gpt-5.6-sol__reason-medium"
GEM = "gemini-3.6-flash__think-medium"
EXPECTED = {
    SOL: (604, 5, 0),
    GEM: (577, 5, 27),
}
EXPECTED_MATCHED = (577, 5, 0)


def reference_files() -> list[dict]:
    plan = json.loads(
        (ROOT / "experiments/stage3_finalists/plan.json").read_text(encoding="utf-8")
    )
    files = [f for f in plan["files"] if f["eval_set"] == "single_convention_reserved"]
    assert len(files) == 30
    assert {f["convention"] for f in files} == set(CONVENTION_CODE_TUPLES)
    return files


def load_cell(config: str, family: str) -> dict:
    path = ROOT / "results/stage3_finalists/cells" / f"{config}__{family}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def filtered_counter(text: str, convention: str) -> Counter:
    allowed = CONVENTION_CODE_TUPLES[convention]
    return Counter(
        token
        for token in extract_morphemes(text or "")
        if token_code_tuple(token) in allowed
    )


def score_cell(cell: dict, convention: str) -> tuple[int, int, int]:
    tp = fp = fn = 0
    for row in cell["rows"]:
        gold = filtered_counter(row.get("expected", ""), convention)
        predicted = filtered_counter(row.get("actual", ""), convention)
        if row.get("failed"):
            # Preserve strict original failure policy, within the target category.
            fp += sum(predicted.values())
            fn += sum(gold.values())
        else:
            matches = gold & predicted
            tp += sum(matches.values())
            fp += sum((predicted - gold).values())
            fn += sum((gold - predicted).values())
    return tp, fp, fn


def total(counts: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    return tuple(sum(part[i] for part in counts) for i in range(3))


def pct(tp: int, fp: int, fn: int) -> float:
    denominator = 2 * tp + fp + fn
    return 100.0 * 2 * tp / denominator if denominator else 0.0


def main() -> None:
    selected = reference_files()
    cells = {config: {} for config in (SOL, GEM)}
    for info in selected:
        for config in cells:
            cells[config][info["family"]] = load_cell(config, info["family"])

    print("Stage 3 post hoc designated-category scoring (30 single-convention transcripts)")
    print("Frozen full-V5 model outputs; no new API requests.")
    for config in (SOL, GEM):
        counts = total([
            score_cell(cells[config][f["family"]], f["convention"])
            for f in selected
        ])
        assert counts == EXPECTED[config], (config, counts, EXPECTED[config])
        print(
            f"  {config}: TP={counts[0]}, FP={counts[1]}, FN={counts[2]}, "
            f"micro F1={pct(*counts):.2f}%"
        )

    common_valid = [
        f for f in selected if cells[GEM][f["family"]].get("ok")
    ]
    assert len(common_valid) == 29
    print("Matched files with structurally valid Gemini output (29):")
    for config in (SOL, GEM):
        counts = total([
            score_cell(cells[config][f["family"]], f["convention"])
            for f in common_valid
        ])
        assert counts == EXPECTED_MATCHED, (config, counts)
        print(
            f"  {config}: TP={counts[0]}, FP={counts[1]}, FN={counts[2]}, "
            f"micro F1={pct(*counts):.2f}%"
        )

    gold_total = sum(
        sum(
            filtered_counter(r.get("expected", ""), f["convention"]).values()
            for r in cells[SOL][f["family"]]["rows"]
        )
        for f in selected
    )
    assert gold_total == 604, gold_total
    print("  Target-category reference annotations: 604 (of 1,545 across all codes)")

    for difficulty in ("easy", "medium", "hard"):
        relevant = [f for f in selected if f["difficulty"] == difficulty]
        counts = total([
            score_cell(cells[SOL][f["family"]], f["convention"])
            for f in relevant
        ])
        print(f"  Sol / {difficulty}: F1={pct(*counts):.2f}% "
              f"(TP={counts[0]}, FP={counts[1]}, FN={counts[2]})")
    print("PASS")


if __name__ == "__main__":
    main()
