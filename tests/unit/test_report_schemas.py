from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from pytest_support.schemas import ReportValidationError, validate_test_report

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "fixtures" / "reports"


@pytest.fixture
def report() -> dict[str, Any]:
    """Load a fresh report for each test to avoid shared mutations."""
    path = REPORTS_DIR / "run-002.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("report_id", "expected_counts"),
    [
        ("run-001", (2, 2, 0, 0, 0)),
        ("run-002", (2, 1, 1, 0, 0)),
        ("run-003", (2, 1, 0, 1, 0)),
    ],
)
def test_fixed_reports_are_valid(
    report_id: str,
    expected_counts: tuple[int, int, int, int, int],
) -> None:
    path = REPORTS_DIR / f"{report_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    validated = validate_test_report(data)

    assert validated["report_id"] == report_id
    assert validated["synthetic"] is True
    assert (
        tuple(
            validated["summary"][field]
            for field in ("total", "passed", "failed", "errors", "skipped")
        )
        == expected_counts
    )


def test_report_must_be_an_object() -> None:
    with pytest.raises(ReportValidationError, match="report must be a JSON object"):
        validate_test_report([])


@pytest.mark.parametrize("version", [True, 1.0, 2])
def test_rejects_invalid_schema_version(
    report: dict[str, Any],
    version: object,
) -> None:
    report["schema_version"] = version

    with pytest.raises(ReportValidationError, match="schema_version"):
        validate_test_report(report)


@pytest.mark.parametrize("value", [True, -1, "2"])
def test_rejects_invalid_count_types_and_values(
    report: dict[str, Any],
    value: object,
) -> None:
    report["summary"]["total"] = value

    with pytest.raises(ReportValidationError, match=r"summary\.total"):
        validate_test_report(report)


def test_rejects_total_that_disagrees_with_test_count(
    report: dict[str, Any],
) -> None:
    report["summary"]["total"] = 99

    with pytest.raises(ReportValidationError, match=r"summary\.total"):
        validate_test_report(report)


def test_rejects_wrong_outcome_counts_even_when_total_matches(
    report: dict[str, Any],
) -> None:
    report["summary"]["passed"] = 2
    report["summary"]["failed"] = 0

    with pytest.raises(ReportValidationError, match=r"summary\.passed"):
        validate_test_report(report)


def test_rejects_duplicate_test_identifiers(report: dict[str, Any]) -> None:
    report["tests"][1]["nodeid"] = report["tests"][0]["nodeid"]

    with pytest.raises(ReportValidationError, match="duplicate nodeid"):
        validate_test_report(report)


@pytest.mark.parametrize(
    ("outcome", "phase"),
    [
        ("failed", "setup"),
        ("error", "call"),
    ],
)
def test_rejects_invalid_outcome_phase_combination(
    report: dict[str, Any],
    outcome: str,
    phase: str,
) -> None:
    report["tests"][0]["outcome"] = outcome
    report["tests"][0]["phase"] = phase

    with pytest.raises(ReportValidationError, match="phase is invalid"):
        validate_test_report(report)


def test_rejects_unsupported_outcome(report: dict[str, Any]) -> None:
    report["tests"][0]["outcome"] = "unknown"

    with pytest.raises(ReportValidationError, match="outcome is unsupported"):
        validate_test_report(report)


def test_failure_requires_a_diagnostic_message(report: dict[str, Any]) -> None:
    report["tests"][0]["message"] = "   "

    with pytest.raises(ReportValidationError, match="message"):
        validate_test_report(report)


def test_passed_test_requires_null_message(report: dict[str, Any]) -> None:
    report["tests"][1]["message"] = "Unexpected diagnostic"

    with pytest.raises(ReportValidationError, match="message must be null"):
        validate_test_report(report)


def test_accepts_skipped_test_with_reason(report: dict[str, Any]) -> None:
    report["tests"][0].update(
        outcome="skipped",
        phase="setup",
        message="Optional dependency is unavailable",
    )
    report["summary"]["failed"] = 0
    report["summary"]["skipped"] = 1

    validated = validate_test_report(report)

    assert validated["summary"]["skipped"] == 1
