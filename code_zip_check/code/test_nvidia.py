"""
test_nvidia.py

Proof-of-concept: sends case_001 image to NVIDIA's LLaMA-3.2-90B Vision
via the OpenAI-compatible API and returns structured JSON.

Usage:
    python test_nvidia.py
"""

import base64
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

IMAGE_PATH = "../dataset/images/sample/case_001/img_1.jpg"

PROMPT = """You are a damage claim reviewer. Inspect the image carefully.

Return ONLY a JSON object with exactly these fields — no markdown, no explanation:

{
  "visible_issue": "<dent | scratch | crack | broken_part | missing_part | none | unknown>",
  "object_part": "<the specific part of the object visible in the image>",
  "severity": "<none | low | medium | high | unknown>"
}"""


def load_image_b64(path: str) -> str:
    return base64.standard_b64encode(Path(path).read_bytes()).decode("utf-8")


def main():
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        print("ERROR: NVIDIA_API_KEY not set in .env")
        sys.exit(1)

    image_path = Path(IMAGE_PATH)
    if not image_path.exists():
        print(f"ERROR: Image not found at {image_path.resolve()}")
        sys.exit(1)

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
    )

    image_b64 = load_image_b64(IMAGE_PATH)

    print("Sending request to NVIDIA API...")

    response = client.chat.completions.create(
        model="meta/llama-3.2-90b-vision-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        },
                    },
                    {
                        "type": "text",
                        "text": PROMPT,
                    },
                ],
            }
        ],
        temperature=0,
        max_tokens=256,
    )

    raw = response.choices[0].message.content

    print("\n" + "=" * 60)
    print("RAW RESPONSE")
    print("=" * 60)
    print(raw)

    print("\n" + "=" * 60)
    print("PARSED JSON")
    print("=" * 60)

    # Extract JSON between first { and last }
    start = raw.find("{")
    end   = raw.rfind("}")
    if start == -1 or end == -1:
        print("ERROR: No JSON object found in response")
        sys.exit(1)

    try:
        parsed = json.loads(raw[start : end + 1])
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON parse failed: {e}")
        print(f"Slice attempted: {raw[start:end+1]}")


if __name__ == "__main__":
    main()
