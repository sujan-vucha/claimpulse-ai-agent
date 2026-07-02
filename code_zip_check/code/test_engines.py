import sys
sys.path.insert(0, ".")

from analyzers.gemini_analyzer import analyze_claim
from engines.decision_engine import make_decision
from engines.evidence_engine import check_evidence_standard
from engines.risk_engine import compute_risk_flags

print("All imports OK")

gemini_ok  = {"visible_issue":"dent",    "object_part":"rear_bumper","severity":"medium","quality_flags":[],                             "supporting_image_ids":["img_1"],"valid_image":True, "visible_damage":True, "reasoning":"Dent visible."}
gemini_bad = {"visible_issue":"unknown", "object_part":"headlight",  "severity":"unknown","quality_flags":["wrong_angle","damage_not_visible"],"supporting_image_ids":[],"valid_image":False,"visible_damage":False,"reasoning":"Glare."}

print("evidence OK  :", check_evidence_standard(gemini_ok))
print("evidence FAIL:", check_evidence_standard(gemini_bad))

history_risky = {"history_flags":"severity_exaggeration", "rejected_claim":3, "accept_claim":1}
history_clean = {"history_flags":"none",                   "rejected_claim":0, "accept_claim":5}
history_empty = {}

print("risk risky:", compute_risk_flags("u1", history_risky))
print("risk clean:", compute_risk_flags("u2", history_clean))
print("risk empty:", compute_risk_flags("u3", history_empty))

# Full stack test
esm, esmr = check_evidence_standard(gemini_ok)
rf = compute_risk_flags("u1", history_risky)
decision = make_decision(gemini_ok, esm, esmr, rf)
print("decision:", decision["claim_status"], "|", decision["risk_flags"])
