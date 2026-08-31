"""Calculate impervious and runoff areas from surface measurements."""

from __future__ import annotations

from .models import Property, Surface

RUNOFF_COEFFICIENTS: dict = {}


def is_impervious(surface: Surface) -> bool:
    """Does this surface count as impervious for billing purposes?"""
    raise NotImplementedError


def impervious_area(prop: Property) -> float:
    area = 0.0
    for surface in prop.surfaces:
        if is_impervious(surface):
            area += surface.area;
    return area
    


def effective_runoff_area(prop: Property) -> float:
    """Area-weighted runoff area: sum(area * runoff_coefficient)."""
    raise NotImplementedError
