"""
main.py

End-to-end pipeline.
Reads claims.csv, runs each claim through the full engine stack,
writes output.csv.

Usage:
    python main.py                          # processes dataset/claims.csv
    python main.py --input dataset/sample_claims.csv   # run on sample
"""

import argparse
import logging
import sys
import time
from pathlib import Path

import pandas as pd
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent))

from analyzers.gemini_analyzer import analyze_claim
from engines.decision_engine import make_decision
from engines.evidence_engine import check_evidence_standard
from engines.risk_engine import compute_risk_flags

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

REPO_ROOT    = Path(__file__).resolve().parents[1]
DATASET_DIR  = REPO_ROOT / "dataset"
DEFAULT_IN   = DATASET_DIR / "claims.csv"
DEFAULT_OUT  = REPO_ROOT / "output.csv"

# Sequential processing to avoid provider throttling (Gemini Free 2.5 Flash has 5 RPM limit).
RATE_LIMIT_SLEEP = 4  # seconds between calls

OUTPUT_COLUMNS = [
    "user_id", "image_paths", "user_claim", "claim_object",
    "evidence_standard_met", "evidence_standard_met_reason",
    "risk_flags", "issue_type", "object_part",
    "claim_status", "claim_status_justification",
    "supporting_image_ids", "valid_image", "severity",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_user_history(path: Path) -> dict[str, dict]:
    """Return dict keyed by user_id for O(1) lookup."""
    df = pd.read_csv(path)
    return {str(row["user_id"]): row.to_dict() for _, row in df.iterrows()}


def resolve_image_paths(image_paths_str: str) -> list[str]:
    """Resolve semicolon-separated CSV paths against dataset root."""
    return [str(DATASET_DIR / p.strip()) for p in image_paths_str.split(";")]


def format_list_field(values: list[str]) -> str:
    """Semicolon-join a list; return 'none' if empty."""
    clean = [v for v in values if v and v != "none"]
    return ";".join(clean) if clean else "none"


def process_claim(row: pd.Series, user_history: dict[str, dict]) -> dict:
    """
    Run a single claim through the full engine stack.
    Returns a flat dict ready to be written to output.csv.
    """
    user_id      = str(row["user_id"])
    image_paths  = resolve_image_paths(row["image_paths"])
    user_claim   = str(row["user_claim"])
    claim_object = str(row["claim_object"])

    # Step 1 — Gemini visual analysis
    gemini = analyze_claim(image_paths, user_claim, claim_object)

    # Step 2 — Evidence standard
    esm, esmr = check_evidence_standard(gemini)

    # Step 3 — History-based risk flags
    history_row = user_history.get(user_id, {})
    risk_flags  = compute_risk_flags(user_id, history_row)

    # Step 4 — Final decision
    decision_t0 = time.perf_counter()
    decision = make_decision(gemini, esm, esmr, risk_flags)
    logger.info("Decision: %.2f sec", time.perf_counter() - decision_t0)

    return {
        "user_id":                      user_id,
        "image_paths":                  row["image_paths"],
        "user_claim":                   user_claim,
        "claim_object":                 claim_object,
        "evidence_standard_met":        str(decision["evidence_standard_met"]).lower(),
        "evidence_standard_met_reason": decision["evidence_standard_met_reason"],
        "risk_flags":                   format_list_field(decision["risk_flags"]),
        "issue_type":                   decision["issue_type"],
        "object_part":                  decision["object_part"],
        "claim_status":                 decision["claim_status"],
        "claim_status_justification":   decision["claim_status_justification"],
        "supporting_image_ids":         format_list_field(decision["supporting_image_ids"]),
        "valid_image":                  str(decision["valid_image"]).lower(),
        "severity":                     decision["severity"],
    }

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default=str(DEFAULT_IN),  help="Path to claims CSV")
    parser.add_argument("--output", default=str(DEFAULT_OUT), help="Path for output CSV")
    args = parser.parse_args()

    claims_path = Path(args.input)
    output_path = Path(args.output)

    logger.info("Reading claims from: %s", claims_path)
    claims = pd.read_csv(claims_path)
    logger.info("Total claims to process: %d", len(claims))

    history = load_user_history(DATASET_DIR / "user_history.csv")
    logger.info("User history loaded: %d users", len(history))

    results  : list[dict] = []
    failures : list[int]  = []

    for idx, row in tqdm(claims.iterrows(), total=len(claims), desc="Processing claims"):
        try:
            result = process_claim(row, history)
            results.append(result)
            logger.info("[%d/%d] %s → %s", idx + 1, len(claims), row["user_id"], result["claim_status"])
        except Exception as e:
            logger.error("FAILED row %d (user=%s): %s", idx, row.get("user_id", "?"), e)
            failures.append(idx)
            results.append({
                "user_id":                      str(row.get("user_id", "unknown")),
                "image_paths":                  str(row.get("image_paths", "")),
                "user_claim":                   str(row.get("user_claim", "")),
                "claim_object":                 str(row.get("claim_object", "")),
                "evidence_standard_met":        "false",
                "evidence_standard_met_reason": f"Processing error: {e}",
                "risk_flags":                   "none",
                "issue_type":                   "unknown",
                "object_part":                  "unknown",
                "claim_status":                 "not_enough_information",
                "claim_status_justification":   f"Processing error: {e}",
                "supporting_image_ids":         "none",
                "valid_image":                  "false",
                "severity":                     "unknown",
            })

        if idx < len(claims) - 1:
            time.sleep(RATE_LIMIT_SLEEP)

    output_df = pd.DataFrame(results, columns=OUTPUT_COLUMNS)
    csv_t0 = time.perf_counter()
    output_df.to_csv(output_path, index=False)
    logger.info("CSV writing: %.2f sec", time.perf_counter() - csv_t0)

    logger.info("output.csv written to: %s", output_path)
    logger.info("Processed: %d  |  Failed: %d", len(results) - len(failures), len(failures))
    if failures:
        logger.warning("Failed rows (0-indexed): %s", failures)


if __name__ == "__main__":
    main()
