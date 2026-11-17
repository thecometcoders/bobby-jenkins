"""Smoke tests for the installed package."""

from importlib.metadata import version

import bobby_jenkins


def test_package_is_installed() -> None:
    assert bobby_jenkins.__doc__
    assert version("bobby-jenkins")
