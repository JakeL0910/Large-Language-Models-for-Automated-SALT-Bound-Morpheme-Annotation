#!/usr/bin/env python3
"""Recompute published Stage 3 F1 from saved cells. No API calls."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scoring"))
sys.path.insert(0, str(ROOT / "scripts"))

from evaluate import evaluate_rows, pool, read_pairs  # noqa: E402

SOL = "gpt-5.6-sol__reason-medium"
GEM = "gemini-3.6-flash__think-medium"
PUBLISHED = {
    ("sol", "mixed", "strict"): 97.8135,
    ("gemini", "mixed", "strict"): 90.6024,
    ("sol", "mixed", "parsed_ok_matched16"): 97.7155,
    ("gemini", "mixed", "parsed_ok"): 97.9677,
}


def cells_dir() -> Path:
    return ROOT / "results/stage3_finalists/cells"


def load_cell(config_id: str, family: str) -> dict:
    return json.loads((cells_dir() / f"{config_id}__{family}.json").read_text(encoding="utf-8"))


def families(eval_set: str) -> list[str]:
    plan = json.loads((ROOT / "experiments/stage3_finalists/plan.json").read_text())
    return [r["family"] for r in plan["files"] if r["eval_set"] == eval_set]


def pool_cells(config_id: str, fams: list[str], ok_only: bool = False) -> dict:
    rows = []
    n_ok = 0
    for fam in fams:
        cell = load_cell(config_id, fam)
        if ok_only and not cell.get("ok"):
            continue
        n_ok += 1 if cell.get("ok") else 0
        for r in cell.get("rows") or []:
            rows.append(r)
    out = pool(rows) if rows else {}
    out["n_files"] = n_ok if ok_only else len(fams)
    out["n_ok"] = n_ok
    return out


def main() -> None:
    mixed = families("mixed_reserved")
    assert len(mixed) == 18
    sol = pool_cells(SOL, mixed)
    gem = pool_cells(GEM, mixed)
    gem_ok_fams = [f for f in mixed if load_cell(GEM, f).get("ok")]
    sol_matched = pool_cells(SOL, gem_ok_fams)
    gem_ok = pool_cells(GEM, gem_ok_fams, ok_only=True)
    checks = [
        ("sol mixed strict", sol["micro_f1_pct"], PUBLISHED[("sol", "mixed", "strict")]),
        ("gemini mixed strict", gem["micro_f1_pct"], PUBLISHED[("gemini", "mixed", "strict")]),
        ("sol mixed matched-16", sol_matched["micro_f1_pct"], PUBLISHED[("sol", "mixed", "parsed_ok_matched16")]),
        ("gemini mixed parsed-ok", gem_ok["micro_f1_pct"], PUBLISHED[("gemini", "mixed", "parsed_ok")]),
    ]
    print("Stage 3 mixed-convention offline reproduction (saved cells, no API)")
    failed = False
    for name, got, expected in checks:
        ok = abs(got - expected) < 0.01
        print(f"  {'PASS' if ok else 'FAIL'} {name}: {got:.4f} (published {expected:.4f})")
        failed = failed or not ok
    print(f"  Gemini mixed files ok: {gem['n_ok']}/18; structural failures remain in strict F1")
    if failed:
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    main()
