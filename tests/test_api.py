"""Thin tests. If these get thick, logic has leaked into api.py."""


from fastapi.testclient import TestClient

from stormwater.api import app, load_esu_rates

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
    assert set(data.keys()) == {"baseline", "proposed", "options", "upfront_cost_delta", "annual_savings", "simple_payback_years", "rate_verified_on", "rate_source_url"}

def test_estimate_returns_fee_detail_and_rate_source():
    rates = load_esu_rates()
    rate = rates["martinsburg-wv"]
    payload = {
            "municipality_id": "martinsburg-wv",
            "address": "123 Main St",
            "parcel_area_sqft": 6767,
            "surfaces": [
                {"kind": "roof", "material": "shingle", "area_sqft": 2000, "label": "roof"}
            ]
        }
    response = client.post("/api/estimate", json=payload)
    data = response.json()
    assert response.status_code == 200
    assert data["rate_source_url"] == rate.source_url
    assert data["rate_verified_on"] == rate.verified_on
    assert data["baseline"]["impervious_sqft"] == 2000.0
    assert float(data["baseline"]["billed_esu_count"]) == 1.0
    assert data["proposed"]["impervious_sqft"] == 0.0
    assert float(data["proposed"]["billed_esu_count"]) == 0.0

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
