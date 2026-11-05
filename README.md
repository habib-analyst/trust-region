# trust-region — Project #114

Scripted analog of arXiv 2610.38867 ("Where You Inject Matters: The Trust
Region Effect in LLM Agents"). Question: does a sequential-reading +
commitment mechanism generate a trust-region structure — different follow
rates for the SAME payload placed in different surfaces and positions?

## Run

```bash
python3 -m pytest tests/ -q   # 6 tests
python3 run_pilot.py           # seed 114001, n=500/arm -> results/pilot.json
python3 run_headtohead.py headline.json        # seed 114002, n=2000/arm
python3 run_headtohead.py headline_rerun.json   # byte-identical rerun check
```

## Model (fixed in G0, before any pilot number)

- Task traversal order: README -> TODO -> source -> data, 4 chunks each.
  The agent always reads every surface (exposure = 1 by construction).
- Payload (identical in every arm, benign proxy only): the instruction to
  append a fictional token `DEBUG-TOKEN-7` to the output. Following = the
  token appears in the output. No real disallowed content anywhere.
- Surface-blind commitment mechanism: after each chunk the agent commits
  to its plan with probability 0.25; an instruction read while uncommitted
  is followed with probability 0.85, once committed with probability 0.15.
  There are no surface-specific parameters. Gradients emerge from
  order x commitment, and the two ablations (commitment-off, shuffled
  order) collapse them — that is the load-bearing test.

## Headline (fresh seed 114002, n=2000/arm)

| Arm | Follow rate |
|---|---|
| README | 0.8565 |
| TODO | 0.3825 |
| source | 0.2080 |
| data | 0.1690 |
| README middle / end | 0.5440 / 0.4485 |
| Ablation (commitment-off) | 0.8365–0.8635 (flat) |
| Shuffled order | 0.3960–0.4195 (flat) |

Docs−codedata +0.431 CI [0.4127, 0.4510]; README−data +0.6875;
start−end +0.408. All 7 locked PREREG bars pass. See PREREG.md and
KILLGATE.md for the bars and the per-gate verdicts.

## Scope honesty

Scripted analog only. The paper's LLM figures (GPT-5.4 README/TODO 2.6x
vs code/data, 3 testbeds, 36 surfaces, 24 risk categories) are context
only, never claimed as reproduced. The claim is that a
sequential-reading + commitment mechanism generates a trust-region
structure in this analog — not that real LLMs carry surface weights.
