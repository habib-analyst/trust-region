"""Head-to-head run (fresh seed 114002, n=2000/arm). Run ONLY after PREREG.

Usage: python3 run_headtohead.py [output_name]
Default output: results/headline.json. Rerun with output_name
results/headline_rerun.json to check byte-identical determinism.
"""

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
    {"name": "a_README", "kind": "ablation", "surface": "README"},
    {"name": "a_TODO", "kind": "ablation", "surface": "TODO"},
    {"name": "a_source", "kind": "ablation", "surface": "source"},
    {"name": "a_data", "kind": "ablation", "surface": "data"},
    {"name": "h_README", "kind": "shuffle", "surface": "README"},
    {"name": "h_TODO", "kind": "shuffle", "surface": "TODO"},
    {"name": "h_source", "kind": "shuffle", "surface": "source"},
    {"name": "h_data", "kind": "shuffle", "surface": "data"},
]

if __name__ == "__main__":
    out_name = sys.argv[1] if len(sys.argv) > 1 else "headline.json"
    out = run_experiment(114002, 2000, ARMS)
    summary = summarize(114002, 2000, ARMS, out)
    # Ablation flatness (M3): max-min across ablation surface rates.
    abl_rates = [summary["rates"][f"a_{s}"]
                 for s in ("README", "TODO", "source", "data")]
    summary["ablation_flatness"] = round(max(abl_rates) - min(abl_rates), 4)
    path = os.path.join(os.path.dirname(__file__), "results", out_name)
    with open(path, "w") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
    print(json.dumps(summary, indent=2, sort_keys=True))
