"""
decision_engine.py

Pure deterministic logic. Converts Gemini visual observations into the
final claim_status and supporting fields required by the competition schema.

No Gemini calls. No CSV reads. No side effects.
"""

# ---------------------------------------------------------------------------
# Flag sets driving the three-way decision
# ---------------------------------------------------------------------------

# Any of these flags means we cannot evaluate the claim visually
_INSUFFICIENT_EVIDENCE_FLAGS = {
    "wrong_angle",
    "cropped_or_obstructed",
    "wrong_object_part",
}

# Any of these flags, combined with a visible-but-mismatched image, points to
# contradiction rather than insufficient evidence
_CONTRADICTION_FLAGS = {
    "claim_mismatch",
}

# issue_type values that represent "no damage present"
_NO_DAMAGE_ISSUES = {"none"}

# Severity soft-cap: if Gemini says high but no strong damage signal, pull back.
# Only applied when contradicted to avoid inflating severity on failed claims.
_SEVERITY_ORDER = ["none", "low", "medium", "high", "unknown"]


def _has_flag(flags: list[str], target_set: set[str]) -> bool:
    return bool(set(flags) & target_set)


def _build_justification(
    claim_status: str,
    visible_issue: str,
    object_part: str,
    quality_flags: list[str],
    reasoning: str,
    supporting_image_ids: list[str],
) -> str:
    """
    Build a concise, image-grounded justification string.
    Prefers Gemini's own reasoning when available; augments with flag context.
    """
    base = reasoning.strip() if reasoning else ""

    if claim_status == "supported":
        if supporting_image_ids and supporting_image_ids != ["none"]:
            ids = ", ".join(supporting_image_ids)
            return base or f"Image {ids} shows {visible_issue} on the {object_part}, supporting the claim."
        return base or f"The submitted image shows {visible_issue} on the {object_part}."

    if claim_status == "contradicted":
        if "claim_mismatch" in quality_flags:
            return base or (
                f"The visible damage ({visible_issue} on {object_part}) "
                "does not match what was claimed."
            )
        if visible_issue in _NO_DAMAGE_ISSUES:
            return base or f"The {object_part} is visible but shows no damage, contradicting the claim."
        return base or f"Image evidence contradicts the stated claim."

    # not_enough_information
    active = [f for f in quality_flags if f in _INSUFFICIENT_EVIDENCE_FLAGS]
    flag_str = ", ".join(active) if active else "insufficient visual evidence"
    return base or f"The claim cannot be verified due to: {flag_str}."


def make_decision(
    gemini_response: dict,
    evidence_standard_met: bool,
    evidence_standard_met_reason: str,
    risk_flags: list[str],
) -> dict:
    """
    Produce the final structured output for one claim.

    Decision rules (in priority order):
    1. NOT_ENOUGH_INFORMATION — any insufficient-evidence flag present, or
       valid_image=False and no visible damage.
    2. CONTRADICTED — object part visible, but damage is absent (none) or
       claim_mismatch flag is set.
    3. SUPPORTED — visible_damage=True and issue is not 'none'/'unknown'.
    4. Default fallback → NOT_ENOUGH_INFORMATION.

    Args:
        gemini_response:          Output dict from gemini_analyzer.analyze_claim().
        evidence_standard_met:    Bool from evidence_engine (passed through to output).
        evidence_standard_met_reason: Reason string from evidence_engine.
        risk_flags:               Combined list from risk_engine.

    Returns:
        Dict with keys: issue_type, object_part, claim_status,
        claim_status_justification, severity, supporting_image_ids,
        valid_image, evidence_standard_met, evidence_standard_met_reason,
        risk_flags.
    """
    visible_issue   = gemini_response.get("visible_issue", "unknown")
    object_part     = gemini_response.get("object_part", "unknown")
    severity        = gemini_response.get("severity", "unknown")
    quality_flags   = gemini_response.get("quality_flags", [])
    supporting_ids  = gemini_response.get("supporting_image_ids", [])
    valid_image     = gemini_response.get("valid_image", False)
    visible_damage  = gemini_response.get("visible_damage", False)
    reasoning       = gemini_response.get("reasoning", "")
    # claim_mismatch can arrive as top-level bool OR inside quality_flags
    claim_mismatch_direct = bool(gemini_response.get("claim_mismatch", False))

    # ------------------------------------------------------------------
    # Rule 1 — NOT_ENOUGH_INFORMATION
    # Triggered when visual evidence is structurally insufficient:
    # wrong angle, part not visible, image not usable, or no damage visible
    # and no clear contradiction either.
    # ------------------------------------------------------------------
    insufficient = _has_flag(quality_flags, _INSUFFICIENT_EVIDENCE_FLAGS)
    wrong_object = "wrong_object" in quality_flags

    if wrong_object:
        valid_image = False  # force valid_image to false when wrong object

    no_usable_image = not valid_image and not visible_damage

    if wrong_object:
        claim_status = "contradicted"

    elif claim_mismatch_direct or _has_flag(quality_flags, _CONTRADICTION_FLAGS):
        claim_status = "contradicted"

    elif insufficient or no_usable_image:
        claim_status = "not_enough_information"
        severity = "unknown"
        supporting_ids = supporting_ids if supporting_ids else []

    elif valid_image and visible_issue in _NO_DAMAGE_ISSUES:
        claim_status = "contradicted"

    # ------------------------------------------------------------------
    # Rule 3 — SUPPORTED
    # Visible damage present, issue is meaningful, no contradicting flags.
    # ------------------------------------------------------------------
    elif visible_damage and visible_issue not in ("none", "unknown"):
        claim_status = "supported"

    # ------------------------------------------------------------------
    # Rule 4 — Fallback (visible_issue=unknown, no flags, ambiguous)
    # ------------------------------------------------------------------
    else:
        claim_status = "not_enough_information"
        severity = "unknown"

    # Build justification grounded in Gemini's own reasoning
    justification = _build_justification(
        claim_status, visible_issue, object_part,
        quality_flags, reasoning, supporting_ids,
    )

    # Normalise supporting_image_ids to "none" string when empty
    # (matches competition output schema)
    supporting_ids_out = supporting_ids if supporting_ids else []

    # Merge quality_flags (image-level) into risk_flags, dedup, keep "none" clean
    all_flags = list(dict.fromkeys(risk_flags + quality_flags))
    all_flags = [f for f in all_flags if f != "none"] or ["none"]

    return {
        "issue_type":                   visible_issue,
        "object_part":                  object_part,
        "claim_status":                 claim_status,
        "claim_status_justification":   justification,
        "severity":                     severity,
        "supporting_image_ids":         supporting_ids_out,
        "valid_image":                  valid_image,
        "evidence_standard_met":        evidence_standard_met,
        "evidence_standard_met_reason": evidence_standard_met_reason,
        "risk_flags":                   all_flags,
    }
