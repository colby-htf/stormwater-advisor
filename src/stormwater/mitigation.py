"""BMP sizing and costing for on-site stormwater mitigation. (Milestone 6+)"""

from __future__ import annotations

from decimal import Decimal

from .models import Property


def required_capture_volume_cf(prop: Property, design_depth_inches: float) -> float:
    """Cubic feet of runoff that must be captured or detained on site."""
    raise NotImplementedError


def size_bmp(volume_cf: float, bmp_type: str) -> dict:
    """How many/how large a given best-management-practice must be."""
    raise NotImplementedError


def capital_cost(volume_cf: float, bmp_type: str) -> Decimal:
    """Installed cost for a BMP of this size."""
    raise NotImplementedError


def annual_maintenance_cost(bmp_type: str, size: dict) -> Decimal:
    """Annual maintenance cost for a BMP of this size."""
    raise NotImplementedError
