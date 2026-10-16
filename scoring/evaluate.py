"""Offline SALT bag-of-morphemes scoring (Stage 1–3 evaluate_rows)."""
from __future__ import annotations

import re
from pathlib import Path

from annotation_metrics import extract_morphemes, morpheme_tp_fp_fn

SPEAKER_LINE = re.compile(r"^[CPA]\s")


def speech_utterances(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if SPEAKER_LINE.match(line.strip())]


def read_pairs(transcript: Path, key: Path) -> list[tuple[str, str]]:
    raw = speech_utterances(transcript.read_text(encoding="utf-8"))
    gold = speech_utterances(key.read_text(encoding="utf-8"))
    if len(gold) != 2 * len(raw):
        raise ValueError(f"Key alignment failure: {key.name} {len(gold)} vs {len(raw)}")
    pairs = []
    for i, line in enumerate(raw):
        if gold[2 * i] != line:
            raise ValueError(f"Gold/raw disagreement in {transcript.name}, utterance {i + 1}")
        pairs.append((line, gold[2 * i + 1]))
    return pairs


def evaluate_rows(pairs: list[tuple[str, str]], by_id: dict[int, str]) -> list[dict]:
    rows = []
    for i, (original, expected) in enumerate(pairs):
        actual = by_id.get(i, "")
        tokens_equal = bool(actual) and len(original.split()) == len(actual.split())
        speaker_equal = bool(actual) and original.split()[0] == actual.split()[0]
        failed = not actual or not tokens_equal or not speaker_equal
        if failed:
            tp, fp, fn = 0, len(extract_morphemes(actual)), len(extract_morphemes(expected))
        else:
            tp, fp, fn = morpheme_tp_fp_fn(expected, actual)
        rows.append({
            "original": original, "expected": expected, "actual": actual,
            "tp": tp, "fp": fp, "fn": fn, "failed": failed,
        })
    return rows


def pool(rows: list[dict]) -> dict:
    tp = sum(r["tp"] for r in rows)
    fp = sum(r["fp"] for r in rows)
    fn = sum(r["fn"] for r in rows)
    fail = sum(1 for r in rows if r["failed"])
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {
        "n_utterances": len(rows),
        "failures": fail,
        "tp": tp, "fp": fp, "fn": fn,
        "precision_pct": round(prec * 100, 4),
        "recall_pct": round(rec * 100, 4),
        "micro_f1_pct": round(f1 * 100, 4),
    }
