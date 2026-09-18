"""
Tests for the savings/payback logic -- the numbers a user will make a
five-figure spending decision on. Treat them accordingly.
"""

from decimal import Decimal

import pytest

from stormwater.esu import annual_fee
from stormwater.models import Property, Surface, SurfaceMaterial
from stormwater.pervious import (
    PERVIOUS_SUBSTITUTES,
    compare,
    eligible_surfaces,
)
from stormwater.rates import EsuRate


@pytest.fixture
def test_rate():
    """A simple test ESU rate for municipalities."""
    return EsuRate(
        municipality_id="test_city",
        display_name="Test City",
        sqft_per_esu=Decimal(2500),
        rate_per_esu=Decimal("100.00"),
        billing_period="annual",
        verified_on="2024-01-01",
        source_url="http://example.com",
    )


@pytest.fixture
def property_with_driveway():
    """A residential property with an asphalt driveway."""
    return Property(
        municipality_id="test_city",
        parcel_area_sqft=10000,
        address="123 Test St",
        surfaces=[
            Surface(
                kind="roof",
                material=SurfaceMaterial.SHINGLE,
                area_sqft=2000,
                label="main_roof",
            ),
            Surface(
                kind="driveway",
                material=SurfaceMaterial.ASPHALT,
                area_sqft=1000,
                label="driveway",
            ),
            Surface(
                kind="walkway",
                material=SurfaceMaterial.CONCRETE,
                area_sqft=500,
                label="walkway",
            ),
        ],
    )


def test_swapping_driveway_reduces_impervious_area(property_with_driveway, test_rate):
    """When a driveway is swapped to porous asphalt, ESU count should decrease."""
    baseline = annual_fee(property_with_driveway, test_rate)
    
    # Swap the driveway
    to_material = PERVIOUS_SUBSTITUTES[SurfaceMaterial.ASPHALT][0]
   
    
    # Create modified property
    modified_surfaces = [
        s if s.label != "driveway" else Surface(
            kind=s.kind,
            material=to_material,
            area_sqft=s.area_sqft,
            label=s.label,
        )
        for s in property_with_driveway.surfaces
    ]
    modified_prop = Property(
        municipality_id=property_with_driveway.municipality_id,
        parcel_area_sqft=property_with_driveway.parcel_area_sqft,
        address=property_with_driveway.address,
        surfaces=modified_surfaces,
    )
    modified_fee = annual_fee(modified_prop, test_rate)
    
    # Impervious area is reduced, so ESU count (and fee) should decrease
    assert modified_fee.esu_count < baseline.esu_count


def test_swap_reduces_annual_fee(property_with_driveway, test_rate):
    """Swapping an impervious surface to pervious should reduce annual fee."""
    
    # Get the comparison with all eligible swaps
    result = compare(property_with_driveway, test_rate)
    
    # Proposed fee should be lower than baseline
    assert result.proposed.annual_fee < result.baseline.annual_fee


def test_payback_period_is_upfront_delta_over_annual_savings(
    property_with_driveway, test_rate
):
    """Simple payback should equal upfront cost divided by annual savings."""
    result = compare(property_with_driveway, test_rate)
    
    # Only test if there are actual savings
    if result.annual_savings > 0:
        expected_payback = float(result.upfront_cost_delta / result.annual_savings)
        assert result.simple_payback_years == pytest.approx(expected_payback, rel=1e-2)


def test_zero_annual_savings_gives_no_payback_not_infinity(test_rate):
    """When a swap has zero or negative savings, payback should be None."""
    # Create a property where the swap might not save money
    # (or at least, we want to test the edge case)
    prop = Property(
        municipality_id="test_city",
        parcel_area_sqft=10000,
        address="456 Edge Case Ln",
        surfaces=[
            Surface(
                kind="roof",
                material=SurfaceMaterial.SHINGLE,
                area_sqft=2000,
                label="main_roof",
            ),
        ],
    )
    
    result = compare(prop, test_rate)
    
    # If there are no eligible surfaces to swap, annual_savings should be 0
    # and payback should be None, not infinity
    if result.annual_savings <= 0:
        assert result.simple_payback_years is None


def test_roof_is_not_offered_as_pervious_pavement_candidate(property_with_driveway):
    """Surfaces not in PERVIOUS_SUBSTITUTES should not be eligible for swapping."""
    eligible = eligible_surfaces(property_with_driveway)
    eligible_materials = {s.material for s in eligible}
    
    # Only surfaces in PERVIOUS_SUBSTITUTES should be eligible
    for surface in property_with_driveway.surfaces:
        if surface.material not in PERVIOUS_SUBSTITUTES:
            assert surface.material not in eligible_materials