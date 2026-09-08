"""Validation for the application's simplified test-report format."""

from __future__ import annotations

from collections import Counter
from typing import Any

OUTCOME_COUNTS = {
    "passed": "passed",
    "failed": "failed",
    "error": "errors",
    "skipped": "skipped",
}

ALLOWED_PHASES = {
    "passed": {"call"},
    "failed": {"call"},
    "error": {"setup", "teardown"},
    "skipped": {"setup", "call", "teardown"},
}


class ReportValidationError(ValueError):
    """Raised when a test report violates the application schema."""


def require_text(value: object, field: str) -> str:
    """Require a string containing at least one non-whitespace character."""
    if not isinstance(value, str) or not value.strip():
        raise ReportValidationError(f"{field} must be a non-empty string")
    return value


def validate_test_report(report: object) -> dict[str, Any]:
    """Validate a decoded report and return it without modifying it.

    Required fields are checked; additional fields are allowed.
    Each test node ID must appear exactly once.
    """
    if not isinstance(report, dict):
        raise ReportValidationError("report must be a JSON object")

    version = report.get("schema_version")
    if type(version) is not int or version != 1:
        raise ReportValidationError("schema_version must be integer 1")

    require_text(report.get("report_id"), "report_id")

    if not isinstance(report.get("synthetic"), bool):
        raise ReportValidationError("synthetic must be a boolean")

    summary = report.get("summary")
    if not isinstance(summary, dict):
        raise ReportValidationError("summary must be a JSON object")

    for field in ("total", *OUTCOME_COUNTS.values()):
        value = summary.get(field)
        if type(value) is not int or value < 0:
            raise ReportValidationError(
                f"summary.{field} must be a non-negative integer"
            )

    tests = report.get("tests")
    if not isinstance(tests, list):
        raise ReportValidationError("tests must be a JSON array")

    counts: Counter[str] = Counter()
    seen_nodeids: set[str] = set()

    for index, test in enumerate(tests):
        prefix = f"tests[{index}]"

        if not isinstance(test, dict):
            raise ReportValidationError(f"{prefix} must be a JSON object")

        nodeid = require_text(test.get("nodeid"), f"{prefix}.nodeid")
        if nodeid in seen_nodeids:
            raise ReportValidationError(f"duplicate nodeid: {nodeid}")
        seen_nodeids.add(nodeid)

        outcome = require_text(test.get("outcome"), f"{prefix}.outcome")
        if outcome not in OUTCOME_COUNTS:
            raise ReportValidationError(f"{prefix}.outcome is unsupported: {outcome!r}")

        phase = require_text(test.get("phase"), f"{prefix}.phase")
        if phase not in ALLOWED_PHASES[outcome]:
            raise ReportValidationError(
                f"{prefix}.phase is invalid for outcome {outcome!r}"
            )

        if "message" not in test:
            raise ReportValidationError(f"{prefix}.message is required")

        if outcome == "passed":
            if test["message"] is not None:
                raise ReportValidationError(
                    f"{prefix}.message must be null for passed tests"
                )
        else:
            require_text(test["message"], f"{prefix}.message")

        counts[OUTCOME_COUNTS[outcome]] += 1

    expected_summary = {"total": len(tests)}
    expected_summary.update({field: counts[field] for field in OUTCOME_COUNTS.values()})

    for field, expected in expected_summary.items():
        if summary[field] != expected:
            raise ReportValidationError(
                f"summary.{field} must be {expected}, got {summary[field]}"
            )

    return report
