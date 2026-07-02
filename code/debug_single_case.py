"""
debug_single_case.py

Runs ONE Gemini call against sample case_001 and prints:
  - raw response text
  - cleaned JSON string
  - parsed dict

Purpose: diagnose JSON parse failures without burning quota.
"""

import json
import logging
import sys
from pathlib import Path

# Enable DEBUG so _extract_json logs every step
logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")

sys.path.insert(0, str(Path(__file__).parent))

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from analyzers.gemini_analyzer import (
    ALLOWED_OBJECT_PARTS,
    MODEL,
    PROMPT_TEMPLATE,
    _extract_json,
    _load_image_part,
    _sanitise_response,
)

# ---------------------------------------------------------------------------
# Case under test
# ---------------------------------------------------------------------------
IMAGE_PATH   = "../dataset/images/sample/case_001/img_1.jpg"
USER_CLAIM   = (
    "Customer: Hi, I found new damage on my car after it was parked outside overnight. "
    "| Support: Sorry to hear that. Can you describe what changed? "
    "| Customer: The back of the car has a dent now. It was not there before. "
    "| Support: Did anything else break or is it mostly body damage? "
    "| Customer: Mostly the rear bumper area. I attached the photo I took this morning."
)
CLAIM_OBJECT = "car"
IMAGE_IDS    = ["img_1"]

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not set")
    sys.exit(1)

client = genai.Client(api_key=api_key)

image_part = _load_image_part(IMAGE_PATH)
if image_part is None:
    print(f"ERROR: image not found at {IMAGE_PATH}")
    sys.exit(1)

allowed_parts = " | ".join(sorted(ALLOWED_OBJECT_PARTS[CLAIM_OBJECT]))
prompt_text = PROMPT_TEMPLATE.format(
    claim_object=CLAIM_OBJECT,
    user_claim=USER_CLAIM,
    image_ids=", ".join(IMAGE_IDS),
    allowed_parts=allowed_parts,
)

print("\n" + "=" * 60)
print("CALLING GEMINI...")
print("=" * 60)

response = client.models.generate_content(
    model=MODEL,
    contents=[image_part, prompt_text],
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        temperature=0,
        max_output_tokens=1024,
    ),
)

raw_text = response.text

print("\n" + "=" * 60)
print(f"RAW RESPONSE  (length={len(raw_text)})")
print("=" * 60)
print(raw_text)

print("\n" + "=" * 60)
print(f"FIRST 500 CHARS")
print("=" * 60)
print(repr(raw_text[:500]))

print("\n" + "=" * 60)
print(f"LAST 500 CHARS")
print("=" * 60)
print(repr(raw_text[-500:]))

print("\n" + "=" * 60)
print("DIAGNOSTICS")
print("=" * 60)
print(f"  starts with ```  : {raw_text.strip().startswith('```')}")
print(f"  contains ```     : {'```' in raw_text}")
print(f"  first {{ position : {raw_text.find('{')}")
print(f"  last  }} position : {raw_text.rfind('}')}")
print(f"  total length     : {len(raw_text)}")

print("\n" + "=" * 60)
print("EXTRACTED JSON")
print("=" * 60)
try:
    parsed = _extract_json(raw_text.strip())
    json_str = json.dumps(parsed, indent=2)
    print(json_str)

    print("\n" + "=" * 60)
    print("SANITISED DICT")
    print("=" * 60)
    sanitised = _sanitise_response(parsed, IMAGE_IDS, CLAIM_OBJECT)
    print(json.dumps(sanitised, indent=2))

except json.JSONDecodeError as e:
    print(f"PARSE FAILED: {e}")
