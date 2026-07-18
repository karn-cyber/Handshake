# Handshake — Dynamo: Fix the Broken Terminal-Bench Task

Repaired Terminal-Bench 2 (Harbor) task. The task itself is simple (parse an
Apache-style access log into a small JSON report); the work was fixing the
broken **authoring** so the task is correct, reproducible, and graded honestly.

The fixed task lives in [`log-report/`](log-report).

## Verify

```bash
harbor run -p log-report -a oracle     # reference solution  -> reward 1 (PASS)
harbor run -p log-report --agent nop   # no-op agent         -> reward 0 (FAIL)
```

Both conditions hold: oracle → **reward 1.0**, nop → **reward 0.0**.

## Defects found and fixed

| # | File | Defect | Fix |
|---|------|--------|-----|
| 1 | `task.toml` | `artifacts = "/app/out.json"` was a **string** (schema requires a list) and pointed at a path the task never produces. | `artifacts = ["/app/report.json"]` — valid list, matching the real output. |
| 2 | `task.toml` | Missing `schema_version`; non-standard metadata; no author attribution. | Added `schema_version = "1.3"`, `[task].authors`, and canonical metadata fields. |
| 3 | `task.toml` | Deprecated `allow_internet`. | Replaced with `network_mode` and explicit `os = "linux"`. |
| 4 | `environment/Dockerfile` | Base image `python:latest` — not reproducible. | Pinned by digest: `python@sha256:9d7f2875…` (python:3.13-slim-bookworm). |
| 5 | `environment/Dockerfile` | **Leaked solution**: `COPY solution_hint.py` (a full reference implementation) into the agent image. | Removed the COPY and deleted the file. |
| 6 | `instruction.md` | Vague prose, no measurable criteria. | Rewrote with numbered success criteria consistent with the verifier (output path, exact keys/types, correctness). |
| 7 | `tests/test_outputs.py` | Verifier only checked the file **existed / was non-empty** — an empty `{}` would pass. | Parses the JSON and asserts the real values against ground truth (`total_requests=6`, `unique_ips=3`, `top_path=/index.html`). |
| 8 | `tests/test.sh` | Wrote reward to `/app/reward.txt` (Harbor never reads it) and produced no CTRF report. | Writes reward to `/logs/verifier/reward.txt`, emits `/logs/verifier/ctrf.json`, always (re)writes the reward. |

## Why the verifier is honest

- Ground truth lives in `tests/` (copied to `/tests` only at verify time), so the
  agent never sees it and cannot tamper with the pass/fail signal.
- The reward is recomputed from the agent's actual output on every run; a
  pre-existing reward file is never trusted.
