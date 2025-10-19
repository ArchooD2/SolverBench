import os
import json

puzzles = [
    name for name in os.listdir("puzzles")
    if os.path.isdir(os.path.join("puzzles", name))
]

# Output in GitHub Actions format
print(f"::set-output name=puzzles::{json.dumps(puzzles)}")
