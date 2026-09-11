"""Load and validate reference data for rate lookups."""

from __future__ import annotations

import json
import os

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

@dataclass(frozen=True)
class EsuRate:
    """Municipal ESU rate for a given year."""

    municipality_id: str
    display_name: str
    sqft_per_esu: Decimal
    rate_per_esu: Decimal
    billing_period: str
    verified_on: str
    source_url: str
    # Optional fields with defaults below:
    rounding_rule: str | None = None
    minimum_charge: Decimal | None = None
    maximum_esu: Decimal | None = None


    def annualize(self, amount: Decimal) -> Decimal:
        """Convert a monthly or annual amount to an annual amount."""
        if self.billing_period == "monthly":
            return amount * Decimal(12)
        elif self.billing_period == "quarterly":
            return amount * Decimal(4)
        elif self.billing_period == "annual":
            return amount
        else:
            raise ValueError(f"Unknown billing period: {self.billing_period}")


        

class RateNotFoundError(LookupError):
    """Raised when a municipality has no rate on file."""


"""Read data/esu_rates.json into a dict keyed by municipality_id."""
def load_esu_rates(path: Path | None = None) -> dict[str, EsuRate]:
    try:
        with open(DATA_DIR/"esu_rates.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find ESU rates file at {path}")

    rates = {}
    for item in data:
        try:
            rate = EsuRate(
                display_name=item["display_name"],
                sqft_per_esu=Decimal(item["sqft_per_esu"]),
                rate_per_esu=Decimal(item["rate_per_esu"]),
                billing_period=item["billing_period"],
                verified_on=item["verified_on"],
                source_url=item["source_url"],
                rounding_rule=item.get("rounding_rule"),
                minimum_charge=Decimal(item["minimum_charge"]) if item.get("minimum_charge") else None,
                maximum_esu=Decimal(item["maximum_esu"]) if item.get("maximum_esu") else None,
            )
            rates[rate.municipality_id] = rate
        except KeyError as e:
            raise ValueError(f"Missing required field {e} in ESU rate data: {item}")
        except Exception as e:
            raise ValueError(f"Error processing ESU rate data: {item}. Error: {e}")

    
def get_rate(municipality_id: str) -> EsuRate:
    """Look up one rate, or raise RateNotFoundError."""
    raise NotImplementedError


def load_material_costs(path: Path | None = None) -> dict:
    """Installed cost per square foot, by SurfaceMaterial."""
    raise NotImplementedError
