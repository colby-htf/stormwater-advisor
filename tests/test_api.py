"""Thin tests. If these get thick, logic has leaked into api.py."""


from fastapi.testclient import TestClient

from stormwater.api import app

client = TestClient(app)

def test_healthz_returns_ok():
    """Make this one pass on day one -- it proves your app boots."""
    response = client.get("/healthz")
    assert response.json() == {"status": "ok"}
    assert response.status_code == 200


def test_estimate_endpoint_returns_comparison():
    payload = {
        "municipality_id": "martinsburg-wv",
        "address": "123 Main St",
        "parcel_area_sqft": 5000,
        "surfaces": [
            {"kind": "roof", "material": "shingle", "area_sqft": 2000, "label": "roof"}
        ]
    }
    response = client.post("/api/estimate", json=payload)
    data = response.json()
    assert response.status_code == 200
    assert set(data.keys()) == {"baseline", "proposed", "options", "upfront_cost_delta", "annual_savings", "simple_payback_years"}


def test_unknown_municipality_returns_4xx_not_500():
    payload = {
        "municipality_id": "fakeplace-usa",
        "address": "123 Main St",
        "parcel_area_sqft": 6767,
        "surfaces": [
            {"kind": "roof", "material": "shingle", "area_sqft": 2000, "label": "roof"}
        ]
    }
    response = client.post("/api/estimate", json=payload)
    assert response.status_code == 404
