"""
evidence_engine.py

Deterministic. No Gemini calls. No CSV reads.
Evaluates whether submitted images meet the minimum evidence standard.
"""

# Quality flags that directly mean evidence standard is NOT met
_FAILING_FLAGS = {
    "wrong_angle",
    "damage_not_visible",
    "cropped_or_obstructed",
    "wrong_object",
    "wrong_object_part",
}


def check_evidence_standard(gemini_response: dict) -> tuple[bool, str]:
    """
    Determine if image evidence meets the minimum standard.

    Args:
        gemini_response: Output dict from gemini_analyzer.analyze_claim().

    Returns:
        Tuple of (evidence_standard_met: bool, reason: str).
    """
    quality_flags = gemini_response.get("quality_flags", [])
    valid_image   = gemini_response.get("valid_image", False)
    object_part   = gemini_response.get("object_part", "unknown")

    # Hard fail: image not usable at all
    if not valid_image:
        return False, "The submitted image is not usable for automated review."

    # Hard fail: any flag that structurally blocks evaluation
    failing = [f for f in quality_flags if f in _FAILING_FLAGS]
    if failing:
        flag_str = ", ".join(failing)
        return False, (
            f"Evidence standard not met due to: {flag_str}. "
            f"The claimed part ({object_part}) could not be evaluated."
        )

    return True, (
        f"The submitted image is sufficient to evaluate the claim "
        f"on the {object_part}."
    )
