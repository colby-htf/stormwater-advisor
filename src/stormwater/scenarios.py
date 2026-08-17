"""Orchestration layer composing core modules into homeowner and developer scenarios."""

from __future__ import annotations

from .models import Comparison, Property


def homeowner_scenario(prop: Property) -> Comparison:
    """MVP path: fee today, fee with pervious swaps, savings, payback."""
    raise NotImplementedError


def developer_scenario(prop: Property, design_depth_inches: float) -> dict:
    """Milestone 7. Adds required mitigation infrastructure and its cost,
    then compares 'build detention' against 'build pervious'."""
    raise NotImplementedError
