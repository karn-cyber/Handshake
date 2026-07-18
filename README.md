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
| 1 | `task.toml` | `artifacts = "/app/out.json"` was a **string** (schema requires an array) and pointed at a file the task never produces. | `artifacts = ["/app/report.json"]` — a top-level array matching the real output. |
| 2 | `environment/Dockerfile` | Base image `python:latest` — not reproducible. | Pinned by digest: `python@sha256:9d7f2875…` (python:3.13-slim-bookworm). |
| 3 | `environment/Dockerfile` | **Leaked solution**: `COPY solution_hint.py` (a full reference implementation) into the agent image. | Removed the `COPY` and deleted `environment/solution_hint.py` from the build context. |
| 4 | `tests/test_outputs.py` | Verifier only checked the file **existed / was non-empty** — an empty `{}` or wrong values would pass. | Parses the JSON and asserts the real values (`total_requests=6`, `unique_ips=3`, `top_path=/index.html`), one test per instruction criterion. |
| 5 | `tests/test.sh` | Wrote reward to `/app/reward.txt` (Harbor never reads it) and produced no CTRF report. | Writes reward to `/logs/verifier/reward.txt`, emits `/logs/verifier/ctrf.json`, always (re)writes the reward. |
| 6 | `instruction.md` | Vague prose, no measurable criteria. | Rewrote with numbered success criteria that map 1:1 to the verifier tests. |

## Why the verifier is honest

- Ground truth lives in `tests/` (copied to `/tests` only at verify time), so the
  agent never sees it and cannot tamper with the pass/fail signal.
- The reward is recomputed from the agent's actual output on every run; a
  pre-existing reward file is never trusted.
