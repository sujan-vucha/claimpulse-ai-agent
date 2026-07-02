import sys
import json
sys.path.insert(0, ".")

from analyzers.gemini_analyzer import analyze_claim

result = analyze_claim(
    image_paths=["../dataset/images/sample/case_001/img_1.jpg"],
    user_claim="The back of the car has a dent now. Mostly the rear bumper area.",
    claim_object="car"
)

output = json.dumps(result, indent=2)

# Write to file as fallback in case stdout is swallowed
with open("test_output.json", "w") as f:
    f.write(output)

print(output, flush=True)
