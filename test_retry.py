import re
import time

def test_retry_logic(error_str, attempt):
    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
        wait_time = 15 * attempt
        match = re.search(r"retry in (\d+(?:\.\d+)?)s", error_str)
        if match:
            wait_time = float(match.group(1)) + 1.0
        return f"Wait time calculated: {wait_time:.1f} seconds"
    return "Not a rate limit error"

errors = [
    # Google's exact error format
    "429 RESOURCE_EXHAUSTED. {'error': {'message': '... Please retry in 44.359593941s.'}}",
    # Similar error without exact retry time (should fallback to exponential)
    "429 RESOURCE_EXHAUSTED limit reached",
    # A short retry time
    "429 ... Please retry in 5.4s.",
]

print("--- RUNNING HARD TESTS ON RETRY LOGIC ---")
for i, err in enumerate(errors):
    print(f"Test {i+1}: {test_retry_logic(err, 1)}")

