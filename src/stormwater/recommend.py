"""LLM recommendation layer. Converts Comparison objects to prose. (Milestone 8+)"""

from __future__ import annotations

from .models import Comparison

SYSTEM_PROMPT = """\
TODO (Issue #34). Constraints this prompt must encode:
  - You may not perform arithmetic. Every figure comes from the input.
  - You may not invent municipal policy, rebates, or credits.
  - If payback exceeds the surface's expected lifespan, say so plainly.
  - State that estimates are planning-level and not a permit determination.
"""


def summarize_for_model(comparison: Comparison) -> dict:
    """Reduce a Comparison to the minimum the model needs."""
    raise NotImplementedError


def generate_recommendation(comparison: Comparison) -> str:
    """Comparison in, plain-English guidance out."""
    raise NotImplementedError


def validate_no_new_numbers(comparison: Comparison, text: str) -> list[str]:
    """Return every numeric claim in text that isn't grounded in comparison."""
    raise NotImplementedError
