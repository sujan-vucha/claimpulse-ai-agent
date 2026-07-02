"""
risk_engine.py

Deterministic. No Gemini calls. No CSV reads.
Derives history-based risk flags from user_history row.
Image-level flags come from Gemini and are merged in decision_engine.
"""


def compute_risk_flags(user_id: str, user_history: dict) -> list[str]:
    """
    Derive history-based risk flags for a claim.

    Args:
        user_id:      The user submitting the claim.
        user_history: Dict for this user from user_history.csv.
                      Empty dict if user not found.

    Returns:
        List of risk flag strings. ['none'] if no flags apply.
    """
    if not user_history:
        return ["none"]

    flags: list[str] = []

    # Flag 1: non-empty history_flags column
    history_flags = str(user_history.get("history_flags", "") or "").strip().lower()
    if history_flags and history_flags != "none":
        flags.append("user_history_risk")

    # Flag 2: more rejections than acceptances → manual review
    rejected = int(user_history.get("rejected_claim", 0) or 0)
    accepted = int(user_history.get("accept_claim", 0) or 0)
    if rejected > accepted:
        flags.append("manual_review_required")

    # Deduplicate, preserve order
    seen: set[str] = set()
    unique_flags: list[str] = []
    for f in flags:
        if f not in seen:
            seen.add(f)
            unique_flags.append(f)

    return unique_flags if unique_flags else ["none"]
