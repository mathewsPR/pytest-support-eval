from importlib.metadata import version

import pytest_support


def test_package_import() -> None:
    assert pytest_support.__name__ == "pytest_support"


def test_installed_version() -> None:
    assert version("pytest-support-eval") == "0.1.0"
