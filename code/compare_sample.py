"""
compare_sample.py

Compares sample_output.csv predictions against sample_claims.csv labels.
Prints per-field accuracy, mismatch details, and saves evaluation/sample_metrics.txt.
"""

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT   = Path(__file__).resolve().parents[1]
SAMPLE_CSV  = REPO_ROOT / "dataset" / "sample_claims.csv"
PRED_CSV    = REPO_ROOT / "sample_output.csv"
METRICS_OUT = Path(__file__).parent / "evaluation" / "sample_metrics.txt"

FIELDS = [
    "claim_status",
    "issue_type",
    "object_part",
    "severity",
    "evidence_standard_met",
    "valid_image",
]


def load(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        print(f"ERROR: {label} not found at {path}")
        sys.exit(1)
    return pd.read_csv(path)


def normalise(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase and strip string fields for fair comparison."""
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip().str.lower()
    return df


def compare(truth: pd.DataFrame, pred: pd.DataFrame) -> list[str]:
    lines: list[str] = []

    if len(truth) != len(pred):
        lines.append(f"WARNING: row count mismatch — truth={len(truth)}, pred={len(pred)}")

    n = min(len(truth), len(pred))
    lines.append(f"Total rows compared: {n}\n")
    lines.append("=" * 60)

    # Per-field accuracy
    lines.append("\nACCURACY BY FIELD")
    lines.append("-" * 40)
    for field in FIELDS:
        if field not in truth.columns:
            lines.append(f"  {field:<30} MISSING in truth")
            continue
        if field not in pred.columns:
            lines.append(f"  {field:<30} MISSING in predictions")
            continue
        correct = (truth[field][:n] == pred[field][:n]).sum()
        pct = correct / n * 100
        lines.append(f"  {field:<30} {correct:>2}/{n}  ({pct:.0f}%)")

    # Per-row mismatch detail for claim_status (most important field)
    lines.append("\n" + "=" * 60)
    lines.append("CLAIM_STATUS MISMATCHES")
    lines.append("-" * 40)
    mismatches = 0
    for i in range(n):
        exp = truth["claim_status"].iloc[i]
        got = pred["claim_status"].iloc[i]
        if exp != got:
            mismatches += 1
            uid  = truth["user_id"].iloc[i] if "user_id" in truth.columns else str(i)
            obj  = truth["claim_object"].iloc[i] if "claim_object" in truth.columns else "?"
            lines.append(f"  [{uid}] ({obj})")
            lines.append(f"    EXPECTED : {exp}")
            lines.append(f"    PREDICTED: {got}")
            # Show issue_type and object_part for context
            if "issue_type" in truth.columns and "issue_type" in pred.columns:
                lines.append(f"    issue  exp={truth['issue_type'].iloc[i]}  got={pred['issue_type'].iloc[i]}")
            if "object_part" in truth.columns and "object_part" in pred.columns:
                lines.append(f"    part   exp={truth['object_part'].iloc[i]}  got={pred['object_part'].iloc[i]}")
            lines.append("")

    if mismatches == 0:
        lines.append("  No mismatches!")
    else:
        lines.append(f"  Total mismatches: {mismatches}/{n}")

    # Fallback detection — how many predictions are the unknown/fallback default
    lines.append("\n" + "=" * 60)
    lines.append("FALLBACK ROW DETECTION (issue_type=unknown → Gemini failed)")
    lines.append("-" * 40)
    if "issue_type" in pred.columns:
        fallbacks = (pred["issue_type"][:n] == "unknown").sum()
        lines.append(f"  Rows with issue_type=unknown: {fallbacks}/{n}  ({fallbacks/n*100:.0f}%)")
        lines.append("  NOTE: These rows hit 429/503 and used fallback values.")
        lines.append("  Re-run after quota resets for valid baseline.")

    # claim_status distribution
    lines.append("\n" + "=" * 60)
    lines.append("PREDICTED claim_status DISTRIBUTION")
    lines.append("-" * 40)
    if "claim_status" in pred.columns:
        for val, cnt in pred["claim_status"][:n].value_counts().items():
            lines.append(f"  {val:<30} {cnt}")

    lines.append("\n" + "=" * 60)
    lines.append("EXPECTED claim_status DISTRIBUTION")
    lines.append("-" * 40)
    if "claim_status" in truth.columns:
        for val, cnt in truth["claim_status"][:n].value_counts().items():
            lines.append(f"  {val:<30} {cnt}")

    return lines


def main():
    truth = normalise(load(SAMPLE_CSV, "sample_claims.csv"))
    pred  = normalise(load(PRED_CSV,   "sample_output.csv"))

    lines = compare(truth, pred)
    report = "\n".join(lines)

    print(report)

    METRICS_OUT.parent.mkdir(parents=True, exist_ok=True)
    METRICS_OUT.write_text(report, encoding="utf-8")
    print(f"\nSaved to: {METRICS_OUT}")


if __name__ == "__main__":
    main()
