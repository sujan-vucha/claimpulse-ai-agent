import pandas as pd
import json

def main():
    ground_truth = pd.read_csv("dataset/sample_claims.csv")
    predictions = pd.read_csv("sample_output_eval.csv")

    # Merge on user_id to ensure we match the right rows
    merged = pd.merge(ground_truth, predictions, on="user_id", suffixes=('_gt', '_pred'))

    total = len(merged)
    metrics = {}

    columns_to_evaluate = [
        "evidence_standard_met",
        "issue_type",
        "object_part",
        "claim_status",
        "valid_image",
        "severity"
    ]

    for col in columns_to_evaluate:
        # Convert both to string and lowercase for robust comparison
        matches = (merged[col + '_gt'].astype(str).str.lower() == merged[col + '_pred'].astype(str).str.lower()).sum()
        accuracy = matches / total
        metrics[col + '_accuracy'] = accuracy

    print("Accuracy Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.2%}")

    with open("evaluation_metrics.json", "w") as f:
        json.dump(metrics, f)

if __name__ == "__main__":
    main()
