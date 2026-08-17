"""Evaluate pervious pavement swap alternatives and cost comparisons."""

from __future__ import annotations

from decimal import Decimal

from .models import Comparison, PerviousOption, Property, SurfaceMaterial
from .rates import EsuRate

PERVIOUS_SUBSTITUTES: dict[SurfaceMaterial, list[SurfaceMaterial]] = {}


def eligible_surfaces(prop: Property) -> list:
    """Surfaces that could physically be converted to a pervious material."""
    raise NotImplementedError


def upfront_cost_delta(
    area_sqft: float,
    from_material: SurfaceMaterial,
    to_material: SurfaceMaterial,
) -> Decimal:
    """The EXTRA cost of choosing pervious over conventional."""
    raise NotImplementedError


def evaluate_option(
    prop: Property, surface_label: str, to_material: SurfaceMaterial, rate: EsuRate
) -> PerviousOption:
    """Price a single swap."""
    raise NotImplementedError


def compare(prop: Property, rate: EsuRate) -> Comparison:
    """Baseline vs. all-recommended-swaps. The headline result."""
    raise NotImplementedError
