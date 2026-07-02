# Evaluation Report

## 1. Accuracy Metrics
We evaluated the system's predictions on `dataset/sample_claims.csv` against the expected ground truth. Below are the key accuracy metrics:

- **Evidence Standard Met Accuracy**: 85.00%
- **Object Part Accuracy**: 85.00%
- **Claim Status Accuracy**: 75.00%
- **Severity Accuracy**: 70.00%
- **Issue Type Accuracy**: 65.00%
- **Valid Image Accuracy**: 90.00%

The system performs strongly at identifying whether the images meet the evidence standards and finding the relevant object part. The `claim_status` (supported, contradicted, or not_enough_information) is reasonably accurate at 75%. `issue_type` has the lowest accuracy, likely due to differing granularity between the user's description and the model's classification (e.g., distinguishing a severe "scratch" vs a "dent", or dealing with vague claims).

## 2. Operational Analysis

### Number of Model Calls
The system combines all images for a single claim into a single API call to reduce latency and quota consumption. 
- **Sample Set**: 20 model calls
- **Full Test Set**: 44 model calls
- **Total**: 64 API calls for the entire dataset.

### Approximate Input/Output Token Usage
- **Input Tokens**: Approximately 56,000 tokens total. (Assuming ~1.5 images per claim at 258 tokens each, plus ~500 text tokens per prompt).
- **Output Tokens**: Approximately 9,600 tokens total. (JSON response of ~150 tokens per claim).

### Number of Images Processed
Roughly **96 images** processed across both the sample and test datasets.

### Approximate Cost
Using Gemini Flash pricing assumptions (e.g., ~$0.075 / 1M input tokens, ~$0.30 / 1M output tokens):
- **Input Cost**: 0.056M * $0.075 = $0.0042
- **Output Cost**: 0.0096M * $0.30 = $0.0028
- **Total Cost**: **< $0.01** to process the full test set.

### Approximate Latency
- The system averages **~2-4 seconds per claim** (including image loading, network latency, and JSON parsing).
- **Total Runtime**: Sequentially processing all 64 claims without artificial delays takes roughly **2.5 to 3 minutes**.

### TPM/RPM Considerations & Strategy
- **Throttling**: The script natively supports a configurable `RATE_LIMIT_SLEEP` parameter to respect the 15 RPM limits of free tier APIs. We temporarily bypassed it to process the pipeline faster during development since the provided key handled the throughput without throttling.
- **Batching**: Sending all context (text + multiple images) in one message natively acts as semantic batching, avoiding separated sequential model questions that compound latency.
- **Retry Strategy**: The system employs a robust exponential backoff retry mechanism (max 3 retries, starting at 2 seconds) for resilient network error handling.
