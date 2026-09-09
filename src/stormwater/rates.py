"""Load and validate reference data for rate lookups."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


class RateNotFoundError(LookupError):
    """Raised when a municipality has no rate on file."""


@dataclass(frozen=True)
class EsuRate:
    """Municipal ESU rate for a given year."""

    municipality_id: str
    display_name: str
    sqft_per_esu: Decimal
    rate_per_esu: Decimal
    billing_period: str
    minimum_charge: Decimal | None
    maximum_esu: Decimal | None
    rounding_rule: str | None = None
    verified_on: str
    source_url: str

    def annualize(self, amount: Decimal) -> Decimal:
        """Convert one billing period's charge to an annual figure."""
        raise NotImplementedError


def load_esu_rates(path: Path | None = None) -> dict[str, EsuRate]:
    """Read data/esu_rates.json into a dict keyed by municipality_id."""
    raise NotImplementedError


def get_rate(municipality_id: str) -> EsuRate:
    """Look up one rate, or raise RateNotFoundError."""
    raise NotImplementedError


def load_material_costs(path: Path | None = None) -> dict:
    """Installed cost per square foot, by SurfaceMaterial."""
    raise NotImplementedError
