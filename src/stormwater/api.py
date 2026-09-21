"""JSON API for stormwater calculator. FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI

from .rates import load_esu_rates

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
def estimate() -> dict:
    """Calculate stormwater fees and compare pervious alternatives."""
    raise NotImplementedError
