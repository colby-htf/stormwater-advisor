"""Pydantic models for API requests and responses."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SurfaceRequest(BaseModel):
    """A surface on the property (roof, driveway, walkway, etc.)."""

    kind: str
    material: str
    area_sqft: float
    label: str


class EstimateRequest(BaseModel):
    """Request to estimate stormwater costs and savings."""

    surfaces: list[SurfaceRequest]
    municipality_id: str
    parcel_area_sqft: float
    address: str


class FeeResultResponse(BaseModel):
    """Annual stormwater fee calculation result."""

    esu_count: Decimal
    annual_fee: Decimal

    model_config = ConfigDict(json_encoders={Decimal: str})


class PerviousOptionResponse(BaseModel):
    """One candidate swap: replace surface X's material with a pervious one."""

    surface_label: str
    from_material: str
    to_material: str
    area_sqft: float
    upfront_cost_delta: Decimal
    annual_fee_savings: Decimal

    model_config = ConfigDict(json_encoders={Decimal: str})


class EstimateResponse(BaseModel):
    """Comparison of baseline vs. proposed scenario with all swaps applied."""

    baseline: FeeResultResponse
    proposed: FeeResultResponse
    options: list[PerviousOptionResponse]
    upfront_cost_delta: Decimal
    annual_savings: Decimal
    simple_payback_years: float | None

    model_config = ConfigDict(json_encoders={Decimal: str})