"""High-level scenario functions for different user types."""

from __future__ import annotations

from .models import Property, Surface, SurfaceKind, SurfaceMaterial
from .pervious import compare
from .rates import EsuRate


def homeowner_scenario(
    surfaces: list,  # List of SurfaceRequest objects
    municipality_id: str,
    parcel_area_sqft: float,
    address: str,
    rate: EsuRate,
):
    """Evaluate stormwater costs and pervious alternatives for a homeowner."""
    # Convert request surfaces to domain surfaces
    domain_surfaces = [
        Surface(
            kind=SurfaceKind(s.kind),
            material=SurfaceMaterial(s.material),
            area_sqft=s.area_sqft,
            label=s.label,
        )
        for s in surfaces
    ]
    
    # Create property
    prop = Property(
        surfaces=domain_surfaces,
        municipality_id=municipality_id,
        parcel_area_sqft=parcel_area_sqft,
        address=address,
    )
    
    # Run comparison
    return compare(prop, rate)


def developer_scenario(prop: Property, design_depth_inches: float) -> dict:
    """Milestone 7. Adds required mitigation infrastructure and its cost,
    then compares 'build detention' against 'build pervious'."""
    raise NotImplementedError
