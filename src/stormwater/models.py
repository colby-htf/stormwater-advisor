"""Shared domain vocabulary."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum


class SurfaceKind(str, Enum):
    """Surface categories for user entry."""

    ROOF = "roof"
    DRIVEWAY = "driveway"
    WALKWAY = "walkway"
    PATIO = "patio"
    POOL_DECK = "pool_deck"
    PARKING_LOT = "parking_lot"
    GRAVEL = "gravel"
    LAWN = "lawn"


class SurfaceMaterial(str, Enum):
    """What the surface is made of. Drives both cost and perviousness."""

    ASPHALT = "asphalt"
    CONCRETE = "concrete"
    PAVERS = "pavers"
    SHINGLE = "shingle"
    METAL = "metal"
    GRAVEL = "gravel"
    PERVIOUS_CONCRETE = "pervious_concrete"
    POROUS_ASPHALT = "porous_asphalt"
    PERMEABLE_PAVERS = "permeable_pavers"
    GRASS_GRID = "grass_grid"
    TURF = "turf"


@dataclass(frozen=True)
class Surface:
    """One measured patch of ground on a property."""

    kind: SurfaceKind
    material: SurfaceMaterial
    area_sqft: float
    label: str = ""

    def __post_init__(self) -> None:
        raise NotImplementedError


@dataclass
class Property:
    """A parcel: its surfaces, location, and lot area."""

    surfaces: list[Surface] = field(default_factory=list)
    municipality_id: str = ""
    parcel_area_sqft: float | None = None
    address: str | None = None


@dataclass(frozen=True)
class FeeResult:
    """The output of an ESU fee calculation for one property, one year."""

    impervious_sqft: float
    esu_count: float
    billed_esu_count: float
    annual_fee: Decimal
    rate_source: str


@dataclass(frozen=True)
class PerviousOption:
    """One candidate swap: replace surface X's material with a pervious one."""

    surface_label: str
    from_material: SurfaceMaterial
    to_material: SurfaceMaterial
    area_sqft: float
    upfront_cost_delta: Decimal
    annual_fee_savings: Decimal


@dataclass(frozen=True)
class Comparison:
    """Baseline vs. proposed comparison for display and analysis."""

    baseline: FeeResult
    proposed: FeeResult
    options: list[PerviousOption]
    upfront_cost_delta: Decimal
    annual_savings: Decimal
    simple_payback_years: float | None
