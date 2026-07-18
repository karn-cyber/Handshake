"""Verify /app/report.json against the ground truth for the access log.

The ground truth is baked into this test, which lives in /tests and is never
visible to the agent, so these checks validate the *contents* of the report
rather than merely that a file exists. There is exactly one test per
instruction.md success criterion.
"""

import json
from pathlib import Path

import pytest

REPORT_PATH = Path("/app/report.json")

# Ground truth derived from environment/access.log:
#   6 non-empty lines;
#   IPs {192.168.0.1, 192.168.0.2, 10.0.0.5} -> 3 unique;
#   paths /index.html x3, /about.html x2, /api/login x1 -> top /index.html.
EXPECTED_TOTAL_REQUESTS = 6
EXPECTED_UNIQUE_IPS = 3
EXPECTED_TOP_PATH = "/index.html"


@pytest.fixture(scope="module")
def report():
    """Load and parse the agent-produced report once for all value checks."""
    text = REPORT_PATH.read_text()
    return json.loads(text)


def test_report_is_valid_json_object():
    """Criterion 1: /app/report.json exists and is a single valid JSON object
    containing total_requests, unique_ips, and top_path."""
    assert REPORT_PATH.exists(), f"no report at {REPORT_PATH}"
    assert REPORT_PATH.stat().st_size > 0, "report.json is empty"
    try:
        data = json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as e:
        pytest.fail(f"report.json is not valid JSON: {e}")
    assert isinstance(data, dict), f"report.json must be a JSON object, got {type(data)}"
    for key in ("total_requests", "unique_ips", "top_path"):
        assert key in data, f"missing key: {key}"


def test_total_requests(report):
    """Criterion 2: total_requests equals the number of non-empty log lines."""
    assert report["total_requests"] == EXPECTED_TOTAL_REQUESTS, (
        f"total_requests: expected {EXPECTED_TOTAL_REQUESTS}, "
        f"got {report.get('total_requests')!r}"
    )


def test_unique_ips(report):
    """Criterion 3: unique_ips equals the number of distinct client IPs."""
    assert report["unique_ips"] == EXPECTED_UNIQUE_IPS, (
        f"unique_ips: expected {EXPECTED_UNIQUE_IPS}, got {report.get('unique_ips')!r}"
    )


def test_top_path(report):
    """Criterion 4: top_path is the most frequently requested path."""
    assert report["top_path"] == EXPECTED_TOP_PATH, (
        f"top_path: expected {EXPECTED_TOP_PATH!r}, got {report.get('top_path')!r}"
    )
