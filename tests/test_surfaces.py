
from decimal import Decimal

import pytest

from stormwater.models import Property, Surface, SurfaceKind, SurfaceMaterial
from stormwater.surfaces import impervious_area, is_impervious


def test_empty_property_has_no_impervious_area():
    assert impervious_area(Property()) == Decimal('0.0')


def test_all_lawn_property_has_no_impervious_area():
    assert is_impervious(Surface(kind=SurfaceKind.LAWN, material=SurfaceMaterial.TURF, area_sqft=1000)) is False
    assert impervious_area(Property(surfaces=[Surface(kind=SurfaceKind.LAWN, material=SurfaceMaterial.TURF, area_sqft=1000)])) == (Decimal('0.0'))


def test_roof_and_driveway_sum():
    property = Property(surfaces=[
        Surface(kind=SurfaceKind.ROOF, material=SurfaceMaterial.SHINGLE, area_sqft=2000),
        Surface(kind=SurfaceKind.DRIVEWAY, material=SurfaceMaterial.ASPHALT, area_sqft=600),
    ])
    assert impervious_area(property) == (Decimal('2600.0'))



def test_permeable_paver_driveway_treatment():
    surface = Surface(
        kind=SurfaceKind.DRIVEWAY,
        material=SurfaceMaterial.PERMEABLE_PAVERS,
        area_sqft=500,
    )
    property = Property(surfaces=[surface])
    assert impervious_area(property) == Decimal('0.0')
    

def test_negative_area_is_rejected():
    with pytest.raises(ValueError):
        Surface(kind=SurfaceKind.ROOF, material=SurfaceMaterial.SHINGLE, area_sqft=-100)
