"""Calculate ESU/ERU counts and annual fees from impervious area."""

from __future__ import annotations

from decimal import ROUND_UP, Decimal

from .models import FeeResult, Property
from .rates import EsuRate
from .surfaces import impervious_area


def esu_count(impervious_sqft: float, rate: EsuRate) -> Decimal:
    """Raw, unrounded ESU count."""
    sqft_decimal = Decimal(str(impervious_sqft))  # ← Convert here
    return sqft_decimal / rate.sqft_per_esu


def billable_esu(raw_esu: Decimal, rate: EsuRate) -> Decimal:
    """Apply the municipality's rounding rule, floor, and cap."""
    billable = raw_esu
    if rate.rounding_rule == "exact":
        pass
    elif rate.rounding_rule == "half":
        billable = (raw_esu * Decimal(2)).quantize(Decimal(1), rounding=ROUND_UP) / Decimal(2)
    elif rate.rounding_rule == "whole":
        # Round UP to nearest 1.0
        billable = raw_esu.quantize(Decimal(1), rounding=ROUND_UP)
    else:
        raise NotImplementedError(f"Rounding rule '{rate.rounding_rule}' not implemented")

    if rate.minimum_charge is not None:
        min_esu = rate.minimum_charge / rate.rate_per_esu
        billable = max(billable, min_esu)

    return billable



def annual_fee(prop: Property, rate: EsuRate) -> FeeResult:
    """Full pipeline: property -> impervious area -> ESUs -> annual dollars."""
    impervious_sqft = impervious_area(prop)
    raw_esu = esu_count(impervious_sqft, rate)
    billable = billable_esu(raw_esu, rate)
    annual_fee = billable * rate.rate_per_esu * Decimal(12)  # monthly → annual
    return FeeResult(
        impervious_sqft=float(impervious_sqft),
        esu_count=raw_esu,
        billed_esu_count=billable,
        annual_fee=annual_fee,
        rate_source=rate.source_url,
    )
