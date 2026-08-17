"""JSON API for stormwater calculator. FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="Stormwater Advisor", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict:
    """Liveness check."""
    return {"status": "ok"}


@app.get("/api/municipalities")
def list_municipalities() -> list:
    """Available municipalities."""
    raise NotImplementedError


@app.post("/api/estimate")
def estimate() -> dict:
    """Calculate stormwater fees and compare pervious alternatives."""
    raise NotImplementedError
