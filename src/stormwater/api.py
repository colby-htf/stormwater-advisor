"""JSON API for stormwater calculator. FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .models import Property, Surface, SurfaceMaterial, SurfaceKind
from .rates import load_esu_rates
from .pervious import compare
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

    surfaces = [
        Surface(
            kind=SurfaceKind(s.kind),
            material=SurfaceMaterial(s.material),
            area_sqft=s.area_sqft,
            label=s.label,
        )
        for s in request.surfaces
    ]

    prop = Property(
        surfaces=surfaces,
        municipality_id=request.municipality_id,
        parcel_area_sqft=request.parcel_area_sqft,
        address=request.address,
    )

    comparison = compare(prop, rate)
