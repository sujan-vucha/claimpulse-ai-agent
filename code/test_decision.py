import sys
sys.path.insert(0, ".")
from engines.decision_engine import make_decision

cases = [
    ("case_001 supported",    {"visible_issue":"dent",        "object_part":"rear_bumper", "severity":"medium", "quality_flags":[],                           "supporting_image_ids":["img_1"], "valid_image":True,  "visible_damage":True,  "reasoning":"Dent on rear bumper."}, True,  "Rear bumper visible.", ["none"]),
    ("case_006 nei",          {"visible_issue":"none",        "object_part":"headlight",   "severity":"none",   "quality_flags":["wrong_angle","damage_not_visible"], "supporting_image_ids":[], "valid_image":False, "visible_damage":False, "reasoning":"Glare."}, False, "Not visible.",         ["none"]),
    ("case_005 contradicted", {"visible_issue":"scratch",     "object_part":"rear_bumper", "severity":"low",    "quality_flags":["claim_mismatch"],            "supporting_image_ids":["img_1"], "valid_image":True,  "visible_damage":True,  "reasoning":"Minor scratch only."}, True, "Bumper visible.", ["user_history_risk"]),
    ("case_009 supported",    {"visible_issue":"crack",       "object_part":"screen",      "severity":"high",   "quality_flags":[],                           "supporting_image_ids":["img_1"], "valid_image":True,  "visible_damage":True,  "reasoning":"Crack visible."}, True,  "Screen visible.",      ["none"]),
    ("case_010 supported",    {"visible_issue":"broken_part", "object_part":"hinge",       "severity":"high",   "quality_flags":[],                           "supporting_image_ids":["img_1"], "valid_image":True,  "visible_damage":True,  "reasoning":"Hinge broken."}, True,  "Hinge visible.",       ["none"]),
    ("no_damage contradicted",{"visible_issue":"none",        "object_part":"trackpad",    "severity":"none",   "quality_flags":[],                           "supporting_image_ids":[],        "valid_image":True,  "visible_damage":False, "reasoning":"No damage."}, True, "Trackpad visible.",    ["none"]),
]

for label, gemini, esm, esmr, rf in cases:
    r = make_decision(gemini, esm, esmr, rf)
    print(f"{label}")
    print(f"  status  : {r['claim_status']}")
    print(f"  issue   : {r['issue_type']}")
    print(f"  part    : {r['object_part']}")
    print(f"  severity: {r['severity']}")
    print(f"  flags   : {r['risk_flags']}")
    print()
