"""
evaluate.py

Compares sample_output.csv predictions against sample_claims.csv labels.
Prints per-field accuracy, overall exact-match accuracy, and every mismatch.
Saves results to evaluation/evaluation_report.md.
"""

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT   = Path(__file__).resolve().parents[2]
SAMPLE_CSV  = REPO_ROOT / "dataset" / "sample_claims.csv"
OUTPUT_CSV  = REPO_ROOT / "sample_output.csv"
REPORT_PATH = Path(__file__).parent / "evaluation_report.md"

FIELDS = [
    "claim_status",
    "issue_type",
    "object_part",
    "severity",
    "valid_image",
    "evidence_standard_met",
]


def norm(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower()


def main():
    if not SAMPLE_CSV.exists():
        print(f"ERROR: {SAMPLE_CSV} not found"); sys.exit(1)
    if not OUTPUT_CSV.exists():
        print(f"ERROR: {OUTPUT_CSV} not found"); sys.exit(1)

    truth = pd.read_csv(SAMPLE_CSV)
    pred  = pd.read_csv(OUTPUT_CSV)

    n = min(len(truth), len(pred))
    lines: list[str] = []

    def w(s: str = "") -> None:
        lines.append(s)
        print(s)

    w("# Baseline Evaluation Report")
    w(f"\nTotal rows compared: **{n}**")
    w()

    # ----------------------------------------------------------------
    # Per-field accuracy
    # ----------------------------------------------------------------
    w("## Per-Field Accuracy")
    w()
    w("| Field | Correct | Total | Accuracy |")
    w("|---|---|---|---|")

    field_scores: dict[str, float] = {}
    for field in FIELDS:
        if field not in truth.columns or field not in pred.columns:
            w(f"| {field} | — | — | MISSING |")
            continue
        t = norm(truth[field][:n])
        p = norm(pred[field][:n])
        correct = (t == p).sum()
        pct = correct / n * 100
        field_scores[field] = pct
        w(f"| {field} | {correct} | {n} | {pct:.0f}% |")

    # ----------------------------------------------------------------
    # Overall exact-row match (all FIELDS must match simultaneously)
    # ----------------------------------------------------------------
    exact_match = pd.Series([True] * n)
    for field in FIELDS:
        if field in truth.columns and field in pred.columns:
            exact_match &= (norm(truth[field][:n]) == norm(pred[field][:n]))
    exact_count = exact_match.sum()
    exact_pct   = exact_count / n * 100

    w()
    w("## Overall Exact-Row Match")
    w()
    w(f"**{exact_count}/{n} rows ({exact_pct:.0f}%)** — all 6 fields correct simultaneously.")
    w()

    # ----------------------------------------------------------------
    # Prediction distribution
    # ----------------------------------------------------------------
    w("## Predicted claim_status Distribution")
    w()
    for val, cnt in norm(pred["claim_status"][:n]).value_counts().items():
        w(f"- `{val}`: {cnt}")
    w()
    w("## Expected claim_status Distribution")
    w()
    for val, cnt in norm(truth["claim_status"][:n]).value_counts().items():
        w(f"- `{val}`: {cnt}")
    w()

    # ----------------------------------------------------------------
    # Mismatch details — every row, every field
    # ----------------------------------------------------------------
    w("## Mismatch Details")
    w()
    total_mismatches = 0
    for i in range(n):
        row_mismatches: list[str] = []
        for field in FIELDS:
            if field not in truth.columns or field not in pred.columns:
                continue
            t_val = norm(truth[field])[i]
            p_val = norm(pred[field])[i]
            if t_val != p_val:
                row_mismatches.append(f"  - **{field}**: expected `{t_val}` → got `{p_val}`")

        if row_mismatches:
            total_mismatches += 1
            uid = truth["user_id"].iloc[i]
            obj = truth["claim_object"].iloc[i]
            w(f"### Row {i+1} — {uid} ({obj})")
            for m in row_mismatches:
                w(m)
            w()

    if total_mismatches == 0:
        w("No mismatches found — perfect score!")

    w(f"**Total rows with at least one mismatch: {total_mismatches}/{n}**")

    # ----------------------------------------------------------------
    # Save report
    # ----------------------------------------------------------------
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
