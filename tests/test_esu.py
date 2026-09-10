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

from stormwater.esu import annual_fee, billable_esu, esu_count
from stormwater.models import Property, Surface, SurfaceKind, SurfaceMaterial
from stormwater.rates import EsuRate


@pytest.fixture
def martinsburg_rate():
    """Martinsburg, WV ESU rate for testing."""
    return EsuRate(
        municipality_id="martinsburg-wv",
        display_name="Martinsburg, WV",
        sqft_per_esu=Decimal("2280.0"),
        rate_per_esu=Decimal("12.00"),
        billing_period="monthly",
        rounding_rule="half",
        minimum_charge=Decimal("6.00"),
        maximum_esu=None,
        source_url="https://codelibrary.amlegal.com/codes/martinsburg/latest/martinsburg_wv/0-0-0-16855",
        verified_on="2026-09-09"
    )


def test_exactly_one_esu(martinsburg_rate):
    prop = Property(surfaces=[
        Surface(kind=SurfaceKind.DRIVEWAY, material=SurfaceMaterial.ASPHALT, area_sqft=2280)
    ])
    result = annual_fee(prop, martinsburg_rate)
    assert result.annual_fee == Decimal("144.00")  # 1 ERU × $12.00 × 12 months
    assert result.billed_esu_count == Decimal("1.0")
    assert result.impervious_sqft == 2280.0


def test_exactly_two_esu_annual_fee(martinsburg_rate):
    prop = Property(surfaces=[
            Surface(kind=SurfaceKind.DRIVEWAY, material=SurfaceMaterial.ASPHALT, area_sqft=4560)
        ])
    result = annual_fee(prop, martinsburg_rate)
    assert result.annual_fee == Decimal("288.00")  # 2 ERUs × $12.00 × 12 months


def test_partial_esu_applies_rounding_rule(martinsburg_rate):
    prop = Property(surfaces=[
            Surface(kind=SurfaceKind.DRIVEWAY, material=SurfaceMaterial.ASPHALT, area_sqft=3000)
        ])
    result = annual_fee(prop, martinsburg_rate)
    esu = esu_count(result.impervious_sqft, martinsburg_rate)
    billable = billable_esu(esu, martinsburg_rate)
    assert result.impervious_sqft == 3000.0
    assert esu == Decimal("1.315789473684210526315789474")
    assert billable == Decimal("1.5")  # half rounding should round up to nearest .5
    assert result.annual_fee == Decimal("216.00")  # 1.5 ERU × $12.00 × 12


def test_minimum_charge_floor_applies(martinsburg_rate):
     prop = Property(surfaces=[
         Surface(kind=SurfaceKind.DRIVEWAY, material=SurfaceMaterial.ASPHALT, area_sqft=300)
     ])
     result = annual_fee(prop, martinsburg_rate)

     assert result.impervious_sqft == 300.0
     assert result.esu_count == Decimal("0.1315789473684210526315789474")
     assert result.billed_esu_count == Decimal("0.5")  # half rounding should round up to nearest .5
     assert result.annual_fee == Decimal("72.00")  # 0.5 ERU × $12.00 × 12 months (at minimum charge floor)


def test_billable_esu_martinsburg_half_rounding(martinsburg_rate):
    raw_count = 3000 / Decimal("2280.0")  # ~1.315789
    billable = billable_esu(raw_count, martinsburg_rate)
    assert billable == Decimal("1.5")  # half rounding should round up to 1.5



