"""Pilot run (seed 114001, n=500/arm). Run BEFORE PREREG is locked."""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from trust_region import run_experiment, summarize  # noqa: E402

ARMS = [
    {"name": "s_README", "kind": "surface", "surface": "README"},
    {"name": "s_TODO", "kind": "surface", "surface": "TODO"},
    {"name": "s_source", "kind": "surface", "surface": "source"},
    {"name": "s_data", "kind": "surface", "surface": "data"},
    {"name": "p_mid", "kind": "position", "chunk": 2},
    {"name": "p_end", "kind": "position", "chunk": 3},
]

if __name__ == "__main__":
    out = run_experiment(114001, 500, ARMS)
    summary = summarize(114001, 500, ARMS, out)
    # Pilot summary only carries the arms it ran; position mid rate added.
    summary["rates"]["p_mid"] = round(sum(out["p_mid"]) / len(out["p_mid"]), 4)
    path = os.path.join(os.path.dirname(__file__), "results", "pilot.json")
    with open(path, "w") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
    print(json.dumps(summary, indent=2, sort_keys=True))
