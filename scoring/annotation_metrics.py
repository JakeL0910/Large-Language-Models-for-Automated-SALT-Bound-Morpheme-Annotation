"""Word-level and morpheme-level metrics for SALT annotation evaluation."""

import os
import re
import statistics
from collections import Counter
from typing import Dict, List, Optional, Set, Tuple

TRIAL_NUMERIC_KEYS = (
    "wla",
    "tp",
    "fp",
    "fn",
    "precision",
    "recall",
    "f1",
    "utterance_accuracy",
)

SKIP_TOKEN_LIMIT = "token_limit"
SKIP_API_ERROR = "api_error"
SKIP_MODEL_UNAVAILABLE = "model_unavailable"

SKIP_LABELS = {
    SKIP_TOKEN_LIMIT: "Token limit (reasoning used budget before answer)",
    SKIP_API_ERROR: "API / request error",
    SKIP_MODEL_UNAVAILABLE: "Model not available",
}

# Versioned lexical distractors for BM WLA (look-alike BM endings that must stay unmarked).
# Derived from scripts/salt_rule_baseline.py NOT_* lists, with high-frequency function
# words removed so the denominator stays focused on designed probe cases.
BM_DISTRACTOR_LEXICON_VERSION = "v1"

_BM_DISTRACTOR_FUNCTION_EXCLUDE: Set[str] = {
    "is",
    "was",
    "has",
    "his",
    "its",
    "us",
    "this",
    "yes",
    "plus",
    "does",
    "goes",
    "says",
    "let's",
    "lets",
    "ones",
    "then",
    "when",
    "even",
    "ten",
    "men",
    "hen",
    "pen",
    "den",
    "again",
    "been",
    "seen",
    "my",
    "your",
    "our",
    "their",
    "her",
    "mine",
    "hers",
    "ours",
    "yours",
    "theirs",
}

_BM_DISTRACTOR_RAW: Set[str] = {
    # Plural / -s lookalikes (and irregular -ves that should not get /s)
    "pants",
    "scissors",
    "binoculars",
    "glasses",
    "clothes",
    "news",
    "shorts",
    "pajamas",
    "jeans",
    "tongs",
    "series",
    "species",
    "mathematics",
    "gas",
    "bus",
    "always",
    "perhaps",
    "less",
    "unless",
    "across",
    "chess",
    "dress",
    "class",
    "glass",
    "grass",
    "kiss",
    "miss",
    "mess",
    "press",
    "guess",
    "boss",
    "cross",
    "toss",
    "leaves",
    "wolves",
    "knives",
    "lives",
    "wives",
    "shelves",
    "calves",
    "halves",
    "loaves",
    "thieves",
    "elves",
    "scarves",
    "selves",
    "hooves",
    # -ed lookalikes / predicate adjectives
    "red",
    "bed",
    "fed",
    "led",
    "shed",
    "sled",
    "need",
    "seed",
    "feed",
    "weed",
    "speed",
    "indeed",
    "bored",
    "tired",
    "scared",
    "excited",
    "surprised",
    "wicked",
    "sacred",
    "hundred",
    "naked",
    "united",
    "bread",
    "head",
    "dead",
    "ahead",
    "instead",
    "spread",
    "thread",
    "read",
    "interested",
    "worried",
    "confused",
    "annoyed",
    "amazed",
    "pleased",
    "embarrassed",
    "fixed",
    "broken",
    # -ing lookalikes
    "thing",
    "things",
    "something",
    "anything",
    "nothing",
    "everything",
    "morning",
    "evening",
    "king",
    "ring",
    "wing",
    "string",
    "spring",
    "sting",
    "ceiling",
    "during",
    "swing",
    "sling",
    "bring",
    "sing",
    "building",
    "clothing",
    "wedding",
    "pudding",
    # -en lookalikes (lexical; irregular participles only when gold leaves them unmarked)
    "children",
    "kitten",
    "garden",
    "often",
    "open",
    "seven",
    "green",
    "queen",
    "listen",
    "oven",
    "golden",
    "wooden",
    "sudden",
    "happen",
    "chicken",
    "mitten",
    "kitchen",
    "women",
    "citizen",
}

BM_DISTRACTORS: Set[str] = {
    w for w in _BM_DISTRACTOR_RAW if w not in _BM_DISTRACTOR_FUNCTION_EXCLUDE
}


def classify_failure(error_message: str, finish_reason: Optional[str] = None) -> str:
    """Map an exception or finish_reason to a skip_reason code."""
    msg = (error_message or "").lower()
    if finish_reason == "length" or "finish_reason=length" in msg:
        return SKIP_TOKEN_LIMIT
    if "model not available" in msg:
        return SKIP_MODEL_UNAVAILABLE
    return SKIP_API_ERROR


def skip_label(skip_reason: Optional[str]) -> str:
    if not skip_reason:
        return ""
    return SKIP_LABELS.get(skip_reason, skip_reason)


# A SALT mark is a word token followed by one or more slash-coded segments.
# The segment alphabet must include apostrophes for contractions such as
# I/'m, she/'s, we/'re, I/'ll, she/h'd, and did/n't.
MORPHEME_PATTERN = re.compile(r"(?<!\w)\w+(?:/[\w'’]+)+(?!\w)")


def extract_morphemes(text: str) -> List[str]:
    """Tokens containing a slash (e.g. eat/en, kitten/s)."""
    return MORPHEME_PATTERN.findall(text)


FOCUSED_CONVENTIONS = (
    "S",
    "Z",
    "3S",
    "ING",
    "ED",
    "EN",
    "BE",
    "MODAL",
    "OTHER",
    "NEG",
)

# Slash-code tuples that belong to a focused convention. /s/z is the Z
# (possessive) form for a regular plural owner, not an S-only mark.
CONVENTION_CODE_TUPLES = {
    "S": {("s",)},
    "Z": {("z",), ("s", "z")},
    "3S": {("3s",)},
    "ING": {("ing",)},
    "ED": {("ed",)},
    "EN": {("en",)},
    "BE": {("'s",), ("'re",), ("'m",)},
    "MODAL": {("'ll",), ("'d",)},
    "OTHER": {("'ve",), ("h's",), ("h'd",), ("d's",), ("d'd",), ("'us",)},
    "NEG": {("'t",), ("n't",)},
}

_TRAILING_PUNCT = re.compile(r"^(.*?)([.,!?;:\"')\]]+)$")


def convention_from_prompt_file(prompt_file: Optional[str]) -> Optional[str]:
    """Map ``v1 S.txt`` / ``v5 Final.txt`` stems to a convention name."""
    if not prompt_file:
        return None
    stem = os.path.splitext(os.path.basename(prompt_file))[0]
    parts = stem.split()
    token = parts[-1] if parts else ""
    if token in FOCUSED_CONVENTIONS or token == "Final":
        return token
    return None


def _split_trailing_punct(token: str) -> Tuple[str, str]:
    match = _TRAILING_PUNCT.match(token or "")
    if match:
        return match.group(1), match.group(2)
    return token or "", ""


def token_code_tuple(token: str) -> Optional[Tuple[str, ...]]:
    """Return slash codes on a gold token (``cat/s/z`` → ``('s', 'z')``)."""
    core, _punct = _split_trailing_punct(token)
    if "/" not in core:
        return None
    parts = core.split("/")
    if len(parts) < 2 or not parts[0]:
        return None
    return tuple(parts[1:])


def filter_line_to_convention(original: str, gold: str, convention: str) -> str:
    """Keep only the target family's marks; restore other tokens from the input.

    Focused prompts say to leave non-target families unmarked, so the gold
    line must match that instruction. Final / unknown conventions are unchanged.
    """
    if not convention or convention == "Final":
        return gold
    allowed = CONVENTION_CODE_TUPLES.get(convention)
    if not allowed:
        return gold
    orig_toks = original.split()
    gold_toks = gold.split()
    n = max(len(orig_toks), len(gold_toks))
    out = []
    for i in range(n):
        gold_tok = gold_toks[i] if i < len(gold_toks) else ""
        orig_tok = orig_toks[i] if i < len(orig_toks) else gold_tok
        codes = token_code_tuple(gold_tok)
        out.append(gold_tok if codes in allowed else orig_tok)
    return " ".join(out)


def morpheme_tp_fp_fn(expected: str, actual: str) -> Tuple[int, int, int]:
    """Multiset true positives, false positives, false negatives for marked morphemes."""
    key_counts = Counter(extract_morphemes(expected))
    pred_counts = Counter(extract_morphemes(actual))
    tp = sum((key_counts & pred_counts).values())
    fp = sum((pred_counts - key_counts).values())
    fn = sum((key_counts - pred_counts).values())
    return tp, fp, fn


def words_without_speaker(text: str) -> List[str]:
    """Drop the leading speaker ID token (e.g. C, P, A) from a transcript line."""
    words = text.split()
    if words and len(words[0]) == 1 and words[0].isalpha():
        return words[1:]
    return words


def word_level_accuracy_line(expected: str, actual: str) -> Tuple[int, int]:
    """Return (matching_words, reference_word_count) for one line (speaker ID excluded)."""
    exp_words = words_without_speaker(expected)
    if not exp_words:
        return (0, 0)
    act_words = words_without_speaker(actual)
    matches = sum(1 for i, word in enumerate(exp_words) if i < len(act_words) and act_words[i] == word)
    return matches, len(exp_words)


def _token_key(token: str) -> str:
    """Lowercased token with light punctuation stripped for lexicon lookup."""
    return (token or "").lower().strip(".,!?;:\"'()[]")


def is_marked_token(token: str) -> bool:
    """True if the token is a SALT slash mark (e.g. block/s, eat/en)."""
    return bool(MORPHEME_PATTERN.search(token or ""))


def is_bm_distractor_token(token: str) -> bool:
    """True if token surface form is in the BM distractor lexicon."""
    return _token_key(token) in BM_DISTRACTORS


def bm_test_word_indices(original: str, expected: str) -> List[Tuple[int, str]]:
    """
    Positions that count toward BM WLA.

    Returns (index_in_expected_words, kind) where kind is ``target`` or ``distractor``.
    Targets = gold-marked tokens. Distractors = unmarked gold tokens whose surface
    form (preferring the original transcript token) is in BM_DISTRACTORS.
    """
    exp_words = words_without_speaker(expected)
    orig_words = words_without_speaker(original) if original else []
    out: List[Tuple[int, str]] = []
    for i, exp_tok in enumerate(exp_words):
        if is_marked_token(exp_tok):
            out.append((i, "target"))
            continue
        surface = orig_words[i] if i < len(orig_words) else exp_tok
        if is_bm_distractor_token(surface) or is_bm_distractor_token(exp_tok):
            out.append((i, "distractor"))
    return out


def bm_word_level_accuracy_line(
    original: str, expected: str, actual: str
) -> Tuple[int, int, int, int]:
    """
    BM WLA for one line.

    Returns (matching_test_words, total_test_words, n_targets, n_distractors).
    A test word is correct when the model token equals the gold token at that index.
    """
    exp_words = words_without_speaker(expected)
    act_words = words_without_speaker(actual)
    tests = bm_test_word_indices(original, expected)
    if not tests:
        return (0, 0, 0, 0)
    matches = 0
    n_targets = 0
    n_distractors = 0
    for i, kind in tests:
        if kind == "target":
            n_targets += 1
        else:
            n_distractors += 1
        exp_tok = exp_words[i]
        act_tok = act_words[i] if i < len(act_words) else ""
        if act_tok == exp_tok:
            matches += 1
    return matches, len(tests), n_targets, n_distractors


def precision_recall_f1(tp: int, fp: int, fn: int) -> Tuple[float, float, float]:
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def compute_run_metrics(results: List[Dict]) -> Dict:
    """
    Aggregate metrics across evaluation lines.

    Each result dict must include ``expected`` and ``actual`` keys.
    WLA = word-level accuracy (matching tokens / reference tokens).
    TP/FP/FN = morpheme-level detection counts (marked forms with /).
    BM WLA is no longer computed for new runs.
    """
    total = len(results)
    skipped = 0
    skipped_token_limit = 0
    skipped_api_error = 0
    skipped_model_unavailable = 0
    utterance_correct = 0
    matching_words = 0
    reference_words = 0
    tp = fp = fn = 0
    total_elapsed_seconds = 0.0

    for row in results:
        expected = row.get("expected") or ""
        actual = row.get("actual") or ""
        if not actual:
            skipped += 1
            reason = row.get("skip_reason")
            if reason == SKIP_TOKEN_LIMIT:
                skipped_token_limit += 1
            elif reason == SKIP_MODEL_UNAVAILABLE:
                skipped_model_unavailable += 1
            else:
                skipped_api_error += 1
            continue
        if actual == expected:
            utterance_correct += 1

        line_matches, line_ref_len = word_level_accuracy_line(expected, actual)
        matching_words += line_matches
        reference_words += line_ref_len

        line_tp, line_fp, line_fn = morpheme_tp_fp_fn(expected, actual)
        tp += line_tp
        fp += line_fp
        fn += line_fn
        total_elapsed_seconds += float(row.get("elapsed_seconds") or 0.0)

    scored = total - skipped
    wla = (matching_words / reference_words * 100.0) if reference_words > 0 else 0.0
    utterance_accuracy = (utterance_correct / scored * 100.0) if scored > 0 else 0.0
    precision, recall, f1 = precision_recall_f1(tp, fp, fn)
    latency_s_per_utt = (total_elapsed_seconds / scored) if scored > 0 else 0.0

    return {
        "total": total,
        "skipped": skipped,
        "skipped_token_limit": skipped_token_limit,
        "skipped_api_error": skipped_api_error,
        "skipped_model_unavailable": skipped_model_unavailable,
        "skipped_annotation": scored - utterance_correct,
        "scored": scored,
        "utterance_correct": utterance_correct,
        "utterance_incorrect": scored - utterance_correct,
        "utterance_accuracy": utterance_accuracy,
        "wla": wla,
        "matching_words": matching_words,
        "reference_words": reference_words,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision * 100.0,
        "recall": recall * 100.0,
        "f1": f1 * 100.0,
        "total_elapsed_seconds": total_elapsed_seconds,
        "latency_s_per_utt": latency_s_per_utt,
        # Legacy keys used elsewhere
        "correct": utterance_correct,
        "incorrect": scored - utterance_correct,
        "accuracy": utterance_accuracy,
        "f1_score": f1 * 100.0,
        "harmonic_mean": f1 * 100.0,
    }


def format_metrics_row(metrics: Dict) -> Dict[str, str]:
    """Single-row dict for display tables (matches spreadsheet-style headers)."""
    return {
        "WLA": f"{metrics['wla']:.2f}%",
        "TP": str(metrics["tp"]),
        "FP": str(metrics["fp"]),
        "FN": str(metrics["fn"]),
        "Precision": f"{metrics['precision']:.2f}%",
        "Recall": f"{metrics['recall']:.2f}%",
        "F1": f"{metrics['f1']:.2f}%",
        "Latency (s/utt)": f"{metrics.get('latency_s_per_utt', 0.0):.3f}",
    }


def aggregate_model_benchmark(per_transcript_metrics: List[Dict]) -> Dict:
    """Macro-average WLA/F1 across transcripts; pooled latency across all utterances."""
    if not per_transcript_metrics:
        return {
            "mean_wla": 0.0,
            "mean_f1": 0.0,
            "latency_s_per_utt": 0.0,
            "total_scored": 0,
            "total_elapsed_seconds": 0.0,
        }
    total_scored = sum(int(m.get("scored", 0)) for m in per_transcript_metrics)
    total_elapsed = sum(float(m.get("total_elapsed_seconds", 0.0)) for m in per_transcript_metrics)
    return {
        "mean_wla": statistics.mean(m["wla"] for m in per_transcript_metrics),
        "mean_f1": statistics.mean(m["f1"] for m in per_transcript_metrics),
        "latency_s_per_utt": (total_elapsed / total_scored) if total_scored > 0 else 0.0,
        "total_scored": total_scored,
        "total_elapsed_seconds": total_elapsed,
    }


def format_benchmark_table_row(model_label: str, agg: Dict) -> Dict[str, str]:
    """Row for the paper model-comparison table."""
    return {
        "Model": model_label,
        "Mean WLA (%)": f"{agg['mean_wla']:.2f}",
        "Mean F1": f"{agg['mean_f1']:.2f}",
        "Latency (s/utt)": f"{agg['latency_s_per_utt']:.3f}",
    }


def _std(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    return statistics.stdev(values)


def summarize_trials(trial_metrics: List[Dict]) -> Dict:
    """Mean and standard deviation across multiple evaluation trials."""
    n = len(trial_metrics)
    summary = {"n_trials": n, "per_trial": trial_metrics}
    for key in TRIAL_NUMERIC_KEYS:
        values = [
            float(m[key])
            for m in trial_metrics
            if key in m and m[key] is not None
        ]
        if not values:
            continue
        summary[f"{key}_mean"] = statistics.mean(values)
        summary[f"{key}_std"] = _std(values)
        summary[f"{key}_min"] = min(values)
        summary[f"{key}_max"] = max(values)
    return summary


def format_mean_std(mean: float, std: float, as_percent: bool) -> str:
    if as_percent:
        return f"{mean:.2f}% ± {std:.2f}%"
    if std == 0:
        return f"{mean:.1f}"
    return f"{mean:.1f} ± {std:.1f}"


def format_trial_summary_row(summary: Dict) -> Dict[str, str]:
    """Aggregate row (mean ± std) for multi-trial runs."""
    n = summary["n_trials"]
    label = f"Mean ± std (n={n})"
    return {
        "Run": label,
        "WLA": format_mean_std(summary["wla_mean"], summary["wla_std"], True),
        "TP": format_mean_std(summary["tp_mean"], summary["tp_std"], False),
        "FP": format_mean_std(summary["fp_mean"], summary["fp_std"], False),
        "FN": format_mean_std(summary["fn_mean"], summary["fn_std"], False),
        "Precision": format_mean_std(summary["precision_mean"], summary["precision_std"], True),
        "Recall": format_mean_std(summary["recall_mean"], summary["recall_std"], True),
        "F1": format_mean_std(summary["f1_mean"], summary["f1_std"], True),
    }


def save_trial_summary(
    summary: Dict,
    results_dir: str,
    model_name: str,
    prompt_version: str,
    temperature: float,
    transcript_file: str,
    answer_key_file: Optional[str],
    saved_paths: List[str],
) -> str:
    """Write a text summary for multi-trial runs."""
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(
        results_dir,
        f"trials_summary_{model_name}_{prompt_version}_temp{temperature}_n{summary['n_trials']}_{timestamp}.txt",
    )
    os.makedirs(results_dir, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Trials: {summary['n_trials']}\n")
        f.write(f"Model: {model_name}\n")
        f.write(f"Prompt: {prompt_version}\n")
        f.write(f"Temperature: {temperature}\n")
        f.write(f"Transcript: {os.path.basename(transcript_file)}\n")
        if answer_key_file:
            f.write(f"Answer key: {os.path.basename(answer_key_file)}\n")
        f.write("\nAggregate (mean ± std):\n")
        row = format_trial_summary_row(summary)
        for k, v in row.items():
            if k != "Run":
                f.write(f"  {k}: {v}\n")
        f.write("\nPer-trial metrics:\n")
        for i, m in enumerate(summary["per_trial"], 1):
            f.write(f"\nTrial {i}:\n")
            for k, v in format_metrics_row(m).items():
                f.write(f"  {k}: {v}\n")
            if i <= len(saved_paths):
                f.write(f"  Saved: {saved_paths[i - 1]}\n")
    return filename
