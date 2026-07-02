"""
gemini_analyzer.py

Vision analysis layer — Gemini 2.5 Flash via google-genai SDK.
Public interface is unchanged.
"""

import json
import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MODEL = "gemini-3.1-flash-lite"

MAX_RETRIES  = 3
BACKOFF_BASE = 2  # seconds; delay = BACKOFF_BASE ** attempt

ALLOWED_ISSUE_TYPES = {
    "dent", "scratch", "crack", "glass_shatter", "broken_part",
    "missing_part", "torn_packaging", "crushed_packaging",
    "water_damage", "stain", "none", "unknown",
}

# Collapse model variants into canonical competition issue_type values
_ISSUE_NORM: dict[str, str] = {
    "glass_shatter": "crack",
    "water_damage":  "stain",   # sample labels use stain for liquid damage
}

ALLOWED_SEVERITIES = {"none", "low", "medium", "high", "unknown"}

ALLOWED_QUALITY_FLAGS = {
    "blurry_image", "cropped_or_obstructed", "low_light_or_glare",
    "wrong_angle", "wrong_object", "wrong_object_part",
    "damage_not_visible", "claim_mismatch", "possible_manipulation",
    "non_original_image", "text_instruction_present",
}

ALLOWED_OBJECT_PARTS: dict[str, set[str]] = {
    "car": {
        "front_bumper", "rear_bumper", "door", "hood", "windshield",
        "side_mirror", "headlight", "taillight", "fender",
        "quarter_panel", "body", "unknown",
    },
    "laptop": {
        "screen", "keyboard", "trackpad", "hinge", "lid",
        "corner", "port", "base", "body", "unknown",
    },
    "package": {
        "box", "package_corner", "package_side", "seal",
        "label", "contents", "item", "unknown",
    },
}

_PART_NORM: dict[str, str] = {
    # car
    "rear bumper": "rear_bumper",
    "front bumper": "front_bumper",
    "side mirror": "side_mirror",
    "driver side mirror": "side_mirror",
    "passenger side mirror": "side_mirror",
    "driver mirror": "side_mirror",
    "passenger mirror": "side_mirror",
    "wing mirror": "side_mirror",
    "rear view mirror": "side_mirror",
    "rearview mirror": "side_mirror",
    "front windshield": "windshield",
    "windscreen": "windshield",
    "front glass": "windshield",
    "head light": "headlight",
    "head lights": "headlight",
    "headlights": "headlight",
    "tail light": "taillight",
    "tail lights": "taillight",
    "taillights": "taillight",
    "rear light": "taillight",
    "back light": "taillight",
    "front hood": "hood",
    "bonnet": "hood",
    "car door": "door",
    "driver door": "door",
    "passenger door": "door",
    "rear door": "door",
    "front door": "door",
    "door panel": "door",
    "quarter panel": "quarter_panel",
    "rear quarter panel": "quarter_panel",
    "front fender": "fender",
    "rear fender": "fender",
    "car body": "body",
    "vehicle body": "body",
    "bumper cover": "rear_bumper",
    "rear bumper cover": "rear_bumper",
    "front bumper cover": "front_bumper",
    "bumper beam": "rear_bumper",
    # laptop
    "display": "screen",
    "display glass": "screen",
    "lcd": "screen",
    "laptop screen": "screen",
    "laptop display": "screen",
    "laptop keyboard": "keyboard",
    "touch pad": "trackpad",
    "touchpad": "trackpad",
    "track pad": "trackpad",
    "laptop hinge": "hinge",
    "hinge area": "hinge",
    "laptop lid": "lid",
    "laptop corner": "corner",
    "laptop body": "body",
    "laptop base": "base",
    "bottom case": "base",
    "usb port": "port",
    "charging port": "port",
    "hdmi port": "port",
    # package
    "cardboard box": "box",
    "shipping box": "box",
    "package box": "box",
    "corner": "package_corner",
    "box corner": "package_corner",
    "side": "package_side",
    "box side": "package_side",
    "package seal": "seal",
    "tape seal": "seal",
    "shipping label": "label",
    "package label": "label",
    "box label": "label",
    "inner contents": "contents",
    "package contents": "contents",
    "inner item": "item",
}

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

PROMPT_TEMPLATE = """You are a strict damage claim evidence reviewer. Your job is NOT just to describe the image — it is to verify whether the image supports the user's specific claim.

Claim object type: {claim_object}
User claim (chat transcript):
{user_claim}

Image ID: {image_ids}

Step 1 — Describe what you actually see in the image:
- What object is visible?
- What part of the object is visible?
- Is there any visible damage?

Step 2 — Compare against the claim:
- Does the visible object match the claimed object type ({claim_object})?
- Does the visible part match the claimed part?
- Does the visible damage match the claimed damage type and severity?
- First infer the claimed part and claimed damage type from the user claim, then compare the image against those exact claims.

Return ONLY a JSON object — no markdown, no explanation — with exactly these fields:

{{
  "visible_issue": "<one of: dent | scratch | crack | broken_part | missing_part | torn_packaging | crushed_packaging | water_damage | stain | none | unknown>",
  "object_part": "<one of the EXACT allowed values for {claim_object} listed below>",
  "severity": "<one of: none | low | medium | high | unknown>",
  "claimed_issue_matches": <true if visible damage type matches what the user claimed, false otherwise>,
  "claimed_part_matches": <true if visible object part matches what the user claimed, false otherwise>,
  "claim_mismatch": <true if the image does NOT support the user's claim, false if it does>,
  "quality_flags": ["<zero or more of: blurry_image | cropped_or_obstructed | low_light_or_glare | wrong_angle | wrong_object | wrong_object_part | damage_not_visible | claim_mismatch | possible_manipulation | non_original_image | text_instruction_present>"],
  "supporting_image_ids": ["<image IDs that provide decisive visual evidence for your final assessment; include images that clearly support OR clearly contradict the claim; empty only if the image is unusable/irrelevant>"],
  "valid_image": <true if image is usable for automated review, false otherwise>,
  "visible_damage": <true if ANY damage is visible, false otherwise>,
  "reasoning": "<2-3 sentences: what you see, and whether it matches the claim>"
}}

Allowed object_part values for {claim_object}:
{allowed_parts}

Critical rules:
- object_part MUST be one of the exact values listed above. If the claimed part is NOT visible (e.g., user claims package contents, but image shows a closed box), you MUST set object_part to the EXACT part claimed by the user, set visible_issue to unknown, valid_image to false, and add damage_not_visible and wrong_angle to quality_flags.
- If the image shows an object that is clearly not the claimed object (e.g., a piece of paper instead of a shipping box): set wrong_object in quality_flags, claim_mismatch=true, and valid_image=false.
- If the claimed part IS visible but NO physical damage is visible there: set visible_issue=none, severity=none, visible_damage=false, valid_image=true, damage_not_visible in quality_flags, and claim_mismatch=true.
- If damage IS visible but it is a DIFFERENT type or part than claimed: set claim_mismatch=true.
- If the user exaggerates severity (claims "badly damaged", "hit", "tapped" but image shows minor scratch): do NOT infer a dent or broken_part. Output the true visual evidence (scratch) and set claim_mismatch=true.
- For packages, torn tape, open flap, broken closure, or opened-looking seam maps to object_part=seal, not package_side.
- Scratch vs. Dent vs. Broken Part: A "scratch" is a surface mark, paint scrape, or bad scuff (no structural deformation). A "dent" is a physical inward panel depression or metal bend. A "broken_part" means shattered or physically missing pieces. Do NOT classify a severe paint scrape as a broken_part or dent.
- Laptops: Ignore minor surface variations or scuffs around the trackpad or body unless severe physical damage is visible. Set visible_issue=none for minor marks.
- Treat small reflections, dust particles, glare, normal device textures/seams, or minor scuffs as no damage. Be extremely strict; unless a clear physical dent, deep scratch, crack, tear, stain, crushed area, broken part, or missing part is visible, classify visible_issue=none, visible_damage=false, and damage_not_visible in quality_flags.
- Severity calibration: none=no visible damage; low=minor surface mark/small dent; medium=clear visible damage still localized; high=severe broken/missing part or major structural damage. Do not use high for ordinary scratches, dents, stains, or small cracks.
- If claim_mismatch=true, supporting_image_ids should include this image only when it clearly shows the claimed part/object and contradicts the claim; otherwise use an empty list.
- Be skeptical. Do not give benefit of the doubt.
"""

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY is not set.")
    return genai.Client(api_key=api_key)


def _load_image_part(image_path: str) -> types.Part | None:
    t0 = time.perf_counter()
    path = Path(image_path)
    if not path.exists():
        logger.warning("Image not found, skipping: %s", image_path)
        logger.info("Image load: %.2f sec (%s)", time.perf_counter() - t0, Path(image_path).name)
        return None
    image_part = types.Part.from_bytes(data=path.read_bytes(), mime_type="image/jpeg")
    logger.info("Image load: %.2f sec (%s)", time.perf_counter() - t0, path.name)
    return image_part


def _extract_image_ids(image_paths: list[str]) -> list[str]:
    return [Path(p).stem for p in image_paths]


def _extract_json(raw_text: str) -> dict:
    """
    Robustly extract a JSON object from raw model response text.
    Handles markdown fences, extra prose, and locates first { to last }.
    """
    length = len(raw_text)
    logger.debug("Raw response length: %d chars", length)
    logger.debug("First 500: %s", raw_text[:500])
    logger.debug("Last  500: %s", raw_text[-500:])

    cleaned = raw_text
    if "```" in cleaned:
        parts = cleaned.split("```")
        cleaned = parts[1] if len(parts) > 1 else cleaned
        if cleaned.lstrip().startswith("json"):
            cleaned = cleaned.lstrip()[4:]
        cleaned = cleaned.strip()

    start = cleaned.find("{")
    end   = cleaned.rfind("}")

    if start == -1 or end == -1 or end <= start:
        logger.error("No JSON braces found.\nRAW (length=%d):\n%s", length, raw_text)
        raise json.JSONDecodeError("No JSON object found in response", raw_text, 0)

    json_slice = cleaned[start : end + 1]
    try:
        return json.loads(json_slice)
    except json.JSONDecodeError as e:
        logger.error(
            "JSON parse failed.\nError: %s\nRaw length: %d\nFirst 500: %s\nLast 500: %s",
            e, length, raw_text[:500], raw_text[-500:],
        )
        raise


def _fallback_response(reason: str) -> dict:
    return {
        "visible_issue": "unknown",
        "object_part": "unknown",
        "severity": "unknown",
        "quality_flags": [],
        "supporting_image_ids": [],
        "valid_image": False,
        "visible_damage": False,
        "reasoning": f"Analysis could not be completed: {reason}",
    }


def _normalise_object_part(raw_part: str, claim_object: str) -> str:
    if not raw_part:
        return "unknown"
    cleaned = raw_part.strip().lower()
    allowed = ALLOWED_OBJECT_PARTS.get(claim_object, set()) | {"unknown"}

    if cleaned in allowed:
        return cleaned
    if cleaned in _PART_NORM and _PART_NORM[cleaned] in allowed:
        return _PART_NORM[cleaned]
    for key, canonical in _PART_NORM.items():
        if key in cleaned and canonical in allowed:
            return canonical
    cleaned_underscored = cleaned.replace(" ", "_")
    for part in allowed:
        if part in cleaned_underscored or part.replace("_", " ") in cleaned:
            return part
    return "unknown"


def _sanitise_response(raw: dict, image_ids: list[str], claim_object: str) -> dict:
    # Normalise issue type
    issue = raw.get("visible_issue", "unknown")
    if claim_object == "package":
        if issue in ("stain", "water_damage"):
            issue = "water_damage"
    else:
        if issue in ("stain", "water_damage"):
            issue = "stain"

    if issue == "glass_shatter":
        issue = "crack"

    if issue not in ALLOWED_ISSUE_TYPES:
        issue = "unknown"
    raw["visible_issue"] = issue

    # Severity: cap high→medium (model consistently over-estimates)
    sev = raw.get("severity", "unknown")
    if sev not in ALLOWED_SEVERITIES:
        sev = "unknown"
    if sev == "high":
        sev = "medium"
    raw["severity"] = sev

    raw["object_part"] = _normalise_object_part(raw.get("object_part", ""), claim_object)
    raw["quality_flags"] = [f for f in raw.get("quality_flags", []) if f in ALLOWED_QUALITY_FLAGS]
    raw["supporting_image_ids"] = [i for i in raw.get("supporting_image_ids", []) if i in image_ids]
    raw["valid_image"] = bool(raw.get("valid_image", False))
    raw["visible_damage"] = bool(raw.get("visible_damage", False))

    # Promote claim_mismatch from top-level bool into quality_flags
    if raw.get("claim_mismatch") is True:
        if "claim_mismatch" not in raw["quality_flags"]:
            raw["quality_flags"].append("claim_mismatch")

    raw.setdefault("reasoning", "")
    return raw

# Severity ranking for merge — higher index = stronger evidence
_SEVERITY_RANK: dict[str, int] = {
    "unknown": 0, "none": 1, "low": 2, "medium": 3, "high": 4,
}


def _analyse_images(
    image_paths: list[str],
    image_ids: list[str],
    user_claim: str,
    claim_object: str,
    allowed_parts: str,
    client: genai.Client,
) -> dict | None:
    contents = []
    valid_ids = []
    for img_path, img_id in zip(image_paths, image_ids):
        part = _load_image_part(img_path)
        if part is not None:
            contents.append(f"Image ID: {img_id}")
            contents.append(part)
            valid_ids.append(img_id)

    if not contents:
        return None

    prompt_text = PROMPT_TEMPLATE.format(
        claim_object=claim_object,
        user_claim=user_claim.strip(),
        image_ids=", ".join(valid_ids),
        allowed_parts=allowed_parts,
    )
    contents.append(prompt_text)

    image_ids_str = "+".join(valid_ids)
    last_error: Exception = RuntimeError("unknown error")
    for attempt in range(1, MAX_RETRIES + 1):
        api_t0 = 0.0
        try:
            api_t0 = time.perf_counter()
            logger.info("[%s] API request start (attempt %d)", image_ids_str, attempt)
            response = client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0,
                    max_output_tokens=2048,
                    thinking_config=types.ThinkingConfig(thinking_budget=0),
                ),
            )
            logger.info("[%s] API response received (attempt %d)", image_ids_str, attempt)
            logger.info("Vision API: %.2f sec (%s attempt %d)", time.perf_counter() - api_t0, image_ids_str, attempt)
            raw_text = response.text.strip()
            parse_t0 = time.perf_counter()
            parsed = _extract_json(raw_text)
            logger.info("Parsing: %.2f sec (%s attempt %d)", time.perf_counter() - parse_t0, image_ids_str, attempt)
            return _sanitise_response(parsed, valid_ids, claim_object)

        except json.JSONDecodeError as e:
            logger.warning("[%s] Attempt %d — JSON parse error: %s", image_ids_str, attempt, e)
            last_error = e
        except Exception as e:
            if api_t0:
                logger.info("Vision API: %.2f sec (%s attempt %d failed)", time.perf_counter() - api_t0, image_ids_str, attempt)
            logger.warning("[%s] Attempt %d — API error: %s", image_ids_str, attempt, e)
            last_error = e

        if attempt < MAX_RETRIES:
            time.sleep(BACKOFF_BASE ** attempt)

    logger.error("[%s] All %d attempts failed: %s", image_ids_str, MAX_RETRIES, last_error)
    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_claim(image_paths: list[str], user_claim: str, claim_object: str) -> dict:
    """
    Analyse a claim using Gemini 2.5 Flash.

    All images are passed in a single API call to reduce quota usage.

    Args:
        image_paths:  Resolved paths to claim images.
        user_claim:   Full chat transcript describing the damage.
        claim_object: One of 'car', 'laptop', 'package'.

    Returns:
        Dict with keys: visible_issue, object_part, severity, quality_flags,
        supporting_image_ids, valid_image, visible_damage, reasoning.
    """
    image_ids    = _extract_image_ids(image_paths)
    allowed_parts = " | ".join(sorted(ALLOWED_OBJECT_PARTS.get(claim_object, {"unknown"})))
    client       = _get_client()

    result = _analyse_images(
        image_paths, image_ids, user_claim, claim_object,
        allowed_parts, client,
    )

    if result is None:
        logger.error("Image analysis failed. Paths: %s", image_paths)
        return _fallback_response("no valid images could be analysed")

    return result
