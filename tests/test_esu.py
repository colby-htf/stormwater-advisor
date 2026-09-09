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

from decimal import Decimal

import pytest

from stormwater.esu import annual_fee, billable_esu
from stormwater.models import Property, Surface, SurfaceKind, SurfaceMaterial
from stormwater.rates import EsuRate

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

def test_martinsburg_3000_sqft():
    rate = EsuRate(
        municipality_id="martinsburg-wv",
        display_name="Martinsburg, WV",
        sqft_per_esu=Decimal(2280),
        rate_per_esu=Decimal("12.00"),
        billing_period="monthly",
        rounding_rule="half",
        minimum_charge=Decimal("6.00"),
        maximum_esu=None,
        source_url="https://codelibrary.amlegal.com/codes/martinsburg/latest/martinsburg_wv/0-0-0-16855",
        verified_on="2026-09-09"
        
    )
    
    prop = Property(surfaces=[
        Surface(kind=SurfaceKind.DRIVEWAY, material=SurfaceMaterial.ASPHALT, area_sqft=3000)
    ])
    
    result = annual_fee(prop, rate)
    assert result == Decimal("216.00")

def test_billable_esu_martinsburg_half_rounding():
    rate = EsuRate(
        municipality_id="martinsburg-wv",
        display_name="Martinsburg, WV",
        sqft_per_esu=Decimal(2280),
        rate_per_esu=Decimal("12.00"),
        billing_period="monthly",
        rounding_rule="half",
        minimum_charge=Decimal("6.00"),
        maximum_esu=None,
        source_url="https://codelibrary.amlegal.com/codes/martinsburg/latest/martinsburg_wv/0-0-0-16855",
        verified_on="2026-09-09"
    )
    
    raw_count = 3000 / Decimal("2280.0")  # ~1.315789
    billable = billable_esu(raw_count, rate)
    assert billable == 1.5  # half rounding should round up to 1.5

def test_martinsburg_3000_sqft_annual_fee():
        raise NotImplementedError

