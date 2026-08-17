"""Calculate ESU/ERU counts and annual fees from impervious area."""

from __future__ import annotations

from decimal import Decimal

from .models import FeeResult, Property
from .rates import EsuRate


def esu_count(impervious_sqft: float, rate: EsuRate) -> float:
    """Raw, unrounded ESU count."""
    raise NotImplementedError


def billable_esu(raw_count: float, rate: EsuRate) -> float:
    """Apply the municipality's rounding rule, floor, and cap."""
    raise NotImplementedError


def annual_fee(prop: Property, rate: EsuRate) -> FeeResult:
    """Full pipeline: property -> impervious area -> ESUs -> annual dollars."""
    raise NotImplementedError
