"""
test_multi_image.py

Verifies that multi-image claims are handled correctly:
  - case_001: 1 image  → single call path
  - case_002: 2 images → per-image calls + merge path
"""

import json
import sys
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

sys.path.insert(0, ".")
from analyzers.gemini_analyzer import analyze_claim

CASES = [
    {
        "label":        "case_001 (1 image) — dent, rear_bumper",
        "image_paths":  ["../dataset/images/sample/case_001/img_1.jpg"],
        "user_claim":   "The back of the car has a dent now. Mostly the rear bumper area.",
        "claim_object": "car",
    },
    {
        "label":        "case_002 (2 images) — scratch, front_bumper",
        "image_paths":  [
            "../dataset/images/sample/case_002/img_1.jpg",
            "../dataset/images/sample/case_002/img_2.jpg",
        ],
        "user_claim":   "Front side par mark aa gaya hai, bumper ke upar. Light theek hai, front bumper par scratch hai.",
        "claim_object": "car",
    },
    {
        "label":        "case_010 (2 images) — broken_part, hinge",
        "image_paths":  [
            "../dataset/images/sample/case_010/img_1.jpg",
            "../dataset/images/sample/case_010/img_2.jpg",
        ],
        "user_claim":   "The hinge area has broken and the screen wobbles. It slipped from the sofa.",
        "claim_object": "laptop",
    },
]

for case in CASES:
    print("\n" + "=" * 60)
    print(f"CASE: {case['label']}")
    print(f"Images: {len(case['image_paths'])}")
    print("=" * 60)

    result = analyze_claim(
        image_paths=case["image_paths"],
        user_claim=case["user_claim"],
        claim_object=case["claim_object"],
    )

    print(json.dumps(result, indent=2))
    print(f"\nvisible_issue : {result['visible_issue']}")
    print(f"object_part   : {result['object_part']}")
    print(f"severity      : {result['severity']}")
    print(f"valid_image   : {result['valid_image']}")
    print(f"visible_damage: {result['visible_damage']}")
    print(f"supporting_ids: {result['supporting_image_ids']}")
    print(f"quality_flags : {result['quality_flags']}")
