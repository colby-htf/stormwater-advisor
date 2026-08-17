"""
Tests for the savings/payback logic -- the numbers a user will make a
five-figure spending decision on. Treat them accordingly.
"""

import pytest

pytestmark = pytest.mark.skip(reason="TODO: Issue #16")


def test_swapping_driveway_reduces_impervious_area():
    raise NotImplementedError


def test_swap_reduces_annual_fee():
    raise NotImplementedError


def test_payback_period_is_upfront_delta_over_annual_savings():
    raise NotImplementedError


def test_zero_annual_savings_gives_no_payback_not_infinity():
    """Division by zero is lurking here. What should the API return --
    None, infinity, or an error? Decide, then encode the decision."""
    raise NotImplementedError


def test_roof_is_not_offered_as_pervious_pavement_candidate():
    raise NotImplementedError
