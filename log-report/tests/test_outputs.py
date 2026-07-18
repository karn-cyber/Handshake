"""Verify the agent's /app/report.json against the known ground truth.

The ground truth is baked into this test (which lives in /tests and is never
visible to the agent), so the checks validate the *contents* of the report,
not merely that a file exists.
"""

import json
from pathlib import Path

import pytest

REPORT_PATH = Path("/app/report.json")

# Ground truth derived from environment/access.log:
#   6 non-empty lines; IPs {192.168.0.1, 192.168.0.2, 10.0.0.5} -> 3 unique;
#   paths /index.html x3, /about.html x2, /api/login x1 -> top /index.html.
EXPECTED_TOTAL_REQUESTS = 6
EXPECTED_UNIQUE_IPS = 3
EXPECTED_TOP_PATH = "/index.html"


@pytest.fixture(scope="module")
def report():
    """Load and parse the agent-produced report, failing loudly if malformed."""
    assert REPORT_PATH.exists(), f"no report at {REPORT_PATH}"
    assert REPORT_PATH.stat().st_size > 0, "report.json is empty"
    text = REPORT_PATH.read_text()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        pytest.fail(f"report.json is not valid JSON: {e}")
    assert isinstance(data, dict), f"report.json must be a JSON object, got {type(data)}"
    return data


def test_total_requests(report):
    """total_requests equals the number of non-empty log lines."""
    assert "total_requests" in report, "missing key: total_requests"
    assert report["total_requests"] == EXPECTED_TOTAL_REQUESTS, (
        f"total_requests: expected {EXPECTED_TOTAL_REQUESTS}, "
        f"got {report['total_requests']!r}"
    )


def test_unique_ips(report):
    """unique_ips equals the number of distinct client IPs."""
    assert "unique_ips" in report, "missing key: unique_ips"
    assert report["unique_ips"] == EXPECTED_UNIQUE_IPS, (
        f"unique_ips: expected {EXPECTED_UNIQUE_IPS}, got {report['unique_ips']!r}"
    )


def test_top_path(report):
    """top_path is the most frequently requested path."""
    assert "top_path" in report, "missing key: top_path"
    assert report["top_path"] == EXPECTED_TOP_PATH, (
        f"top_path: expected {EXPECTED_TOP_PATH!r}, got {report['top_path']!r}"
    )
