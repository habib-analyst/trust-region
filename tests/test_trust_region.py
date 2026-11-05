"""Tests for the trust-region analog harness."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from trust_region import (  # noqa: E402
    PAYLOAD, TOKEN, run_arm, run_experiment, surface_start_chunk,
)


def test_payload_is_benign_proxy_only():
    assert TOKEN in PAYLOAD
    assert "DEBUG-TOKEN-7" in PAYLOAD
    # No real secret, credential, or disallowed instruction in the payload.
    for bad in ("password", "secret key", "api_key", "rm -rf", "sudo"):
        assert bad not in PAYLOAD.lower()


def test_surface_start_chunks_follow_task_order():
    assert surface_start_chunk("README") == 0
    assert surface_start_chunk("TODO") == 4
    assert surface_start_chunk("source") == 8
    assert surface_start_chunk("data") == 12


def test_no_surface_specific_parameters():
    # The same arm run with the same seed is deterministic.
    a = run_arm(1, "s_README", 200, inject_chunk=0)
    b = run_arm(1, "s_README", 200, inject_chunk=0)
    assert a == b


def test_commitment_off_is_flat_across_surfaces():
    # Content-only view: with p_commit=0 every surface follows at P_PRE.
    rates = []
    for s in ("README", "TODO", "source", "data"):
        out = run_arm(7, f"a_{s}", 2000, inject_chunk=surface_start_chunk(s),
                      p_commit=0.0)
        rates.append(sum(out) / len(out))
    assert max(rates) - min(rates) < 0.05


def test_early_chunks_follow_more_than_late_chunks():
    early = run_arm(3, "x", 2000, inject_chunk=0)
    late = run_arm(3, "x", 2000, inject_chunk=12)
    assert sum(early) / len(early) > sum(late) / len(late) + 0.30


def test_experiment_runs_all_kinds():
    spec = [
        {"name": "s_README", "kind": "surface", "surface": "README"},
        {"name": "p_end", "kind": "position", "chunk": 3},
        {"name": "a_source", "kind": "ablation", "surface": "source"},
        {"name": "h_data", "kind": "shuffle", "surface": "data"},
    ]
    out = run_experiment(5, 100, spec)
    assert set(out) == {"s_README", "p_end", "a_source", "h_data"}
    assert all(len(v) == 100 for v in out.values())
    assert all(x in (0, 1) for v in out.values() for x in v)
