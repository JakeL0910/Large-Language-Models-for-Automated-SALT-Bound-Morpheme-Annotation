#!/usr/bin/env python3
"""Verify the 60-file public dataset hashes and split isolation. No API calls."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V5 = "f554bf77a9e8dbe0963425ef54e35f78619d8cdfb333151202a514597b2eede7"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    man = json.loads((ROOT / "dataset/MANIFEST.json").read_text())
    errors = []
    splits = {"mixed_validation": [], "mixed_reserved": [], "single_convention_reserved": []}
    for row in man["files"]:
        splits[row["split"]].append(row["family"])
        for kind in ("transcript", "key"):
            path = ROOT / row[kind]
            expected = row["transcript_sha256"] if kind == "transcript" else row["key_sha256"]
            if not path.is_file():
                errors.append(f"missing {path}")
                continue
            got = sha256_file(path)
            if got != expected:
                errors.append(f"hash {path}: got {got} expected {expected}")
    n_tx = len(list((ROOT / "dataset").rglob("transcripts/*.txt")))
    n_key = len(list((ROOT / "dataset").rglob("keys/*.txt")))
    if n_tx != 60 or n_key != 60:
        errors.append(f"counts transcripts={n_tx} keys={n_key} (expected 60/60)")
    if set(splits["mixed_validation"]) & set(splits["mixed_reserved"]):
        errors.append("validation/reserved mixed overlap")
    if set(splits["single_convention_reserved"]) & (
        set(splits["mixed_validation"]) | set(splits["mixed_reserved"])
    ):
        errors.append("single-convention overlap with mixed families")
    v5 = sha256_file(ROOT / "prompts/10 Final/v5 Final.txt")
    if v5 != V5:
        errors.append(f"V5 hash {v5}")
    print(f"transcripts={n_tx} keys={n_key}")
    print(f"validation={len(splits['mixed_validation'])} reserved_mixed={len(splits['mixed_reserved'])} single={len(splits['single_convention_reserved'])}")
    print(f"V5={v5}")
    if errors:
        print("FAIL")
        for e in errors:
            print(" ", e)
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    main()
