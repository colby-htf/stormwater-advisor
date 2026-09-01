"""Calculate impervious and runoff areas from surface measurements."""

from __future__ import annotations

from decimal import Decimal

from .models import Property, Surface, SurfaceMaterial

#TODO: Refine, add more granular values after MVP
RUNOFF_COEFFICIENTS: dict = {
    SurfaceMaterial.ASPHALT: Decimal("0.82"),      # 0.70–0.95 → midpoint
    SurfaceMaterial.CONCRETE: Decimal("0.87"),     # 0.80–0.95 → midpoint
    SurfaceMaterial.PAVERS: Decimal("0.77"),       # 0.70–0.85 → midpoint (brick proxy)
    SurfaceMaterial.SHINGLE: Decimal("0.85"),      # 0.75–0.95 → midpoint
    SurfaceMaterial.METAL: Decimal("0.85"),        # Similar to shingle
    SurfaceMaterial.TURF: Decimal("0.20"),         # 0.18–0.22 → midpoint
    SurfaceMaterial.GRASS_GRID: Decimal("0.15"),   # Slightly more pervious than turf
    SurfaceMaterial.GRAVEL: Decimal("0.30"),       # Common estimate
    SurfaceMaterial.PERVIOUS_CONCRETE: Decimal("0.05"),  # Nearly pervious
    SurfaceMaterial.POROUS_ASPHALT: Decimal("0.10"),      #  Much better than standard
    SurfaceMaterial.PERMEABLE_PAVERS: Decimal("0.10"),    #  Designed to drain
}


def is_impervious(surface: Surface) -> bool:
    pervious_materials = {
        SurfaceMaterial.GRAVEL,
        SurfaceMaterial.PERVIOUS_CONCRETE,
        SurfaceMaterial.POROUS_ASPHALT,
        SurfaceMaterial.PERMEABLE_PAVERS,
        SurfaceMaterial.GRASS_GRID,
        SurfaceMaterial.TURF,
    }
    return surface.material not in pervious_materials


def impervious_area(prop: Property) -> Decimal:
    area = Decimal('0.0')
    for surface in prop.surfaces:
        if is_impervious(surface):
            area += surface.area_sqft
    return area
    


def effective_runoff_area(prop: Property) -> Decimal:
    total = Decimal('0.0')
    for surface in prop.surfaces:
        if is_impervious(surface):
            coefficient = RUNOFF_COEFFICIENTS.get(surface.material)
            total += surface.area_sqft * coefficient
    return total