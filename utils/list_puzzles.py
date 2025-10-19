import os
import json

# Grab all .py files in puzzles/, strip extension
puzzles = [
    os.path.splitext(f)[0]
    for f in os.listdir("puzzles")
    if f.endswith(".py")
]

# Write to GitHub Actions output
with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
    fh.write(f"puzzles={json.dumps(puzzles)}\n")