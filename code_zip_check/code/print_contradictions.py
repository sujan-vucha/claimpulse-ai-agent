import sys
import pandas as pd
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
truth = pd.read_csv(REPO / "dataset/sample_claims.csv")
pred  = pd.read_csv(REPO / "sample_output.csv")

TARGET_USERS = {"user_005","user_008","user_014","user_020","user_033","user_034"}

for i, row in truth.iterrows():
    if row["user_id"] not in TARGET_USERS:
        continue
    p = pred.iloc[i]
    print("=" * 70)
    print(f"USER: {row['user_id']}  OBJECT: {row['claim_object']}")
    print(f"CLAIM: {row['user_claim'][:300]}")
    print()
    print(f"EXPECTED  → status={row['claim_status']}  issue={row['issue_type']}  part={row['object_part']}  sev={row['severity']}")
    print(f"PREDICTED → status={p['claim_status']}  issue={p['issue_type']}  part={p['object_part']}  sev={p['severity']}")
    print()
