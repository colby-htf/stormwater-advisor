"""
Golden-number tests. The point of this file is to pin real, citable municipal
math so a refactor can never quietly change someone's bill.

Anchor case to build from (verify the current figures yourself, Issue #10):
    Martinsburg, WV -- 1 ERU = 2,280 sqft impervious, $12.00/month.
    A 4,560 sqft impervious property is exactly 2 ERUs.
    What is its annual fee? Compute by hand, put that number here.

Then the interesting one: 3,000 sqft impervious is 1.316 ERUs.
Write a test for each plausible rounding rule and see how far apart the
answers are. That spread is your motivation for Issue #11.
"""

import pytest

pytestmark = pytest.mark.skip(reason="TODO: Issue #11")


def test_exactly_one_esu():
    raise NotImplementedError


def test_exactly_two_esu_annual_fee():
    raise NotImplementedError


def test_partial_esu_applies_rounding_rule():
    raise NotImplementedError


def test_minimum_charge_floor_applies():
    """A tiny cabin with 300 sqft of roof should not be billed $1.58."""
    raise NotImplementedError


def test_unknown_municipality_raises():
    """Not returns zero. Raises. Know why you care."""
    raise NotImplementedError
