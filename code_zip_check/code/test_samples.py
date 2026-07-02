"""
test_samples.py

Runs analyze_claim() against 6 sample cases and prints
EXPECTED vs PREDICTED side by side. No decision logic. No CSV writes.
"""

import json
import sys
sys.path.insert(0, ".")

import pandas as pd
from analyzers.gemini_analyzer import analyze_claim

DATASET_ROOT = "../dataset"
SAMPLE_CSV   = f"{DATASET_ROOT}/sample_claims.csv"

# Cases to test — folder name maps to image path prefix
TARGET_CASES = ["case_001", "case_005", "case_006", "case_008", "case_009", "case_010"]

def resolve_paths(image_paths_str: str) -> list[str]:
    """Resolve each semicolon-separated path against the dataset root."""
    return [f"{DATASET_ROOT}/{p.strip()}" for p in image_paths_str.split(";")]

def main():
    df = pd.read_csv(SAMPLE_CSV)

    # Filter to only the 6 target cases by matching image_paths column
    df["_case"] = df["image_paths"].apply(lambda p: p.split("/")[2])
    df = df[df["_case"].isin(TARGET_CASES)].reset_index(drop=True)

    for _, row in df.iterrows():
        case_id     = row["_case"]
        image_paths = resolve_paths(row["image_paths"])

        print("=" * 60)
        print(f"CASE: {case_id}")
        print(f"Object: {row['claim_object']}  |  Images: {len(image_paths)}")
        print()

        print("EXPECTED:")
        print(f"  issue_type   : {row['issue_type']}")
        print(f"  object_part  : {row['object_part']}")
        print(f"  severity     : {row['severity']}")
        print(f"  claim_status : {row['claim_status']}")
        print()

        print("PREDICTED (Gemini):")
        result = analyze_claim(
            image_paths=image_paths,
            user_claim=row["user_claim"],
            claim_object=row["claim_object"],
        )
        print(json.dumps(result, indent=2))
        print()

        # Quick match summary
        issue_match  = "✓" if result["visible_issue"]  == row["issue_type"]   else "✗"
        part_match   = "✓" if result["object_part"]    == row["object_part"]  else "✗"
        sev_match    = "✓" if result["severity"]        == row["severity"]     else "✗"
        print(f"  Match → issue_type:{issue_match}  object_part:{part_match}  severity:{sev_match}")
        print()

if __name__ == "__main__":
    main()
