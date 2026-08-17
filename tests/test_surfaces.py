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

pytestmark = pytest.mark.skip(reason="TODO: Issue #6")


def test_empty_property_has_no_impervious_area():
    """The trivial case. If this is wrong, everything is wrong."""
    raise NotImplementedError


def test_all_lawn_property_has_no_impervious_area():
    raise NotImplementedError


def test_roof_and_driveway_sum():
    """2,000 sqft roof + 600 sqft driveway = ? Write the number you EXPECT
    in the assertion before you write the function."""
    raise NotImplementedError


def test_permeable_paver_driveway_treatment():
    """This test is where you'll discover you have a policy question, not a
    code question. Good. Go find the answer, then write the test."""
    raise NotImplementedError


def test_negative_area_is_rejected():
    raise NotImplementedError
