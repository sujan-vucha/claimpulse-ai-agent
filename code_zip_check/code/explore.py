import pandas as pd

sample = pd.read_csv("../dataset/sample_claims.csv")
claims = pd.read_csv("../dataset/claims.csv")
history = pd.read_csv("../dataset/user_history.csv")
requirements = pd.read_csv("../dataset/evidence_requirements.csv")

print("=== SHAPES ===")
print("Sample:", sample.shape)
print("Claims:", claims.shape)
print("History:", history.shape)
print("Requirements:", requirements.shape)

print("\n=== COLUMNS ===")
print("sample:", sample.columns.tolist())
print("claims:", claims.columns.tolist())

print("\n=== DISTRIBUTIONS ===")
print("claim_status:\n", sample["claim_status"].value_counts())
print("\nissue_type:\n", sample["issue_type"].value_counts())
print("\nseverity:\n", sample["severity"].value_counts())

print("\n=== UNIQUE USERS IN HISTORY ===")
print(history["user_id"].nunique())

print("\n=== EVIDENCE REQUIREMENTS ===")
print(requirements.to_string())

print("\n=== SAMPLE HEAD 10 ===")
print(sample.head(10).to_string())
