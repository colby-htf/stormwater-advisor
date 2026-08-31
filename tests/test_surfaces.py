"""
Start here. Seriously -- this file before any other code.

The functions in surfaces.py are pure, which makes them the easiest thing in
the project to test and the hardest thing to get subtly wrong later. Writing
these tests first forces you to decide what the functions MEAN before you
decide how they work.

Delete the `skip` marks as you implement. A test you can't yet make pass is
a specification; a test you deleted is a regret.
"""

import pytest
from stormwater.models import Surface, SurfaceKind, SurfaceMaterial, Property
from stormwater.surfaces import is_impervious, impervious_area, effective_runoff_area

pytestmark = pytest.mark.skip(reason="TODO: Issue #6")


def test_empty_property_has_no_impervious_area():
    assert impervious_area(Property()) == pytest.approx(0.0)


def test_all_lawn_property_has_no_impervious_area():
    assert is_impervious(Surface(kind=SurfaceKind.LAWN, material=SurfaceMaterial.GRASS)) is False
    assert impervious_area(Property(surfaces=[Surface(kind=SurfaceKind.LAWN, material=SurfaceMaterial.GRASS, area_sqft=1000)])) == pytest.approx(0.0)


def test_roof_and_driveway_sum():
    property = Property(surfaces=[
        Surface(kind=SurfaceKind.ROOF, material=SurfaceMaterial.SHINGLE, area_sqft=2000),
        Surface(kind=SurfaceKind.Driveway, material=SurfaceMaterial.ASPHALT, area_sqft=600),
    ])
    assert impervious_area(property) == pytest.approx(2600.0)



def test_permeable_paver_driveway_treatment():
    """This test is where you'll discover you have a policy question, not a
    code question. Good. Go find the answer, then write the test."""
    raise NotImplementedError


def test_negative_area_is_rejected():
    assert impervious_area(Property()) > 0.0
