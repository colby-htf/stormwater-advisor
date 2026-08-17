"""Thin tests. If these get thick, logic has leaked into api.py."""

import pytest

pytestmark = pytest.mark.skip(reason="TODO: Issue #19")


def test_healthz_returns_ok():
    """Make this one pass on day one -- it proves your app boots."""
    raise NotImplementedError


def test_estimate_endpoint_returns_comparison():
    raise NotImplementedError


def test_unknown_municipality_returns_4xx_not_500():
    raise NotImplementedError
