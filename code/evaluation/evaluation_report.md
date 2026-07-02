# Baseline Evaluation Report

Total rows compared: **20**

## Per-Field Accuracy

| Field | Correct | Total | Accuracy |
|---|---|---|---|
| claim_status | 14 | 20 | 70% |
| issue_type | 13 | 20 | 65% |
| object_part | 15 | 20 | 75% |
| severity | 13 | 20 | 65% |
| valid_image | 17 | 20 | 85% |
| evidence_standard_met | 17 | 20 | 85% |

## Overall Exact-Row Match

**12/20 rows (60%)** — all 6 fields correct simultaneously.

## Predicted claim_status Distribution

- `supported`: 13
- `not_enough_information`: 4
- `contradicted`: 3

## Expected claim_status Distribution

- `supported`: 13
- `contradicted`: 5
- `not_enough_information`: 2

## Mismatch Details

### Row 2 — user_002 (car)
  - **claim_status**: expected `supported` → got `contradicted`
  - **issue_type**: expected `scratch` → got `broken_part`
  - **severity**: expected `low` → got `medium`

### Row 5 — user_005 (car)
  - **claim_status**: expected `contradicted` → got `supported`
  - **issue_type**: expected `scratch` → got `dent`
  - **severity**: expected `low` → got `medium`

### Row 6 — user_006 (car)
  - **issue_type**: expected `unknown` → got `none`
  - **object_part**: expected `headlight` → got `unknown`

### Row 8 — user_008 (car)
  - **claim_status**: expected `contradicted` → got `not_enough_information`
  - **issue_type**: expected `broken_part` → got `unknown`
  - **object_part**: expected `front_bumper` → got `unknown`
  - **severity**: expected `high` → got `unknown`
  - **evidence_standard_met**: expected `true` → got `false`

### Row 14 — user_020 (laptop)
  - **issue_type**: expected `none` → got `scratch`
  - **object_part**: expected `trackpad` → got `body`
  - **severity**: expected `none` → got `low`

### Row 18 — user_032 (package)
  - **claim_status**: expected `not_enough_information` → got `contradicted`
  - **issue_type**: expected `unknown` → got `none`
  - **object_part**: expected `contents` → got `box`
  - **severity**: expected `unknown` → got `none`
  - **valid_image**: expected `false` → got `true`

### Row 19 — user_033 (package)
  - **claim_status**: expected `contradicted` → got `not_enough_information`
  - **severity**: expected `low` → got `unknown`
  - **valid_image**: expected `true` → got `false`
  - **evidence_standard_met**: expected `true` → got `false`

### Row 20 — user_034 (package)
  - **claim_status**: expected `contradicted` → got `not_enough_information`
  - **issue_type**: expected `none` → got `unknown`
  - **object_part**: expected `seal` → got `unknown`
  - **severity**: expected `none` → got `unknown`
  - **valid_image**: expected `true` → got `false`
  - **evidence_standard_met**: expected `true` → got `false`

**Total rows with at least one mismatch: 8/20**