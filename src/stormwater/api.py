"""JSON API for stormwater calculator. FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .rates import load_esu_rates
from .scenarios import homeowner_scenario
from .schemas import EstimateRequest, EstimateResponse, FeeResultResponse, PerviousOptionResponse

app = FastAPI(title="Stormwater Advisor", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict:
    """Liveness check."""
    return {"status": "ok"}


@app.get("/api/municipalities")
def list_municipalities() -> list:
    """Available municipalities."""
    rates = load_esu_rates()
    response = []
    for municipality_id, esu_rate in rates.items():
        item = {
            "municipality_id": municipality_id,
            "display_name": esu_rate.display_name,
            "sqft_per_esu": esu_rate.sqft_per_esu,
            "rate_per_esu": esu_rate.rate_per_esu,
        }
        response.append(item)
    return response



@app.post("/api/estimate")
def estimate(request: EstimateRequest) -> EstimateResponse:
    """Calculate stormwater fees and compare pervious alternatives."""
    try:
        rates = load_esu_rates()
        rate = rates[request.municipality_id]
    except KeyError:
        return JSONResponse(
            status_code=404,
            content={"detail": f"Municipality '{request.municipality_id}' not found"}
        )
    
    comparison = homeowner_scenario(
        request.surfaces,
        request.municipality_id,
        request.parcel_area_sqft,
        request.address,
        rate,
    )
    
    return EstimateResponse(
        baseline=FeeResultResponse(
            esu_count=comparison.baseline.esu_count,
            annual_fee=comparison.baseline.annual_fee,
        ),
        proposed=FeeResultResponse(
            esu_count=comparison.proposed.esu_count,
            annual_fee=comparison.proposed.annual_fee,
        ),
        options=[
            PerviousOptionResponse(
                surface_label=opt.surface_label,
                from_material=opt.from_material.value,
                to_material=opt.to_material.value,
                area_sqft=opt.area_sqft,
                upfront_cost_delta=opt.upfront_cost_delta,
                annual_fee_savings=opt.annual_fee_savings,
            )
            for opt in comparison.options
        ],
        upfront_cost_delta=comparison.upfront_cost_delta,
        annual_savings=comparison.annual_savings,
        simple_payback_years=comparison.simple_payback_years,
    )