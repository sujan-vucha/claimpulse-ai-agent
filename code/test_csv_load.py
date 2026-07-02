import sys
sys.path.insert(0, ".")
import pandas as pd
from pathlib import Path

REPO_ROOT   = Path(".").resolve().parent
DATASET_DIR = REPO_ROOT / "dataset"

claims  = pd.read_csv(DATASET_DIR / "claims.csv")
history = pd.read_csv(DATASET_DIR / "user_history.csv")

print("claims rows :", len(claims))
print("history rows:", len(history))
print("claims cols :", claims.columns.tolist())

history_dict = {str(r["user_id"]): r.to_dict() for _, r in history.iterrows()}
test_user = str(claims.iloc[0]["user_id"])
h = history_dict.get(test_user, {})
print("first user       :", test_user)
print("history_flags    :", h.get("history_flags", "NOT FOUND"))
print("rejected_claim   :", h.get("rejected_claim", "NOT FOUND"))
print("accept_claim     :", h.get("accept_claim", "NOT FOUND"))
print("CSV load OK")
